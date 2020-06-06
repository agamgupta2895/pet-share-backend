from py2neo import Graph,Node,Relationship
import uuid
from Contants import ServiceConstants
import boto3
import json
from CommonUtils import helper
class Blog:
    def __init__(self):
        self.graph = Graph("http://35.154.113.82:7474",user="neo4j",password="pet-share-india")
        self.client = boto3.client('s3')
    def fetch_all_blogs(self,user_id):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        try:
            graph_response = self.graph.run("""
                                    Match (node:{BLOG_LABEL})
                                    return node
                                    """.format(
                                            BLOG_LABEL = "Blog"
                                    )).data()
            
            return graph_response
        except Exception as err:
            response["error"] = str(err)
            return response
    def fetch_blog(self,user_id,blog_id):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        print("started")
        try:
            graph_response = self.graph.run("""
                                    Match (node:{BLOG_LABEL}  {{id:"{BLOG_ID}"}})
                                    return node
                                    """.format(
                                            BLOG_LABEL = "Blog",
                                            BLOG_ID = blog_id
                                    )).data()
            return graph_response
        except Exception as err:
            response["error"] = str(err)
            return response

    
    def create_or_update_blog(self,user_id,image,data):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        try:
            print("in create or update")
            data = data.encode('ascii','ignore')
            data = json.loads(data)
            if "id" in data:
                blog_id = data["id"]
            else:
                blog_id = uuid.uuid4().hex
                data["id"]= blog_id
            blog_path = "blogs/"+str(blog_id)+"/blog_image.jpg"
            bucket_name = 'pet-share-india'
            response = self.client.put_object(
                    ACL = 'public-read',
                    Bucket = bucket_name,
                    Key= blog_path,
                    Body = image,
                    ContentType = 'image/png'
                )
            
            s3_base_url = "https://pet-share-india.s3.ap-south-1.amazonaws.com/"
            data["image_url"] = s3_base_url + blog_path
            property_string = helper.create_property_string("blog",data)
            property_string = property_string["properties"][:-2]
            blog_query = """
                    MERGE (blog:{BLOG_LABEL} {{id:"{BLOG_ID}"}})
                    ON CREATE SET
                    {PROPERTY_STRING}
                    ON MATCH SET
                    {PROPERTY_STRING}
                    """.format(
                            BLOG_LABEL = "Blog",
                            PROPERTY_STRING = property_string,
                            BLOG_ID = blog_id
                    )
            graph_response = self.graph.run(blog_query).data()
            relationship_query = """
                        Match (user:{USER_LABEL} {{id: "{USER_ID}"}})
                        MATCH (blog:{BLOG_LABEL} {{id:"{BLOG_ID}"}})
                        MERGE (user)-[rel:{RELATIONSHIP_NAME}]->(blog)
                    """.format(
                        USER_LABEL = "User",
                        USER_ID = user_id,
                        BLOG_LABEL = "Blog",
                        BLOG_ID = blog_id,
                        RELATIONSHIP_NAME = "CREATED"
                    )
            graph_response = self.graph.run(relationship_query).data()
            return response
            
        except Exception as err:
            response["error"] = str(err)
            return response
