from flask import Flask  
from Services import api_routes
from Services import User
import urllib
app = Flask(__name__) #creating the Flask class object   
 

app.register_blueprint(User.userService) 

if __name__ =='__main__':  
    app.run(host= api_routes.__HOST,debug = True)  