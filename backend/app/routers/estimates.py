from typing import Optional
from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(
    window_id: int = Query(...),
    fabric_id: int = Query(...),
    save: bool = False,
    pattern_repeat_cm: Optional[float] = Query(default=None, ge=0),
):
    return estimate_service.run_estimate(window_id, fabric_id, save, "", pattern_repeat_cm)
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.window_id, body.fabric_id, body.save, body.note, body.pattern_repeat_cm
    )
