from py2neo import Graph,Node,Relationship
import uuid
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
        try:
            print(data)
            data = data.encode('ascii','ignore')
            data = json.loads(data)
            data["created_by"] = user_id
            pet_type = data["pet_type"]
            pet_breed = data["pet_breed"]
            user_details = helper.get_user_details(user_id=user_id,graph=self.graph)
            if "error" in user_details:
                response["error"] = user_details["error"]
                return response
            user_details = dict(user_details["data"])
            if "id" in data:
                pet_profile_id = data["id"]
            else:
                pet_profile_id = uuid.uuid4().hex
                data["id"]= pet_profile_id
            if images is not None:
                images_paths = []
                for image in images:
                    image_id = str(uuid.uuid4().hex)
                    image_path = "pets/"+str(pet_profile_id)+"/"+image_id+".jpg"
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
            property_string = helper.create_property_string("pet",data)
            property_string = property_string["properties"][:-2]
            pet_profile_query = """
                    MERGE (pet:{PET_LABEL}:{PET_TYPE}:{PET_BREED} {{id:"{PET_ID}"}})
                    ON CREATE SET
                    {PROPERTY_STRING}
                    ON MATCH SET
                    {PROPERTY_STRING}
                    """.format(
                            PET_LABEL = "Pet",
                            PET_TYPE = pet_type,
                            PET_BREED = pet_breed,
                            PROPERTY_STRING = property_string,
                            PET_ID = pet_profile_id
                    )
            graph_response = self.graph.run(pet_profile_query).data()
            relationship_query = """
                        Match (user:{USER_LABEL} {{id: "{USER_ID}"}})
                        MATCH (pet:{PET_LABEL} {{id:"{PET_ID}"}})
                        MERGE (user)-[rel:{RELATIONSHIP_NAME}]->(pet)
                    """.format(
                        USER_LABEL = "User",
                        USER_ID = user_id,
                        PET_LABEL = "Pet",
                        PET_ID = pet_profile_id,
                        RELATIONSHIP_NAME = "HAS_A"
                    )
            graph_response = self.graph.run(relationship_query).data()
            return response
            
        except Exception as err:
            response["error"] = str(err)
            return response