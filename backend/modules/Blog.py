from py2neo import Graph,Node,Relationship
import uuid
from Contants import ServiceConstants
import boto3
import json
from CommonUtils.Helper import Helper
class Blog:
    def __init__(self):
        self.client = boto3.client('s3')
        self.s3_base_url = "https://pet-share-india.s3.ap-south-1.amazonaws.com/"

    def fetch_all_blogs(self):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        helper = Helper()
        labels = ["Blog"]
        try:
            blogs = helper.find_nodes_in_db(labels=labels)
            if 'error' in blogs:
                return blogs
            response["data"] = blogs
            return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def fetch_blog(self,user_id,blog_id):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        helper = Helper()
        labels = ["Blog"]
        search = {"id":blog_id}
        try:
            blog = helper.find_single_node_in_db(labels = labels,search=search)
            print(blog)
            if 'error' in blog:
                response["error"] = blog["error"]
                return response
            if 'errorMessage' in blog:
                response["error"] = blog["errorMessage"]
                return response
            blog = blog["node_properties"]
            if user_id == blog["created_by"]:
                blog["is_owner"] = True
            else:
                blog["is_owner"] = False
            response["Blog"] = blog
            return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def add_a_public_image(self,image):
        """"
        """
        response = {}
        try:
            image_id = uuid.uuid4().hex
            image_path = "blogs/public/"+str(image_id)+"/blog_image.jpg"
            bucket_name = 'pet-share-india'
            response = self.client.put_object(
                    ACL = 'public-read',
                    Bucket = bucket_name,
                    Key= image_path,
                    Body = image,
                    ContentType = 'image/png'
                )
            
            s3_base_url = "https://pet-share-india.s3.ap-south-1.amazonaws.com/"
            response["result"] = s3_base_url + image_path
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
    def create_or_update_blog(self,user_id,images,data):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        helper = Helper()

        try:
            data = data.encode('ascii','ignore')
            data = json.loads(data)
            data["created_by"] = user_id
            if "id" in data:
                blog_id = data["id"]
            else:
                blog_id = uuid.uuid4().hex
                data["id"]= blog_id
            search = {"id":data["id"]}
            if images is not None:
                images_paths = []
                for image in images:
                    print(images)
                    image_id = str(uuid.uuid4().hex)
                    image_path = "blogs/"+str(blog_id)+"/"+image_id+".jpg"
                    bucket_name = 'pet-share-india'
                    response = self.client.put_object(
                            ACL = 'public-read',
                            Bucket = bucket_name,
                            Key= image_path,
                            Body = image,
                            ContentType = 'image/png'
                        )
                    images_paths.append(self.s3_base_url+image_path)
                data["image_url"] = images_paths
            labels = ["Blog"]
            blog_node = helper.create_a_new_node(labels =labels,
                                                properties = data,
                                                search=search)
            if 'error' in blog_node:
                response["error"] = blog_node["error"]
                return response
            src = {
                "labels" :["User"],
                "search":{"id":user_id}
            }
            tgt = {
                "labels" :["Blog"],
                "search" : {"id":blog_id}
            }
            relationship  = helper.create_a_relationship(src=src,tgt=tgt,rel="CREATED")                 
            if 'error' in relationship:
                response["error"] = relationship["error"]
            return response
            
        except Exception as err:
            response["error"] = str(err)
            return response
    def delete_a_blog(self,user_id,blog_id):
        """
        """
        response = {}
        helper = Helper()
        labels = ["Blog"]
        search = {"id":blog_id}
        try:

            deleted_entity = helper.delete_single_node_in_db(labels=labels,search=search)
            if 'error' in deleted_entity:
                response["error"] = deleted_entity["error"]
                return response
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('pet-share-india')
            bucket.objects.filter(Prefix="pet-share-india/blogs/"+blog_id).delete()
            response["result"] = "Deleted successfully"
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
    def add_cookie(self,blog_id,user_id):
        """
        """
        response = {}
        helper = Helper()
        src = {
                "labels" :["User"],
                "search":{"id":user_id}
            }
        tgt = {
            "labels" :["Blog"],
            "search" : {"id":blog_id}
        }
        
        try:
            can_user_add_cookie = helper.fetch_a_relationship(src=src,tgt=tgt,rel="SENT")
            print(can_user_add_cookie)
            if 'error' in can_user_add_cookie:
                response["error"] = can_user_add_cookie["error"]
                return response
            elif 'result' in can_user_add_cookie and can_user_add_cookie["result"]["cookie"] > 4:
                response["error"] = "User cannot add more cookies"
                return response
            elif 'errorMessage' in can_user_add_cookie:
                properties = {
                    "cookie" : 1
                }
            else:
                properties = {
                    "cookie" : can_user_add_cookie["result"]["cookie"] + 1
                }
            cookie_result = helper.create_a_relationship(src=src,tgt=tgt,rel="SENT",properties=properties)
            response["result"] = "Cookie added successfully"
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
    
    def fetch_popular_blogs(self):
        response = {}
        helper = Helper()
        labels = ["Blog"]
        try:
            popular_blogs = helper.fetch_popular_blogs(labels=labels)
            if 'error' in popular_blogs:
                response["error"] = popular_blogs["error"]
                return response
            return popular_blogs
        except Exception as err:
            response["error"] = str(err)
            return response
    