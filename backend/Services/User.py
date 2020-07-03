from flask import Flask,Blueprint,request,Response
from Contants import ServiceConstants
from modules.User import User
from CommonUtils import Helper
import api_routes
import api_routes_third_party
import requests
import json
import bcrypt
import uuid
import Authorizer
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
    content["type"] = "fb-user"
    content["picture"] = content["picture"]["data"]["url"]
    tokens = Authorizer.generate_tokens(content)
    if "error" in tokens:
        response_object["error"] = tokens["error"]
        #:TODO: status code to be added
        return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
    status_code = response.status_code
    if status_code != ServiceConstants.__SUCCESS:
        response_object["error"] = {
            "message": content["error"]["message"],
            "code":content["error"]["code"]
        }
        return response_object,status_code
    user_id = content["id"]
    user = User()
    search = {"id":user_id}
    user_present = user.check_if_user_present_in_backend(search=search)
    if "error" in user_present:
        response_object["error"] = user_present["error"]
        return response_object, ServiceConstants.__BAD_REQUEST
    #create new user in backend
    user_created = user.create_or_update_user(content,user_id)
    if "error" in user_created:
        #:TODO: status code to be added
        response_object["error"] = user_created["error"]
        return response_object, ServiceConstants.__BAD_REQUEST
    tokens = tokens["tokens"]
    response_object["data"] = content
    response_object["access_token"] = tokens["access_token"]
    response_object["refresh_token"] = tokens["refresh_token"]
    return response_object

@userService.route("/",methods = ["GET"])
def landing():
    print("here")
    return "Welcome to petshare india!"   

@userService.route(api_routes.__SIGNUP_USER,methods = ["POST"])
def create_a_user():
    response_object = {}
    user = User()
    try:
        user_id = uuid.uuid4().hex
        data = request.json
        data["type"] = "custom-user"
        data["id"] = user_id
        email = data["email"]
        search = {"email":email}
        if_email_is_present = user.check_if_user_present_in_backend(search=search)
        print(if_email_is_present)
        if "error" in if_email_is_present:
            response_object["error"]= if_email_is_present["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        if 'errorMessage' not in if_email_is_present:
            response_object["error"] = "User already present"
            return response_object, ServiceConstants.__BAD_REQUEST
        tokens = Authorizer.generate_tokens(data)
        if "error" in tokens:
            response_object["error"] = tokens["error"]
            #:TODO: status code to be added
            return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
        tokens = tokens["tokens"]
        password = data["password"]
        saltandHasofpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        data["password"] = saltandHasofpass
        user_created = user.create_or_update_user(data,user_id)
        if "error" in user_created:
            response_object["error"] = property_string["error"]
            #:TODO: status code to be added
            return response_object, ServiceConstants.__BAD_REQUEST
        response_object["data"] = data
        response_object["access_token"] = tokens["access_token"]
        response_object["refresh_token"] = tokens["refresh_token"]
        return response_object
    except Exception as err:
        response_object["error"] = str(err)
        return response_object

@userService.route(api_routes.__LOGIN_USER,methods = ["POST"])
def login_a_user():
    response_object = {}
    user =User()
    try:
        data = request.json
        email = data["email"]
        password = data["password"]
        search = {"email":email}
        if_user_present = user.check_if_user_present_in_backend(search=search)
        if "error" in if_user_present or 'errorMessage' in if_user_present:
            response_object["error"]= if_user_present["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        user_details = if_user_present["node_properties"]
        hashAndSalt = user_details["password"]
        valid = bcrypt.checkpw(password.encode('utf-8'), hashAndSalt.encode('utf-8'))
        if valid is False:
            response_object["error"] = "Password incorrect. Please re enter"
            return response_object, ServiceConstants.__BAD_REQUEST
        tokens = Authorizer.generate_tokens(data)
        if "error" in tokens:
            response_object["error"] = tokens["error"]
            #:TODO: status code to be added
            return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
        tokens = tokens["tokens"]
        response_object["data"] = user_details
        response_object["access_token"] = tokens["access_token"]
        response_object["refresh_token"] = tokens["refresh_token"]
        return response_object
    except Exception as err:
        response_object["error"] = str(err)
        return response_object

@userService.route(api_routes.__USER_BLOGS,methods = ["GET"])
def fetch_user_blogs():
    response_object = {}
    user = User()
    access_token = request.headers['Authorization']

    # Authorizer.
    auth_result = Authorizer.validate_token(access_token,fields=["id"])
    user_id = auth_result["id"]
    if 'error' in auth_result:
        response_object["error"] = str(auth_result["error"])
        #:TODO: return status code
        return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
    blogs = user.fetch_user_blogs(user_id)
    data = []
    for item in blogs["data"]:
        data.append(item["blogs"])
    response_object["data"] = data
    return response_object


@userService.route(api_routes.__TOKEN_VALIDITY,methods = ["GET"])
def is_token_valid():
    response_object = {}
    access_token = request.args.get('access_token')
    # Authorizer.
    auth_result = Authorizer.validate_token(access_token,fields=["id","name","picture"])
    if 'error' in auth_result:
        response_object["error"] = str(auth_result["error"])
        response_object["is_valid"] = False
        #:TODO: return status code
        return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
    #:TODO: sending access token for now. to be removed
    response_object["data"] = auth_result
    response_object["is_valid"] = True
    response_object["access_token"] = access_token
    return response_object

