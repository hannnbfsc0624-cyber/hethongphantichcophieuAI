"""Thông tin doanh nghiệp thật: hồ sơ công ty, cổ đông lớn, ban lãnh đạo.
Dùng thư viện vnstock — cần Internet."""
from __future__ import annotations


def get_company_profile(ticker: str) -> dict:
    ticker = ticker.upper()
    try:
        from vnstock import Vnstock
        c = Vnstock().stock(symbol=ticker, source="VCI").company
    except Exception as e:
        return dict(ticker=ticker, overview={}, shareholders=[], officers=[], error=str(e))

    def _safe(fn):
        try:
            return fn().to_dict(orient="records")
        except Exception:
            return []

    overview_records = _safe(c.overview)
    return dict(
        ticker=ticker,
        overview=overview_records[0] if overview_records else {},
        shareholders=_safe(c.shareholders),
        officers=_safe(lambda: c.officers(filter_by="working")),
    )