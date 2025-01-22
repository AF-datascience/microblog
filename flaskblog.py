# import flask class
from flask import Flask 
# app is an instance of flask viarable 
# __name__ is the name of the module, this is the same as main - so flask knows where to look
app = Flask(__name__)

# routesare where to go to different pages 
# made using route decorators
# this function returns the info on this site, here it is text 
# envronment variable is set to run the flask app using $env
# have server running in debug mode
@app.route("/")
def hello(): 
    return "<h3>Main</h3>"

# conditional to run app 

if __name__ == '__main__': 
    app.run(debug = True)