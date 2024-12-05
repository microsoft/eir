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
(2) get_patient_data[input]: Worker that searches for demographic patient data. Useful when looking up things like date of birth. 
(3) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general world knowledge and common sense. Prioritize it when you are confident in solving the problem yourself. Input can be any instruction. 

For example,
Task: Find the nationality of the goalie of the UEFA Champions League Champions in 2023. 
Plan: Look up the winner team of the UEFA Champions League in 2023.#E1=TeamData[Winner UEFA Champions League 2023]
Plan: Look up the goalie of the team in 2023.#E2=TeamMemberData[Name of the Goalie in team #E1]
Plan: Look up the nationality of the goalie.#E3=SoccerPlayerData[Nationality of the player #E2]

Begin! 
Describe your plans with rich details. Each Plan should be followed by only one #E. Do not include any additional commentary or modify the format of the plan.

Rule: {rule}"""

def get_validation_plan(rule: str) -> str:    
    result = model.invoke(prompt.format(rule=rule))
    
    return result.content
