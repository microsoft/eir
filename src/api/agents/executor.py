import os
import re

from langgraph.graph import END, StateGraph, START
from langchain_openai import AzureChatOpenAI

from ..tools import patient_data
from ..models.state import ReWOO

model = AzureChatOpenAI(model=os.environ["OPENAI_MODEL_NAME"], 
                        api_version=os.environ["OPENAI_API_VERSION"], 
                        base_url=os.environ["OPENAI_API_BASE_URL"])


plan_string=""

def _get_current_task(state: ReWOO):
    if "results" not in state or state["results"] is None:
        return 1
    if len(state["results"]) == len(state["steps"]):
        return None
    else:
        return len(state["results"]) + 1



def get_plan(state: ReWOO, config):
    # Regex to match expressions of the form E#... = ...[...]
    regex_pattern = r"Plan:\s*(.+)\s*(#E\d+)\s*=\s*(\w+)\s*\[([^\]]+)\]"

    result = config["metadata"]["plan"]
    
    # Find all matches in the sample text
    matches = re.findall(regex_pattern, result)
    return {"steps": matches, "plan_string": result}




def tool_execution(state: ReWOO):
    """Worker node that executes the tools of a given plan."""
    _step = _get_current_task(state)
    _, step_name, tool, tool_input = state["steps"][_step - 1]
    _results = (state["results"] or {}) if "results" in state else {}
    for k, v in _results.items():
        tool_input = tool_input.replace(k, v)
    if tool == "ChartNotes":
        result = patient_data.get_patient_notes(tool_input)
    elif tool == "PatientData":
        result = patient_data.get_patient_data(tool_input)
    elif tool == "LLM":
        result = model.invoke(tool_input)
    else:
        raise ValueError
    _results[step_name] = str(result)
    return {"results": _results}

def _route(state):
    _step = _get_current_task(state)
    if _step is None:
        # We have executed all tasks
        return "solve"
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "tool"
    

task = "Is the patient with id 1234 eligible for the Ozempic drug?"
solve_prompt = """Solve the following task or problem. To solve the problem, we have made step-by-step Plan and \
retrieved corresponding Evidence to each Plan. Use them with caution since long evidence might \
contain irrelevant information.

{plan}

Now solve the question or task according to provided Evidence above. Respond with the answer
directly with no extra words.

Task: {task}
Response:"""

def solve(state: ReWOO):
    plan = ""
    for _plan, step_name, tool, tool_input in state["steps"]:
        _results = (state["results"] or {}) if "results" in state else {}
        for k, v in _results.items():
            tool_input = tool_input.replace(k, v)
            step_name = step_name.replace(k, v)
        plan += f"Plan: {_plan}\n{step_name} = {tool}[{tool_input}]"
    prompt = solve_prompt.format(plan=plan, task=state["task"])
    result = model.invoke(prompt)
        
    return {"result": result.content}


def run_plan(plan_string: str):
    config = {"plan": plan_string}

    graph = StateGraph(ReWOO)
   
    graph.add_node("plan", get_plan, metadata=config)    
    graph.add_node("tool", tool_execution)
    graph.add_node("solve", solve)
    graph.add_edge("plan", "tool")
    graph.add_edge("solve", END)
    graph.add_conditional_edges("tool", _route)
    graph.add_edge(START, "plan")
    
    app = graph.compile()
    result = app.invoke({"task": task})

    return result

