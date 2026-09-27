import pytest
from app.engines.curtain_math import fabric_meters

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_zero_repeat_keeps_legacy_behavior():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0)
    assert r["gross_cut_height"] == 2.85
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25
    assert r["pattern_repeat_cm"] == 0

def test_positive_repeat_rounds_up():
    # 毛裁高 2.85m；花高 64cm：2.85/0.64=4.45… 向上取 5 跳 → 3.20m
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 64)
    assert r["gross_cut_height"] == 2.85
    assert r["cut_height"] == 3.2
    assert r["panels"] == 5
    assert r["meters"] == 16.0
    assert r["pattern_repeat_cm"] == 64

def test_exact_multiple_adds_no_extra_repeat():
    # 2.85 / 0.95 恰好 3 跳，不应再多对齐一跳
    r = fabric_meters(1.0, 2.6, 2.0, 0.10, 0.15, 2.8, 95)
    assert r["gross_cut_height"] == 2.85
    assert r["cut_height"] == 2.85

def test_tiny_gross_height_still_one_repeat():
    # 毛裁高小于一个花高也要给到 1 跳
    r = fabric_meters(1.0, 0.3, 1.0, 0.0, 0.0, 2.8, 100)
    assert r["gross_cut_height"] == 0.3
    assert r["cut_height"] == 1.0

def test_negative_repeat_rejected():
    with pytest.raises(ValueError):
        fabric_meters(1.0, 2.0, 2.0, 0.1, 0.1, 1.4, -1)
