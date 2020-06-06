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

@blogsService.route(api_routes.__BLOGS_CRUD,methods = ["POST","GET"])
def blogs_crud():
    response_object = {}
    access_token = request.headers['Authorization']
    is_authorized,user_id = Authorizer.fb_authorizer(access_token)
    blog = Blog()
    if is_authorized == False:
        response_object["error"] = "Not authorized user"
        #:TODO: return status code
        return response_object
    if request.method == "GET":
        #call blogs object
        blogs_list = blog.fetch_all_blogs(user_id=user_id)
        if "error" in blogs_list:
            response_object["error"] = blogs_list["error"]
            return response_object
        response_object["data"] = blogs_list
        return response_object
    elif request.method == "POST":
        #Create new blog
        #create  new blog id
        image =  request.files.get('image')
        data = request.form.get("data")
        blog_created = blog.create_or_update_blog(user_id=user_id,image= image,data=data)
        if "error" in blog_created:
            response_object["error"] = blog_created["error"]
            return response_object
        return response_object
    
