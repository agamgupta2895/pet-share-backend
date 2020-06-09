import requests
import api_routes_third_party
import json
from Contants import ServiceConstants
from User import User

def fb_authorizer(access_token):
    response_object = {}
    params = {
        "access_token" : access_token
    }
    url = api_routes_third_party.__FETCH_USER_DATA_FB
    response = requests.get(url = url,params=params)
    content = json.loads(response.content)
    status_code = response.status_code
    user = User()
    if status_code != ServiceConstants.__SUCCESS:
        return False,""
    user_present = user.check_if_user_id_present_in_backend(user_id=content["id"])
    if user_present["result"] == False:
        return False, None
    response_object["user_id"] = content["id"]

    return True,content["id"]