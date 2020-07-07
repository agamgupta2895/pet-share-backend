from py2neo import Graph,Node,Relationship
import uuid
from CommonUtils.Helper import Helper
from Contants import ServiceConstants
import boto3
import json
#from CommonUtils import helper
class Pet:
    def __init__(self):
        self.graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")
        self.client = boto3.client('s3')
        self.s3_base_url = "https://pet-share-india.s3.ap-south-1.amazonaws.com/"
    def create_or_update_pet_profile(self,user_id,images,data):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        helper = Helper()

        try:
            data["created_by"] = user_id
            pet_type = data["pet_type"]
            pet_breed = data["pet_breed"]
            if "id" in data:
                pet_id = data["id"]
            else:
                pet_id = uuid.uuid4().hex
                data["id"]= pet_id
            search = {"id":data["id"]}
            if images is not None:
                images_paths = []
                for image in images:
                    image_id = str(uuid.uuid4().hex)
                    image_path = "pets/"+str(pet_id)+"/"+image_id+".jpg"
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
            labels = ["Pet",pet_type,pet_breed]
            print("here")
            pet_node = helper.create_a_new_node(labels =labels,
                                                properties = data,
                                                search=search)
            if 'error' in pet_node:
                response["error"] = blog_node["error"]
                return response
            src = {
                "labels" :["User"],
                "search":{"id":user_id}
            }
            tgt = {
                "labels" :["Pet"],
                "search" : {"id":pet_id}
            }
            relationship  = helper.create_a_relationship(src=src,tgt=tgt,rel="ADDED_PET")                 
            if 'error' in relationship:
                response["error"] = relationship["error"]
            return response
            
        except Exception as err:
            response["error"] = str(err)