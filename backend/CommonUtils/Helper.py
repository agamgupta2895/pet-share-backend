
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import jwt
import datetime

class Helper:
    def __init__(self):
        self.graph = Graph("http://3.7.71.31:7474",user="neo4j",password="pet-share-india")
        self.nodeMatcher = NodeMatcher(self.graph)
        self.relationshipMatcher = RelationshipMatcher(self.graph)

    def create_a_new_node(self,labels,properties,search):
        response = {}
        try:
            node = self.nodeMatcher.match(*labels,**search)
            if len(node) > 0:
                node = node.first()
                for key,value in properties.items():
                    node[key] = value
                self.graph.push(node)
            else:
                node = Node(*labels,**properties)
                self.graph.create(node)
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
        return node
    def find_single_node_in_db(self,labels=None,search=None):
        response = {}
        try:
            node = self.nodeMatcher.match(*labels,**search)
            if len(node) > 0:
                node_labels = list(node.first().labels)
                node_properties = dict(node.first())
                response["node_labels"] = node_labels
                response["node_properties"] = node_properties
                return response
            else:
                response["errorMessage"] = "Entity not present"
                return response
        except Exception as err:
            response["error"] = str(err)
            return response
    def find_nodes_in_db(self,labels,search=None):
        response = {}
        data = []
        try:
            if search == None:
                nodes = self.nodeMatcher.match(*labels)
            else:
                nodes = self.nodeMatcher.match(*labels,**search)
            if len(nodes) > 0:
                for node in nodes:
                    data.append(dict(node))
                return data
            else:
                return data
        except Exception as err:
            response["error"] = str(err)

    def create_a_relationship(self,src,tgt,rel,properties = None):
        response = {}
        try:
            src_node_search = src["search"]
            src_node_labels = src["labels"]
            tgt_node_search = tgt["search"]
            tgt_node_labels = tgt["labels"]
            src_node = self.nodeMatcher.match(*src_node_labels,**src_node_search).first()
            tgt_node = self.nodeMatcher.match(*tgt_node_labels,**tgt_node_search).first()
            if properties is None:
                src_rel_tgt = Relationship(src_node,rel,tgt_node)
            else:
                src_rel_tgt = Relationship(src_node,rel,tgt_node,**properties)
            self.graph.create(src_rel_tgt)
            return response
        except Exception as err:
            response["error"] = str(err)
            return response
    def delete_single_node_in_db(self,labels=None,search=None):
        response = {}
        try:
            node = self.nodeMatcher.match(*labels,**search)
            if len(node) > 0:
                self.graph.delete(node.first())
                return response
            else:
                response["errorMessage"] = "Entity not present"
                return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def fetch_a_relationship(self,src,tgt,rel):
        response = {}
        try:
            src_node_search = src["search"]
            src_node_labels = src["labels"]
            tgt_node_search = tgt["search"]
            tgt_node_labels = tgt["labels"]
            src_node = self.nodeMatcher.match(*src_node_labels,**src_node_search).first()
            tgt_node = self.nodeMatcher.match(*tgt_node_labels,**tgt_node_search).first()
            relationship = self.relationshipMatcher.match(nodes=[src_node,tgt_node],r_type = rel).first()
            if relationship is not None:
                relationship_properties = dict(relationship)
                response["result"] = relationship_properties
                return response
            else:
                response["errorMessage"] = "Relationship not found"
                return response
        except Exception as err:
            response["error"] = str(err)
            return response

    def fetch_popular_blogs(self,labels):
        response = {}
        data =[]
        try:
            nodes = self.nodeMatcher.match(*labels).order_by("_.cookie DESC").limit(5)
            if len(nodes) > 0:
                for node in nodes:
                    data.append(dict(node))
                return data
            else:
                return data
        except Exception as err:
            response["erorr"] = str(err)
            return response

    def fetch_nodes_with_relationship(self,src,tgt,rel):
        response = {}
        try:
            
            src_node_search = src["search"]
            src_node_labels = src["labels"]
            src_node = self.nodeMatcher.match(*src_node_labels,**src_node_search).first()
            tgt_node = self.nodeMatcher.match(*tgt_node_labels)
            relationship = self.relationshipMatcher.match(nodes=[src_node,tgt_node],r_type = rel).first()
            if relationship is not None:
                relationship_properties = dict(relationship)
                response["result"] = relationship_properties
                return response
            else:
                response["errorMessage"] = "Relationship not found"
                return response
        except Exception as err:
            response["error"] = str(err)
            return response