
from py2neo import Graph,Node,Relationship
import jwt
import datetime



def create_property_string(entity,properties):
    """
    :entity - name of the node for which the property string is getting created
    :properties - the complete object to be saved
    """
    response = {}
    try:

        str_properties = ""
        for key,value in properties.items():
            value = str(value)   
            value = value.replace('"', '\\"')
            row = "{entity}.{a}=".format(a=key, entity=entity) \
                        + "\"" + str(value) + "\",\n"""
            str_properties = str_properties + row
        response["properties"] = str_properties
        return response
    except Exception as err:
        response["error"] = str(err)
        return response

def get_user_details(email=None,user_id=None,graph=None):
    """
    """
    graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")
    response = {}
    try:
        if user_id is not None:
            user_details_query = """
                            Match (user:{USER_LABEL} {{id: "{USER_ID}"}})
                            return user
                        """.format(
                            USER_LABEL = "User",
                            USER_ID = user_id
                        )
        elif email is not None:
            user_details_query = """
                            Match (user:{USER_LABEL} {{email: "{EMAIL}"}})
                            return user
                        """.format(
                            USER_LABEL = "User",
                            EMAIL = email
                        )
        graph_response = graph.run(user_details_query).data()
        if len(graph_response)>0:
            response["data"] = graph_response[0]["user"]
            return response
        response["error"] = "User not found"
        return response
    except Exception as err:
        response["error"] = str(err)
        return response
