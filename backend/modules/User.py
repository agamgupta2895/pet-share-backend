from py2neo import Graph,Node,Relationship

class User:
    def __init__(self):
        self.graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")

    def check_if_user_id_present_in_backend(self,user_id):
        """
        :user_id - ID of the logged in user
        :response - True/False 
        """
        response = {}
        try:
            graph_response = self.graph.run("""
                                    Match (node:{USER_LABEL} {{id:"{USER_ID}"}})
                                    return node
                                    """.format(
                                            USER_LABEL = "User",
                                            USER_ID = user_id
                                    )).data()
            if len(graph_response) > 0:
                response["result"] = True
                return response
            response["result"] = False
            return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def create_or_update_user(self, property_string,user_id):
        """
        :data - data of the logged in user
        :response - True/False 
        """
        response = {}
        try:
            query = """
                    MERGE (user:{USER_LABEL} {{id:"{USER_ID}"}})
                    ON CREATE SET
                    {PROPERTY_STRING}
                    ON MATCH SET
                    {PROPERTY_STRING}
                    """.format(
                            USER_LABEL = "User",
                            PROPERTY_STRING = property_string,
                            USER_ID = user_id
                    )
            print(query)
            graph_response = self.graph.run(query)
            return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def fetch_user_blogs(self,user_id):

        response = {}
        try:
            query = """
                Match(user:{USER_LABEL} {{id:"{USER_ID}"}})-[rel:{CREATED_LABEL}]->(blogs:{BLOG_LABEL})
                return blogs
            """.format(
                            USER_ID = user_id,
                            USER_LABEL = "User",
                            CREATED_LABEL = "CREATED",
                            BLOG_LABEL = "Blog"
                        )
            graph_response = self.graph.run(query).data()
            response["data"] = graph_response
            return response
        except Exception as err:
            response["error"] = str(err)
            return response

