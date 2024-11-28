#importing libraries
import os
from dotenv import load_dotenv
import datetime
import json
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
# from auth import get_access_token
from langchain.agents import tool

from langchain_core.tools import tool as original_tool

load_dotenv()

chartnotes_api_url = os.getenv("CHARTNOTES_API_URL")


def tool(func):
    func = original_tool(func)
    func._is_tool = True
    return func

def get_chartnotes(fileName: str, caseId: str) -> str:
 
    """Calls chartnotes API to fetch diagnosis data for the patient."""
   
    # token = get_access_token()
    token = "123"
   
    payload={}
   
    headers = {
    'x-upstream-env': 'dev',
    'Authorization': f'Bearer {token}'
    }
   
    url = f"{chartnotes_api_url}caseId={caseId}&fileName={fileName}&applicationName=PAS&access_token={token}"
   
    response = requests.request("GET", url, headers=headers, data=payload)
 
    if response.status_code == 200:
        chartnotes_res = response.json()
        lab_data = chartnotes_res['MedicalNotes']['llmExtraction']['labResults']

        return ({"labResults":lab_data}, 200)
    else:
        print('Failed to access the API', response.status_code,response.text)
        return({"error": "Error in fetching chartnotes data."}, 500)
 
@tool
def get_observation_data(case_data):
    """Extracts the lab observation data from the case data."""
    ECDH_data= case_data['ECDHDetails']['Observation']

    if ECDH_data:
        response = {"ECDH_details": ECDH_data}
        return(response)
    
    else:
        fileName = case_data["fileName"]
        caseId = case_data["CaseId"]
        response =get_chartnotes(fileName, caseId)
        return(response)

# with open('SampleRequestFormatFromPAS_Updated.json','r') as file:
#     request_data = json.load(file)
# ans = get_observation_data(request_data)
# print(ans)