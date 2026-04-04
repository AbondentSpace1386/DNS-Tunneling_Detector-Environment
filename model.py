from pydantic import BaseModel, Field
from typing import List,Optional

class State(BaseModel):
    features: List[float]=Field(...,min_item=4,max_item=4,description="Fratures vector:[domain_length,request_frequency,entropy,query_type_encoded]"
                                )
class Action(BaseModel):
    action: int=Field(..., ge=0 ,le=2,description= "0=Allow,1=block")
class StepResponse(BaseModel):
    state: State
    reward: float=Field(...,ge=0.0,le=1.0)
    done: bool
class ResetRequest(BaseModel):
    task: Optional[str]='Easy Detection'
class ResetResponse(BaseModel):
    state: State