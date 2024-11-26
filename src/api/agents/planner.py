import os

from langchain_openai import AzureChatOpenAI

# from models import state as ReWOO

model = AzureChatOpenAI(model=os.environ["OPENAI_MODEL_NAME"], 
                        api_version=os.environ["OPENAI_API_VERSION"], 
                        base_url=os.environ["OPENAI_API_BASE_URL"])

prompt = """For the following rule, make plans that can validate a patient meets the criteria defined by the rule. For each plan, indicate \
which external tool together with tool input to retrieve evidence. You can store the evidence into a \
variable #E that can be called by later tools. (Plan, #E1, Plan, #E2, Plan, ...)

Tools can be one of the following:
(1) get_patient_notes[input]: Worker that searches for patient visit notes. Useful when you need to confirm a diagnosis or treatment.
(2) get_patient_data[input]: Worker that searches for specific patient data. Useful when looking up patient data.
(2) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general
world knowledge and common sense. Prioritize it when you are confident in solving the problem
yourself. Input can be any instruction.

For example,
Rule: The outside air temperature must be below 32 degrees Fahrenheit in order for it to be snowing.
Plan: Look up the outside air temperature. #E1 = WeatherData[lookup outside air temperature]

Begin! 
Describe your plans with rich details. Each Plan should be followed by only one #E.

Rule: {rule}"""

def get_validation_plan(rule: str) -> str:    
    result = model.invoke(prompt.format(rule=rule))
    
    return result.content
