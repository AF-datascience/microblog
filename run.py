# conditional to run app 
# this will run if we run script directly
# python calls this script __main__ when we run it directly
from flaskblog import app

if __name__ == '__main__': 
    app.run(debug = True)