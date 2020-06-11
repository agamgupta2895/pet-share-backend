
from py2neo import Graph,Node,Relationship

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

def get_user_details(user_id,graph):
    """
    """

    response = {}
    try:
        user_details_query = """
                        Match (user:{USER_LABEL} {{id: "{USER_ID}"}})
                        return user
                    """.format(
                        USER_LABEL = "User",
                        USER_ID = user_id
                    )
        graph_response = graph.run(user_details_query).data()
        print(graph_response)
        response["data"] = graph_response[0]["user"]
        return response
    except Exception as err:
        response["error"] = str(err)
        return response