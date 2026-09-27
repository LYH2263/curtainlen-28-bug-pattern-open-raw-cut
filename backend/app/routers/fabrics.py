from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.repositories import fabrics as repo
router = APIRouter()

class PatternRepeatUpdate(BaseModel):
    # 布料默认花高（厘米）；只影响此后的试算，不回改已保存编号
    pattern_repeat_cm: float = Field(ge=0)

@router.get("/fabrics")
def list_fabrics(): return {"items": repo.list_fabrics()}
@router.get("/fabrics/{fid}")
def get_fabric(fid: int):
    r = repo.get_fabric(fid)
    if not r: raise HTTPException(404)
    return r
@router.patch("/fabrics/{fid}")
def patch_fabric(fid: int, body: PatternRepeatUpdate):
    r = repo.update_pattern_repeat(fid, body.pattern_repeat_cm)
    if not r: raise HTTPException(404)
    return r
