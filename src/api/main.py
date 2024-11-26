
from pydantic import BaseModel

#from .tools.patient_data import get_patient_data, get_patient_notes
from .agents.planner import get_validation_plan
from .agents.executor import run_plan
from .tools.drug_rules import fetch_drug_rules

import fastapi

app = fastapi.FastAPI()

class plan_request(BaseModel):
    drug: str
    rules: str

class ExecutePlanRequest(BaseModel):
    task: str
    plan: str

@app.post("/generate_plan")
async def generate_plan(request: plan_request):
    result = get_validation_plan(request.rules)
    return result

# @app.get("/get_plan")
# async def get_plan(drug: str):
#     return {"plan": f"Take 1 pill of {drug} every 4 hours"}

@app.get("/get_rules")
async def get_rules(drug:str):
    result = fetch_drug_rules(drug)
    return result

@app.post("/execute_plan")
async def execute_plan(request: ExecutePlanRequest):
    # Get the plan from the body (JSON) in the POST request and execute it
    result = run_plan(request.task, request.plan)
    return result