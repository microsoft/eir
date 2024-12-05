from pydantic import BaseModel

# OpenTelemetry Integration
### 
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from dotenv import load_dotenv
# load_dotenv('azure.env')
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter.from_connection_string(
    os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)


tracer_provider = TracerProvider()
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
trace_api.set_tracer_provider(tracer_provider)
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter, schedule_delay_millis=60000)
trace.get_tracer_provider().add_span_processor(span_processor)
LangChainInstrumentor().instrument()

###


from .agents.planner import get_validation_plan
from .agents.executor import run_plan
from .tools.drug_rules import fetch_drug_rules

import fastapi
from fastapi.staticfiles import StaticFiles


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

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