
from pydantic import BaseModel

#from .tools.patient_data import get_patient_data, get_patient_notes
from .agents.planner import get_validation_plan

import fastapi

app = fastapi.FastAPI()

class plan_request(BaseModel):
    drug: str
    rules: str

@app.post("/generate_plan")
async def generate_plan(request: plan_request):
    result = get_validation_plan(request.rules)
    return result

# @app.get("/get_plan")
# async def get_plan(drug: str):
#     return {"plan": f"Take 1 pill of {drug} every 4 hours"}
