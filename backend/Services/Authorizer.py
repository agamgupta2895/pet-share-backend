import requests
import api_routes_third_party
import json
from Contants import ServiceConstants

def fb_authorizer(access_token):
    response_object = {}
    params = {
        "access_token" : access_token
    }
    url = api_routes_third_party.__FETCH_USER_DATA_FB
    response = requests.get(url = url,params=params)
    content = json.loads(response.content)
    status_code = response.status_code
    if status_code != ServiceConstants.__SUCCESS:
        return False,""
    response_object["user_id"] = content["id"]

    return True,content["id"]