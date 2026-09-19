"""
Phân loại sentiment tin tức tài chính TIẾNG VIỆT theo từ điển (lexicon-based).

Vì sao chọn cách này thay vì tải model AI (FinBERT...)?
  - Môi trường dev/sandbox không có internet để tải model.
  - Model FinBERT tiếng Anh không hiểu sắc thái tiếng Việt ("khối ngoại xả hàng"
    khác "khối ngoại bán ròng" nhưng cùng nghĩa tiêu cực) — cần từ điển riêng.
  - Lexicon-based: nhanh (~0ms/tin), không cần GPU, minh bạch, dễ mở rộng bằng
    cách thêm từ khoá — rất phù hợp để CHẠY NGAY.

Khi cần độ chính xác cao hơn (giai đoạn 2 trong roadmap), có 2 hướng nâng cấp,
đã để hàm `classify_with_llm()` làm điểm cắm:
  1. Gán nhãn tay 1000-2000 tiêu đề rồi fine-tune PhoBERT/DistilBERT đa ngôn ngữ.
  2. Gọi LLM (Claude API) để phân loại — chính xác hơn lexicon nhưng tốn phí/latency.
"""
from __future__ import annotations
import re

from app.config import USE_GEMINI
from app.utils.cache import sentiment_cache, cached

POSITIVE_KEYWORDS = [
    "tăng trưởng", "bứt phá", "lập đỉnh", "mua ròng", "lãi", "lợi nhuận tăng",
    "vượt kỳ vọng", "khả quan", "tích cực", "hồi phục", "bùng nổ", "kỷ lục",
    "mở rộng", "đầu tư mới", "ký kết hợp đồng", "trúng thầu", "cổ tức cao",
    "nâng hạng", "khuyến nghị mua", "dòng tiền mạnh", "vượt đỉnh", "khởi sắc",
    "bắt đáy", "giải ngân", "gom hàng", "target giá tăng", "thượng hạn",
]

NEGATIVE_KEYWORDS = [
    "giảm sàn", "bán ròng", "xả hàng", "thua lỗ", "lỗ", "sụt giảm", "rủi ro",
    "cảnh báo", "điều tra", "phạt", "vi phạm", "nợ xấu", "phá sản", "bán tháo",
    "áp lực bán", "downtrend", "mất thanh khoản", "hủy niêm yết", "cắt margin",
    "hạ hạng", "khuyến nghị bán", "chi phí tăng", "thị phần giảm", "kiện tụng",
    "đình chỉ", "tạm ngừng", "sai phạm", "thao túng",
]

NEGATION_WORDS = {"không", "chưa", "chẳng", "đừng", "khó"}


def _tokenize_context(text: str, keyword: str, window: int = 3) -> bool:
    """Trả về True nếu keyword bị phủ định gần đó (vd 'không tăng trưởng')."""
    idx = text.find(keyword)
    if idx == -1:
        return False
    before = text[max(0, idx - 20):idx].split()
    return any(neg in before[-window:] for neg in NEGATION_WORDS)


def _classify_lexicon(text: str) -> dict:
    """Trả về {label, score, matched_positive, matched_negative}.
    score dương = tích cực, âm = tiêu cực, khoảng [-1, 1]."""
    text_lower = text.lower()
    pos_hits, neg_hits = [], []

    for kw in POSITIVE_KEYWORDS:
        if kw in text_lower:
            if _tokenize_context(text_lower, kw):
                neg_hits.append(f"(phủ định) {kw}")
            else:
                pos_hits.append(kw)

    for kw in NEGATIVE_KEYWORDS:
        if kw in text_lower:
            if _tokenize_context(text_lower, kw):
                pos_hits.append(f"(phủ định) {kw}")
            else:
                neg_hits.append(kw)

    raw_score = len(pos_hits) - len(neg_hits)
    total = len(pos_hits) + len(neg_hits)
    score = 0.0 if total == 0 else raw_score / total

    if score > 0.15:
        label = "Tích cực"
    elif score < -0.15:
        label = "Tiêu cực"
    else:
        label = "Trung lập"

    return dict(
        label=label,
        score=round(score, 2),
        matched_positive=pos_hits,
        matched_negative=neg_hits,
    )

@cached(sentiment_cache, "classify")
def classify(text: str) -> dict:
    """Dùng Gemini nếu USE_GEMINI=true và có key, tự fallback về lexicon nếu
    Gemini tắt/thiếu key/lỗi/hết quota (không bao giờ crash). Cache theo text,
    TTL = CACHE_TTL_SENTIMENT, áp dụng cho cả 2 nhánh."""
    if USE_GEMINI:
        try:
            from app.analysis.gemini_client import classify_sentiment_gemini
            return classify_sentiment_gemini(text)
        except Exception:
            pass  # rơi xuống lexicon, không để lỗi Gemini lan ra ngoài
    return _classify_lexicon(text)


def classify_with_llm(text: str, call_llm_fn) -> dict:
    """Điểm cắm để nâng cấp độ chính xác bằng LLM thay vì lexicon.
    `call_llm_fn` là 1 hàm bạn tự truyền vào, ví dụ gọi Claude API:

        def call_claude(prompt: str) -> str:
            resp = anthropic_client.messages.create(...)
            return resp.content[0].text

        result = classify_with_llm(title, call_claude)

    Hàm này KHÔNG tự gọi API — tách rời để bạn kiểm soát chi phí/API key.
    """
    prompt = (
        "Phân loại sentiment của tin tức chứng khoán sau đây thành đúng 1 trong 3 "
        "nhãn: Tích cực / Tiêu cực / Trung lập. Chỉ trả về đúng 1 từ.\n\n"
        f"Tin: {text}"
    )
    label = call_llm_fn(prompt).strip()
    if label not in ("Tích cực", "Tiêu cực", "Trung lập"):
        label = "Trung lập"
    return dict(label=label, score=None, matched_positive=[], matched_negative=[])


def classify_batch(items: list[dict], text_field: str = "title") -> list[dict]:
    """Nhận list tin tức (dict có field `title`/`raw_text`), trả về list đã gắn
    thêm key 'sentiment'."""
    out = []
    for item in items:
        text = item.get(text_field) or item.get("raw_text") or ""
        result = classify(text)
        merged = dict(item)
        merged["sentiment"] = result
        out.append(merged)
    return out