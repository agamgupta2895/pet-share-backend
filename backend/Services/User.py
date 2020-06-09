from flask import Flask,Blueprint,request,Response
from Contants import ServiceConstants
from modules.User import User
from CommonUtils import helper
import api_routes
import api_routes_third_party
import requests
import json
userService = Blueprint("userService",__name__)

@userService.route(api_routes.__LOGIN_USER_FB,methods = ["GET"])
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
    user_id = content["id"]
    user = User()
    user_present = user.check_if_user_id_present_in_backend(user_id=user_id)
    if "error" in user_present:
        response_object["error"] = user_present["error"]
        return response_object
    #create new user in backend
    property_string = helper.create_property_string("user",content)
    if "error" in property_string:
        print("not present")
        response_object["error"] = property_string["error"]
        #:TODO: status code to be added
        return response_object
    user_created = user.create_or_update_user(property_string["properties"][:-2],user_id)
    if "error" in user_created:
        #:TODO: status code to be added
        response_object["error"] = user_created["error"]
        return response_object
    if (user_present["result"] == False):     
        response_object["user_type"] = "new_user"
    else:
        #User already present in backend. But properties could have changed
        response_object["user_type"] = "existing_user"
    response_object["data"] = content
    return response_object

@userService.route("/",methods = ["GET"])
def landing():
    print("here")
    return "Hello World!"   