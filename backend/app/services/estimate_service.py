from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str, pattern_repeat_cm: float | None = None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    # 未显式给花高时用布料默认花高；当次值随结果一并固化进 calc_runs
    pr_cm = float(f.get("pattern_repeat_cm") or 0.0) if pattern_repeat_cm is None else float(pattern_repeat_cm)
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"], pr_cm)
    run_id = history.insert_run(window_id, fabric_id, calc, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **calc}
