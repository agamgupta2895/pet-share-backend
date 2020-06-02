from flask import Flask  
from Services import api_routes
from Services import User,Blog


app = Flask(__name__) #creating the Flask class object   
 

app.register_blueprint(User.userService) 
app.register_blueprint(Blog.blogsService) 

if __name__ =='__main__':  
    app.run(host= api_routes.__HOST,debug = True)  