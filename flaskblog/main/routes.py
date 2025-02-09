# import the correct packages
from flask import render_template, request, Blueprint 
from flaskblog.models import Post

# creating a blueprint - just like a flask instance 
# passing in name of blueprint
main = Blueprint('main', __name__)

# we dont use the global app variable to create the routes anymore 
# we make routes specially for the users blueprint and register these with the applciation later 
# so it all becomes main.route

# routesare where to go to different pages 
# made using route decorators
# this function returns the info on this site, here it is text 
# envronment variable is set to run the flask app using $env
# have server running in debug mode
# two routes can be handled by the same function
@main.route("/")
@main.route("/home")
# render the template from the templates directory
def home(): 
    # this conde renderes the dummy data into the html file
    # return render_template('home.html', posts = posts)
    # a new posts ariaable is equialent from our posts 
    # paginate this home page so that we can have a set number of posts per page

    # for specific pages: 
    # sets default page as 1 
    # grabs a page we want
    # so someone has to pass a page number a s number
    # we pass thios page into the query below
    # its like when you pass in ?page = int in the url bar
    page = request.args.get('page', 1, type = int)

    # paginate method will be set so we can see 5 posts per pages: 
    # need to make a way so that the we can see the other pages in the posts home route: 

    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 2)
    # posts = Post.query.all()
    return render_template('home.html', posts = posts)

# about page route: 
@main.route("/about")
def about(): 
    return render_template('about.html', title = "About Page")
