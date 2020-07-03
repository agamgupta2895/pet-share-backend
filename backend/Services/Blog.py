from flask import Flask,Blueprint,request,Response
from modules.Blog import Blog
from CommonUtils import helper
from Contants import ServiceConstants
import api_routes
import api_routes_third_party
import requests
import json
import Authorizer
import hashlib

blogsService = Blueprint("blogService",__name__)



@blogsService.route(api_routes.__BLOGS_CU,methods = ["POST","GET"])
def blogs_crud():
    response_object = {}
    
    blog = Blog()
    if request.method == "GET":
        #call blogs object
        blogs_list = blog.fetch_all_blogs(user_id="user_id")
        if "error" in blogs_list:
            response_object["error"] = blogs_list["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        data = []
        for item in blogs_list:
            data.append(item["node"])
        response_object["data"] = data
        return response_object
    elif request.method == "POST":
        access_token = request.headers['Authorization']
        # Authorizer.
        auth_result = Authorizer.validate_token(access_token,fields=["id"])
        if 'error' in auth_result:
            response_object["error"] = str(auth_result["error"])
            #:TODO: return status code
            return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
        #Create new blog
        #create  new blog id
        images =  request.files.getlist('images')
        data = request.form.get("data")
        user_id = auth_result["id"]
        blog_created = blog.create_or_update_blog(user_id=user_id,images= images,data=data)
        if "error" in blog_created:
            response_object["error"] = blog_created["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        return response_object
    

@blogsService.route(api_routes.__BLOG,methods = ["DELETE","GET"])
def blogs(blog_id):
    response_object = {}
    user_id = ''
    blog = Blog()
    if request.method == "GET":
        #call blogs object
        if 'Authorization' in request.headers:
            access_token = request.headers['Authorization']
            auth_result = Authorizer.validate_token(access_token,fields=["id"])
            if 'error' in auth_result:
                response_object["error"] = str(auth_result["error"])
                #:TODO: return status code
                return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
            user_id = auth_result["id"]
        single_blog = blog.fetch_blog(user_id=user_id,blog_id=blog_id)
        if "error" in single_blog:
            response_object["error"] = single_blog["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        created_by = single_blog["Blog"]["created_by"]
        user_details = helper.get_user_details(user_id=created_by)
        popular_blogs = blog.fetch_popular_blogs()
        response_object["user_details"] = user_details["data"]
        print(response_object["user_details"])
        response_object["data"] = single_blog
        response_object["popular_blogs"] = popular_blogs["result"]
        return response_object
    elif request.method == "DELETE":
        #Delete blog
        access_token = request.headers['Authorization']
        auth_result = Authorizer.validate_token(access_token,fields=["id"])
        if 'error' in auth_result:
            response_object["error"] = str(auth_result["error"])
            #:TODO: return status code
            return response_object, ServiceConstants.__INVALID_ACCESS_TOKEN
        user_id = auth_result["id"]
        blog_deleted = blog.delete_a_blog(user_id,blog_id)
        if "error" in blog_deleted:
            response_object["error"] = blog_deleted["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        response_object["message"] = blog_deleted["message"]
        return response_object


@blogsService.route(api_routes.__ADD_IMAGE,methods = ["POST"])
def add_image():
    response_object = {}
    access_token = request.headers['Authorization']
    auth_result = Authorizer.validate_token(access_token,fields=["id"])
    if 'error' in auth_result:
        response_object["error"] = str(auth_result["error"])
        #:TODO: return status code
        return response_object
    blog = Blog()
    image =  request.files.get('image')
    data = request.form.get("data")
    image_added = blog.add_a_public_image(image= image)
    if "error" in image_added:
        response_object["error"] = image_added["error"]
        return response_object, ServiceConstants.__BAD_REQUEST
    response_object["result"] = image_added["result"]
    return response_object

@blogsService.route(api_routes.__ADD_COOKIE,methods=["POST"])
def add_cookie(blog_id):
    response_object = {}
    access_token = request.headers['Authorization']
    auth_result = Authorizer.validate_token(access_token,fields=["id"])
    if 'error' in auth_result:
        response_object["error"] = str(auth_result["error"])
        #:TODO: return status code
        return response_object
    blog = Blog()
    add_a_cookie = blog.add_cookie(blog_id)
    if "error" in add_a_cookie:
        response_object["error"] = add_a_cookie["error"]
        return response_object, ServiceConstants.__BAD_REQUEST
    response_object["result"] = add_a_cookie["result"]
    return response_object