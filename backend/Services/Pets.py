from flask import Flask,Blueprint,request,Response
from modules.Pet import Pet
from Contants import ServiceConstants,PetShareConstants
from Services import api_routes
from Services import api_routes_third_party
from Services import Authorizer
import requests
import json
import hashlib

petsService = Blueprint("petsService",__name__)



@petsService.route(api_routes.__PETS_CU,methods = ["POST","GET"])
def pets_cu():
    response_object = {}
    
    pet = Pet()
    if request.method == "GET":
        #call pets object
        pet_list = pet.fetch_all_pets()
        if "error" in pet_list:
            response_object["error"] = pet_list["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        return pet_list
        
    elif request.method == "POST":
        access_token = request.headers['Authorization']
        auth_result = Authorizer.validate_token(access_token,fields=["id","name"])
        print(auth_result)
        if 'error' in auth_result:
            response_object["error"] = str(auth_result["error"])
            #:TODO: return status code
            return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
        images =  request.files.getlist('images')
        data = request.form.get("data")
        user_id = auth_result["id"]
        data = data.encode('ascii','ignore')
        data = json.loads(data)
        data["author"] = auth_result["name"]
        pet_profile_created = pet.create_or_update_pet_profile(user_id=user_id,images= images,data=data)
        if "error" in pet_profile_created:
            response_object["error"] = pet_profile_created["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        return response_object
    
@petsService.route(api_routes.__PETS_TYPE_DETAILS,methods = ["GET"])
def pet_constants():
    response_object = {}
    response_object["data"] = PetShareConstants.list_of_pets_and_breeds
    return response_object