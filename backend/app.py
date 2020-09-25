from flask import Flask  
from Services import api_routes
from Services import User,Blog,Pets
from flask_cors import CORS
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher

app = Flask(__name__) #creating the Flask class object   
CORS(app) 

app.register_blueprint(User.userService) 
app.register_blueprint(Blog.blogsService)
app.register_blueprint(Pets.petsService)

@app.route('/')
def hello_world():
  return 'This is a dockerized application!\n Welcome to PetShare India'

@app.route("/connectivity")
def check_neo4j_connectivity():
  graph = Graph("0.0.0.0:7474",user="neo4j",password="pet-share-india")
  labels = ["Blog"]
  properties = {"name":"Your dad, Akhil!"}
  node = Node(*labels,**properties)
  graph.create(node)
  node = nodeMatcher.match(*labels)
  return dict(node.first())

if __name__ == '__main__':
  app.run(host="0.0.0.0")
