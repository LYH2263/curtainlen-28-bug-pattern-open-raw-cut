from typing import Optional
from pydantic import BaseModel, Field

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    # 当次试算花高（厘米）；None 表示用布料默认花高。负数在接口层 422。
    pattern_repeat_cm: Optional[float] = Field(default=None, ge=0)
