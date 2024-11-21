import random

from pydantic import BaseModel
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

import fastapi

from .data import names

app = fastapi.FastAPI()

class plan_request(BaseModel):
    drug: str
    rules: list

@app.get("/generate_name")
async def generate_name(starts_with: str = None):
    name_choices = names
    if starts_with:
        name_choices = [name for name in name_choices if name.lower().startswith(starts_with.lower())]
    random_name = random.choice(name_choices)
    return {"name": random_name}

@app.post("/generate_plan")
async def generate_plan(request: plan_request):
    return {"plan": f"Take 1 of {request.drug} pill every 4 hours", "rules": request.rules}

@app.get("/get_plan")
async def get_plan(drug: str):
    return {"plan": f"Take 1 pill of {drug} every 4 hours"}
