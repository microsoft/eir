import requests
import json
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from diagnosis_auth import get_access_token
from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()

chartnotes_api_url = os.getenv("CHARTNOTES_API_URL")

@tool
def get_diagnosis_from_chartnotes(fileName: str, caseId: str) -> str:

    """Calls chartnotes API to fetch diagnosis data for the patient."""
    
    token = get_access_token()
    
    payload={}
    
    headers = {
    'x-upstream-env': 'dev',
    'Authorization': f'Bearer {token}'
    }
    
    url = f"{chartnotes_api_url}caseId={caseId}&fileName={fileName}&applicationName=PAS&access_token={token}"
    
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        chartnotes_res = response.json()
        diagnosis_json = chartnotes_res["MedicalNotes"]["llmExtraction"]["diagnoses"]
        return ({"diagnoses":diagnosis_json}, 200)
    else:
        print('Failed to access the API', response.status_code,response.text)
        return({"error": "Error in fetching chartnotes data."}, 500)

 

 

