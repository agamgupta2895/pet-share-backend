from flask import Flask,Blueprint,request,Response
from Contants import ServiceConstants
import api_routes
import api_routes_third_party
import requests
import json
userService = Blueprint("userService",__name__)

@userService.route(api_routes.__FETCH_USER_DATA_FB,methods = ["GET"])
def fetch_user_details_fb():
    response_object = {}
    access_token = request.args.get('access_token')
    user_data_fields = ServiceConstants.__USER_DATA_FIELDS_FB
    params = {
        "access_token" : access_token,
        "fields" : user_data_fields
    }
    url = api_routes_third_party.__FETCH_USER_DATA_FB
    response = requests.get(url = url,params=params)
    content = json.loads(response.content)
    status_code = response.status_code
    if status_code != ServiceConstants.__SUCCESS:
        response_object["error"] = {
            "message": content["error"]["message"],
            "code":content["error"]["code"]
        }
        return response_object,status_code
    response_object["data"] = content
    return response_object

@userService.route("/",methods = ["GET"])
def landing():
    print("here")
    return "Hello World!"
