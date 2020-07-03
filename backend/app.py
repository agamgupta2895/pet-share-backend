from flask import Flask  
from Services import api_routes
from Services import User,Blog,Pets
from flask_cors import CORS


app = Flask(__name__) #creating the Flask class object   
CORS(app) 

app.register_blueprint(User.userService) 
app.register_blueprint(Blog.blogsService)
app.register_blueprint(Pets.petsService)

@app.route('/landing')
def hello_world():
  return 'Hello from Flask3!'
if __name__ == '__main__':
  app.run()
