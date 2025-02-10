# conditional to run app 
# this will run if we run script directly
# python calls this script __main__ when we run it directly
from flaskblog import create_app

# can pass in a config if we want, but passed in default
app = create_app()

# we dont need to import app - instead import create_app function 
if __name__ == '__main__': 
    app.run(debug = True)