# import flask class
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from forms import RegistrationForm, LoginForm
from datetime import datetime

# app is an instance of flask viarable 
# __name__ is the name of the module, this is the same as main - so flask knows where to look
app = Flask(__name__)
# url-for finds the routes finds the location of teh routes for us. 

# set a secret key to stop people messing with the app
app.config['SECRET_KEY'] = 'fea587cc66094ff6e53b8b3288d38d0d'
# set a location for the sql database: 
# relative path from the current file
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

# create database instance 
db = SQLAlchemy(app)


# class models are the database 
# each class is a table in the database 

# class or model for the users 
# class Users(db.Model): 
#     # columns for table: 
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(20), unique = True, nullable = False)
#     email = db.Column(db.String(120), unique = True, nullable = False)
#     image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
#     password = db.Column(db.String(60), nullable = False)

#     # the post model has a relationship to teh user model 
#     # beckref lets u find the user who made the post 
#     # lazy loads data in one go 
#     posts = db.relationship('Post', backref = 'author', lazy = True)
#     # this references hte post class
#     # a repr method 
#     # how an object is printed

#     def __repr__(self): 
#         return f"User {self.username}, email {self.email}. {self.image}"

# # so a post can belong to one user only 
# # but a user can have many posts 
# # this is a one to many relationship, one author but many posts 
# # table names iwll be se to lowercase e.g. User class makes table user. 
# # specify the user in the posts model 

# # class to model the Posts: 
# class Post(db.Model): 
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(100), nullable = False)   
#     data_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     content = db.Column(db.Text, nullable = False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     # here the reference is the table name and column name 
#     # creating attribute above forthe user int he posts moel

#     def __repr__(self): 
#         return f"Post '{self.title} and date: {self.date_posted}"

# the post attribute is not a column it is a query grabbic the posts from teh user


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



# dummy data: 
# can be used int he template for home.html using jinja 
posts = [

    {'title': 'Bond Market',
     'author': 'john Doe', 
     'content': 'HSBC' , 
     'date_posted': '01-01-2024'
     }, 

    {'title': 'Gilts Market',
     'author': 'John Smith', 
     'content': 'JP Morgan', 
     'date_posted': '01-01-2024'
     }, 


]




# routesare where to go to different pages 
# made using route decorators
# this function returns the info on this site, here it is text 
# envronment variable is set to run the flask app using $env
# have server running in debug mode
# two routes can be handled by the same function
@app.route("/")
@app.route("/home")
# render the template from the templates directory
def home(): 
    return render_template('home.html', posts = posts)

# about page route: 
@app.route("/about")
def about(): 
    return render_template('about.html', title = "About Page")

# creating routes for registrationa nd logn 
# placing in get and post methods 
# check for post data valid for the form
@app.route("/register", methods = ['GET', 'POST'])
def register(): 
    form = RegistrationForm()
    if form.validate_on_submit(): 
        flash(f'Acount created for {form.username.data}', category = "success")
        return redirect(url_for('home'))
    return render_template('register.html', title = "Register", form =form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)






# conditional to run app 
# this will run if we run script directly
if __name__ == '__main__': 
    app.run(debug = True)