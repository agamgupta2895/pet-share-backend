from py2neo import Graph,Node,Relationship
import uuid
from Contants import ServiceConstants
import boto3
import json
from CommonUtils import helper
class Blog:
    def __init__(self):
        self.graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")
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
        try:
            graph_response = self.graph.run("""
                                    Match (node:{BLOG_LABEL}  {{id:"{BLOG_ID}"}})
                                    return node
                                    """.format(
                                            BLOG_LABEL = "Blog",
                                            BLOG_ID = blog_id
                                    )).data()
            node = dict(graph_response[0]["node"])
            if user_id == node["created_by"]:
                node["is_owner"] = True
            else:
                node["is_owner"] = False
            response["Blog"] = node
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
    def create_or_update_blog(self,user_id,image,data):
        """
        :user_id - ID of the logged in user
        :response - 
        """
        response = {}
        try:
            data = data.encode('ascii','ignore')
            data = json.loads(data)
            data["created_by"] = user_id
            user_details = helper.get_user_details(user_id=user_id,graph=self.graph)
            if "error" in user_details:
                response["error"] = user_details["error"]
                return response
            user_details = dict(user_details["data"])
            data["author"] = user_details["name"]
            
            if "id" in data:
                blog_id = data["id"]
            else:
                blog_id = uuid.uuid4().hex
                data["id"]= blog_id
            if image is not None:
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
    def delete_a_blog(self,user_id,blog_id):
        """
        """
        response = {}
        try:
            query_to_fetch_blog = """
                            Match(user:{USER_LABEL} {{id:"{USER_ID}"}})-[rel:{CREATED_LABEL}]->(blog:{BLOG_LABEL}{{id:"{BLOG_ID}"}})
                            return blog
                        """.format(
                            USER_ID = user_id,
                            USER_LABEL = "User",
                            CREATED_LABEL = "CREATED",
                            BLOG_LABEL = "Blog",
                            BLOG_ID = blog_id
                        )
            graph_response = self.graph.run(query_to_fetch_blog).data()
            if len(graph_response) > 0 :
                graph_response = graph_response[0]["blog"]
                if "image_url" in graph_response:
                    image_url = graph_response["image_url"]
                    path = image_url.split("/")
                    path = path[-3] + "/" + path[-2] + "/" + path[-1]
                    delete_list = [
                        {
                            'Key' : path
                        }
                    ]
                    bucket = self.client.delete_objects(
                        Bucket = "pet-share-india",
                        Delete = {
                            'Objects' : delete_list
                        }
                    )
                
                query_to_delete_blog = """
                                Match (blog:{BLOG_LABEL}{{id:"{BLOG_ID}"}})
                                detach delete blog
                            """.format(
                                BLOG_LABEL = "Blog",
                                BLOG_ID=blog_id
                            )
                graph_response = self.graph.run(query_to_delete_blog).data()
                response["message"] = "delete successfully"
                return response
            else:
                response["error"] = "Invalid user trying to delete the blog"
                return response
        except Exception as err:
            response["error"] = str(err)
            return response
    def add_cookie(self,blog_id):
        """
        """
        response = {}
        try:
            query_to_add_counter = """
                Match(blog:{BLOG_LABEL} {{id:"{BLOG_ID}"}})
                set blog.cookie = toInteger(blog.cookie) + 1
            """.format(
                BLOG_LABEL = "Blog",
                BLOG_ID = blog_id
            )
            print(query_to_add_counter)
            graph_response = self.graph.run(query_to_add_counter)
            response["result"] = "Cookie added successfully"
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
    
    def fetch_popular_blogs(self):
        response = {}
        try:
            query_to_fetch_popular_blogs = """
                Match(blog:{BLOG_LABEL})
                return blog.title as title,blog.author as author,blog.id as id ,blog.cookie as cookie,blog.image_url as image_url
                order by toInteger(blog.cookie) desc
                limit 5
            """.format(
                BLOG_LABEL = "Blog"
            )
            graph_response = self.graph.run(query_to_fetch_popular_blogs)
            response["result"] = graph_response.data()
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
    