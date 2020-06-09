
def create_property_string(entity,properties):
    """
    :entity - name of the node for which the property string is getting created
    :properties - the complete object to be saved
    """
    response = {}
    try:

        str_properties = ""
        for key,value in properties.items():
            if type(value) == "str":
                value = value.replace('"', '\\"')
            row = "{entity}.{a}=".format(a=key, entity=entity) \
                        + "\"" + str(value) + "\",\n"""
            str_properties = str_properties + row
        response["properties"] = str_properties
        return response
    except Exception as err:
        response["error"] = str(err)
        return response