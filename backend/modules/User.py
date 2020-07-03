from py2neo import Graph,Node,Relationship
from CommonUtils.Helper import Helper
class User:
    def __init__(self):
        self.graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")

    def check_if_user_present_in_backend(self,search):
        """
        :user_id - ID of the logged in user
        :response - True/False 
        """
        response = {}
        labels = ["User"]
        try:
            helper = Helper()
            user_present = helper.find_single_node_in_db(labels=labels,
                                            search = search)
            if 'error' in user_present:
                response["error"] = user_present["error"]
                return response
            return user_present
        except Exception as err:
            response["error"] = str(err)
            return response

    def create_or_update_user(self, content,user_id):
        """
        :data - data of the logged in user
        :response - True/False 
        """
        response = {}
        helper = Helper()
        labels = ["User"]
        search = {"id":user_id}
        try:
            user = helper.create_a_new_node(labels= labels,properties = content,search = search)
            if 'error' in user:
                return user
            return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def fetch_user_blogs(self,user_id):

        response = {}
        helper = Helper()
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

    def get_node_details(self,search):
        response = {}
        labels = ["User"]
        try:
            helper = Helper()
            user_present = helper.find_single_node_in_db(labels=labels,
                                            search = search)
            if 'error' in user_present:
                response["error"] = user_present["error"]
                return response
            response["result"] = user_present
            return response
        except Exception as err:
            response["error"] = str(err)
            return response