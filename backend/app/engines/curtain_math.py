from app.engines.helpers import ceil_units


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
    pattern_repeat_cm: float = 0.0,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    pattern_repeat_cm = float(pattern_repeat_cm or 0.0)
    if pattern_repeat_cm < 0:
        raise ValueError("pattern repeat must be >= 0")
    finished_w = float(window_w) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    # 毛裁高：层高 + 上下折边
    gross_h = float(window_h) + float(hem_top) + float(hem_bottom)
    if pattern_repeat_cm > 0:
        # 向上对齐到花高（米）的整数倍
        repeat_m = pattern_repeat_cm / 100.0
        repeats = max(1, ceil_units(gross_h / repeat_m))
        cut_h = repeats * repeat_m
    else:
        cut_h = gross_h
    meters = panels * cut_h
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "gross_cut_height": round(gross_h, 3),
        "pattern_repeat_cm": round(pattern_repeat_cm, 3),
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
    }
