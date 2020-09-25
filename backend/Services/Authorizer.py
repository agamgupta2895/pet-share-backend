import requests
from Services import api_routes_third_party
import json
from Contants import ServiceConstants
from User import User
import jwt
import datetime



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

def generate_tokens(data):
    response = {
        "tokens":{}
    }
    try:
        access_token = jwt.encode(
                            {
                                'data': data,
                                'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=2),
                            }, 'pet-share-india', algorithm='HS256')
        refresh_token = jwt.encode(
                        {
                            'data': data,
                            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7),
                        }, 'pet-share-india', algorithm='HS256')
        response["tokens"]["access_token"] = access_token
        response["tokens"]["refresh_token"] = refresh_token
        return response
    except Exception as err:
        response["error"] = str(err)
        return response

def validate_token(access_token,fields=None):
    response = {}
    try:
        try:
            decoded_jwt = jwt.decode(access_token, 'pet-share-india', algorithms=['HS256'])
        except Exception as err:
            response["error"] = "Invalid token provided" 
            return response
        for item in fields:
            if item in decoded_jwt["data"]:
                response[item] = decoded_jwt["data"][item]
        return response
    except Exception as err:
        response["error"] = str(err)