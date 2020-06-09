from flask import Flask,Blueprint,request,Response
from modules.Blog import Blog
from CommonUtils import helper
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
            return response_object
        data = []
        for item in blogs_list:
            data.append(item["node"])
        response_object["data"] = data
        return response_object
    elif request.method == "POST":
        access_token = request.headers['Authorization']
        is_authorized,user_id = Authorizer.fb_authorizer(access_token)
        if user_id is None:
            response_object["error"] = "Please sign up"
            #:TODO: return status code
            return response_object
        if is_authorized == False:
            response_object["error"] = "Not authorized user"
            #:TODO: return status code
            return response_object
        #Create new blog
        #create  new blog id
        image =  request.files.get('image')
        if image == None:
            print("No image found")
        data = request.form.get("data")
        blog_created = blog.create_or_update_blog(user_id=user_id,image= image,data=data)
        if "error" in blog_created:
            response_object["error"] = blog_created["error"]
            return response_object
        return response_object
    

@blogsService.route(api_routes.__BLOG,methods = ["DELETE","GET"])
def blogs(blog_id):
    response_object = {}
    access_token = request.headers['Authorization']
    is_authorized,user_id = Authorizer.fb_authorizer(access_token)
    blog = Blog()
    if user_id is None:
        response_object["error"] = "Please sign up"
        #:TODO: return status code
        return response_object
    if is_authorized == False:
        response_object["error"] = "Not authorized user"
        #:TODO: return status code
        return response_object
    if request.method == "GET":
        #call blogs object
        blog = blog.fetch_blog(user_id="user_id",blog_id=blog_id)
        if "error" in blog:
            response_object["error"] = blog["error"]
            return response_object
        response_object["data"] = blog[0]["node"]
        return response_object
    elif request.method == "DELETE":
        print("Deleting")
        #Delete blog
        print(user_id)
        print(blog_id)
        blog_deleted = blog.delete_a_blog(user_id,blog_id)
        if "error" in blog_deleted:
            response_object["error"] = blog_deleted["error"]
            return response_object
        response_object["message"] = blog_created["message"]
        return response_object


@blogsService.route(api_routes.__ADD_IMAGE,methods = ["POST"])
def add_image():
    response_object = {}
    access_token = request.headers['Authorization']
    is_authorized,user_id = Authorizer.fb_authorizer(access_token)
    blog = Blog()
    if user_id is None:
        response_object["error"] = "Please sign up"
        #:TODO: return status code
        return response_object
    if is_authorized == False:
        response_object["error"] = "Not authorized user"
        #:TODO: return status code
        return response_object
    if request.method == "POST":
        image =  request.files.get('image')
        data = request.form.get("data")
        image_added = blog.add_a_public_image(image= image)
        if "error" in image_added:
            response_object["error"] = image_added["error"]
            return response_object
        response_object["result"] = image_added["result"]
        return response_object
    
