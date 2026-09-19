"""Client gọi Google Gemini API: (1) phân loại sentiment chính xác hơn lexicon,
(2) sinh khuyến nghị đầu tư chi tiết bằng tiếng Việt.

Mọi hàm ở đây RAISE GeminiUnavailable thay vì tự fallback — nơi gọi
(sentiment.py, screener.py) chịu trách nhiệm try/except. Nhờ vậy thiếu API
key / lỗi / hết quota KHÔNG làm crash web."""
from __future__ import annotations
import json
import concurrent.futures

from app.config import GEMINI_API_KEY, USE_GEMINI
from app.utils.cache import gemini_cache, cached


class GeminiUnavailable(Exception):
    """USE_GEMINI=false, thiếu key, hết quota, hoặc lỗi gọi API."""


def _get_model():
    if not USE_GEMINI:
        raise GeminiUnavailable("USE_GEMINI=false — Gemini đang tắt.")
    if not GEMINI_API_KEY:
        raise GeminiUnavailable("Thiếu GEMINI_API_KEY trong .env.")
    try:
        import google.generativeai as genai
    except ImportError:
        raise GeminiUnavailable("Chưa cài thư viện: pip install google-generativeai")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-1.5-flash")


def _call_gemini(prompt: str, timeout: int = 20) -> str:
    model = _get_model()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(lambda: model.generate_content(prompt))
        try:
            resp = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise GeminiUnavailable(f"Gemini quá thời gian chờ ({timeout}s).")
        except Exception as e:
            raise GeminiUnavailable(f"Lỗi gọi Gemini: {e}")
    try:
        return resp.text.strip()
    except Exception as e:
        raise GeminiUnavailable(f"Gemini trả về rỗng/lỗi: {e}")


def classify_sentiment_gemini(text: str) -> dict:
    """Không tự cache ở đây — sentiment.classify() đã cache toàn bộ kết quả
    (Gemini hay lexicon) theo CACHE_TTL_SENTIMENT."""
    prompt = (
        "Bạn là chuyên gia phân tích tài chính Việt Nam. Phân loại sentiment của "
        "tiêu đề tin tức chứng khoán sau vào ĐÚNG 1 nhãn: Tích cực, Tiêu cực, hoặc "
        "Trung lập. Chỉ trả về JSON hợp lệ, không thêm chữ nào khác:\n"
        '{"label": "Tích cực" | "Tiêu cực" | "Trung lập", "score": <số từ -1 đến 1>}\n\n'
        f"Tiêu đề: {text}"
    )
    raw = _call_gemini(prompt).strip()
    if raw.startswith("```"):
        raw = raw.strip("`").removeprefix("json").strip()
    try:
        data = json.loads(raw)
        label = data.get("label", "Trung lập")
        score = float(data.get("score", 0))
    except Exception:
        raise GeminiUnavailable(f"Không parse được JSON từ Gemini: {raw[:200]}")
    if label not in ("Tích cực", "Tiêu cực", "Trung lập"):
        label = "Trung lập"
    return dict(label=label, score=round(max(-1.0, min(1.0, score)), 2),
                matched_positive=[], matched_negative=[], engine="gemini")


@cached(gemini_cache, "recommendation")
def generate_recommendation_gemini(ticker: str, technical_signal: dict, news_titles: list[str],
                                    sentiment_net: float) -> str:
    news_block = "\n".join(f"- {t}" for t in news_titles[:8]) or "(không có tin tức gần đây)"
    prompt = (
        "Bạn là chuyên gia phân tích chứng khoán Việt Nam, viết khuyến nghị đầu tư "
        "NGẮN GỌN (4-6 câu), bằng tiếng Việt, dựa CHỈ trên dữ liệu dưới đây — không "
        "bịa thêm số liệu. Nêu rõ: nhận định xu hướng, điểm cần lưu ý từ tin tức, và "
        "một khuyến nghị hành động thận trọng kèm câu miễn trừ trách nhiệm ở cuối.\n\n"
        f"Mã cổ phiếu: {ticker}\n"
        f"Tín hiệu kỹ thuật: {technical_signal.get('trend')} (điểm {technical_signal.get('score')})\n"
        f"Chi tiết kỹ thuật: {'; '.join(technical_signal.get('detail', []))}\n"
        f"Sentiment tin tức (net, -1 đến 1): {sentiment_net}\n"
        f"Tin tức gần đây:\n{news_block}"
    )
    return _call_gemini(prompt, timeout=25)