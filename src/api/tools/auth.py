import requests
import json
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

chartnotes_token_url = os.getenv("CHARTNOTES_TOKEN_URL")
chartnotes_client_id =  os.getenv("CHARTNOTES_CLIENT_ID")
chartnotes_client_secret = os.getenv("CHARTNOTES_CLIENT_SECRET")
chartnotes_scope = os.getenv("CHARTNOTES_SCOPE")

def get_access_token():
    client = BackendApplicationClient(client_id=chartnotes_client_id)
    oauth = OAuth2Session(client=client)
   
    token = oauth.fetch_token(
        token_url = chartnotes_token_url,
        client_id=chartnotes_client_id,
        client_secret=chartnotes_client_secret,
        scope = chartnotes_scope
    )
    # print(token.get('access_token'))
    return token.get('access_token')
   