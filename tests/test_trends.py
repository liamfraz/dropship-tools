from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from ds.scout.trends import check_trend, check_trends_batch


# --- Live tests (require internet, may fail due to rate limiting) ---


def test_check_trend_returns_dict():
    result = check_trend("water bottle")
    assert "keyword" in result
    assert "trend_direction" in result  # "rising", "stable", "declining"
    assert "avg_interest" in result
    assert "recent_interest" in result
    assert isinstance(result["avg_interest"], (int, float))


def test_check_trend_multiple_keywords():
    results = check_trends_batch(["water bottle", "phone case"])
    assert len(results) == 2
    assert all("keyword" in r for r in results)


# --- Mock-based fallback tests (always pass, no internet needed) ---


def _mock_interest_data(keyword: str, values: list[int]) -> pd.DataFrame:
    """Build a DataFrame mimicking pytrends interest_over_time output."""
    dates = pd.date_range("2025-01-01", periods=len(values), freq="W")
    return pd.DataFrame({keyword: values, "isPartial": [False] * len(values)}, index=dates)


@patch("ds.scout.trends.TrendReq")
def test_check_trend_rising(mock_trendreq_cls):
    mock_pt = MagicMock()
    mock_trendreq_cls.return_value = mock_pt
    # Low average, high recent -> rising
    values = [20, 20, 20, 20, 20, 20, 20, 20, 50, 60, 70, 80]
    mock_pt.interest_over_time.return_value = _mock_interest_data("gadget", values)

    result = check_trend("gadget")
    assert result["keyword"] == "gadget"
    assert result["trend_direction"] == "rising"
    assert result["recent_interest"] > result["avg_interest"]


@patch("ds.scout.trends.TrendReq")
def test_check_trend_declining(mock_trendreq_cls):
    mock_pt = MagicMock()
    mock_trendreq_cls.return_value = mock_pt
    # High average, low recent -> declining
    values = [80, 80, 80, 80, 80, 80, 80, 80, 10, 10, 10, 10]
    mock_pt.interest_over_time.return_value = _mock_interest_data("widget", values)

    result = check_trend("widget")
    assert result["keyword"] == "widget"
    assert result["trend_direction"] == "declining"


@patch("ds.scout.trends.TrendReq")
def test_check_trend_stable(mock_trendreq_cls):
    mock_pt = MagicMock()
    mock_trendreq_cls.return_value = mock_pt
    values = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    mock_pt.interest_over_time.return_value = _mock_interest_data("thingy", values)

    result = check_trend("thingy")
    assert result["keyword"] == "thingy"
    assert result["trend_direction"] == "stable"


@patch("ds.scout.trends.TrendReq")
def test_check_trend_no_data(mock_trendreq_cls):
    mock_pt = MagicMock()
    mock_trendreq_cls.return_value = mock_pt
    mock_pt.interest_over_time.return_value = pd.DataFrame()

    result = check_trend("nonexistent_xyz_abc")
    assert result["trend_direction"] == "no_data"
    assert result["avg_interest"] == 0


@patch("ds.scout.trends.TrendReq")
def test_check_trends_batch_mock(mock_trendreq_cls):
    mock_pt = MagicMock()
    mock_trendreq_cls.return_value = mock_pt

    def side_effect():
        # Return different data each call
        return _mock_interest_data("item", [50] * 12)

    mock_pt.interest_over_time.side_effect = [
        _mock_interest_data("bottle", [40] * 12),
        _mock_interest_data("case", [60] * 12),
    ]

    # check_trends_batch creates a new TrendReq per call, so we need to handle that
    mock_instances = [MagicMock(), MagicMock()]
    mock_instances[0].interest_over_time.return_value = _mock_interest_data("bottle", [40] * 12)
    mock_instances[1].interest_over_time.return_value = _mock_interest_data("case", [60] * 12)
    mock_trendreq_cls.side_effect = mock_instances

    results = check_trends_batch(["bottle", "case"])
    assert len(results) == 2
    assert results[0]["keyword"] == "bottle"
    assert results[1]["keyword"] == "case"
