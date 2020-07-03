from flask import Flask,Blueprint,request,Response
from modules.Pet import Pet
from CommonUtils import helper
from Contants import ServiceConstants,PetConstants
import api_routes
import api_routes_third_party
import requests
import json
import Authorizer
import hashlib

petsService = Blueprint("petsService",__name__)



@petsService.route(api_routes.__PETS_CU,methods = ["POST","GET"])
def pets_cu():
    response_object = {}
    
    pet = Pet()
    if request.method == "GET":
        #call blogs object
        pass
        
    elif request.method == "POST":
        access_token = request.headers['Authorization']
        # Authorizer.
        auth_result = Authorizer.validate_token(access_token,fields=["id"])
        if 'error' in auth_result:
            response_object["error"] = str(auth_result["error"])
            #:TODO: return status code
            return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
        user_id = auth_result["id"]
        print(user_id)
        images =  request.files.getlist('images')
        print(images)
        data = request.form.get("data")
        pet_profile_created = pet.create_or_update_pet_profile(user_id=user_id,images= images,data=data)
        if "error" in pet_profile_created:
            response_object["error"] = pet_profile_created["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        return response_object
    
@petsService.route(api_routes.__PETS_TYPE_DETAILS,methods = ["GET"])
def pet_constants():
    response_object = {}
    response_object["data"] = PetConstants.list_of_pets_and_breeds
    return response_object