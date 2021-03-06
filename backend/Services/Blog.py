from flask import Flask,Blueprint,request,Response
from modules.Blog import Blog
from modules.User import User
from Contants import ServiceConstants,PetShareConstants
from Services import api_routes
from Services import api_routes_third_party
from Services import Authorizer
import requests
import json
import hashlib


blogsService = Blueprint("blogService",__name__)



@blogsService.route(api_routes.__BLOGS_CU,methods = ["POST","GET"])
def blogs_crud():
    response_object = {}
    
    blog = Blog()
    if request.method == "GET":
        #call blogs object
        blogs_list = blog.fetch_all_blogs()
        if "error" in blogs_list:
            response_object["error"] = blogs_list["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        return blogs_list
    elif request.method == "POST":
        access_token = request.headers['Authorization']
        # Authorizer
        auth_result = Authorizer.validate_token(access_token,fields=["id","name"])
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
    user = User()
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
        if "error" in single_blog or 'errorMessage' in single_blog:
            response_object["error"] = single_blog["error"]
            return response_object, ServiceConstants.__BAD_REQUEST
        created_by = single_blog["Blog"]["created_by"]
        search = {"id":created_by}
        user_details = user.get_node_details(search=search)
        popular_blogs = blog.fetch_popular_blogs()
        response_object["userDetails"] = user_details["result"]["node_properties"]
        response_object["data"] = single_blog
        response_object["popularBlogs"] = popular_blogs
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
        response_object["message"] = "Deleted"
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
    user_id = auth_result["id"]
    blog = Blog()
    add_a_cookie = blog.add_cookie(blog_id=blog_id,user_id=user_id)
    if "error" in add_a_cookie:
        response_object["error"] = add_a_cookie["error"]
        return response_object, ServiceConstants.__BAD_REQUEST
    response_object["result"] = add_a_cookie["result"]
    return response_object

@blogsService.route(api_routes.__TAGS,methods=["GET"])
def get_tags(type):
    response_object = {}
    if data == 'Blog':
        response_object["data"] = PetShareConstants.list_of_tags_blog
    return response_object