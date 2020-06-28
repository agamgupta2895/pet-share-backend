from py2neo import Graph,Node,Relationship

class Validate:
    def __init__(self):
        self.graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")

    def check_if_email_present(self,email):
        response = {}
        try:
            graph_response = self.graph.run("""
                                    Match (node:{USER_LABEL} {{email:"{EMAIL}"}})
                                    return node
                                    """.format(
                                            USER_LABEL = "User",
                                            EMAIL = email
                                    )).data()
            if len(graph_response) > 0:
                raise Exception("Email already present")
            response["result"] = False
            return response
        except Exception as err:
            response["error"] = str(err)
            return response