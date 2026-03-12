from pytrends.request import TrendReq


def check_trend(keyword: str, timeframe: str = "today 3-m") -> dict:
    """Check Google Trends interest for a single keyword.

    Returns a dict with keyword, trend_direction, avg_interest, and recent_interest.
    """
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([keyword], timeframe=timeframe)
    data = pytrends.interest_over_time()

    if data.empty or keyword not in data.columns:
        return {
            "keyword": keyword,
            "trend_direction": "no_data",
            "avg_interest": 0,
            "recent_interest": 0,
        }

    values = data[keyword].tolist()
    avg_interest = round(sum(values) / len(values), 1)
    recent = values[-4:]
    recent_interest = round(sum(recent) / len(recent), 1)

    if recent_interest > avg_interest * 1.15:
        direction = "rising"
    elif recent_interest < avg_interest * 0.85:
        direction = "declining"
    else:
        direction = "stable"

    return {
        "keyword": keyword,
        "trend_direction": direction,
        "avg_interest": avg_interest,
        "recent_interest": recent_interest,
    }


def check_trends_batch(keywords: list[str], timeframe: str = "today 3-m") -> list[dict]:
    """Check Google Trends interest for multiple keywords."""
    return [check_trend(kw, timeframe) for kw in keywords]
