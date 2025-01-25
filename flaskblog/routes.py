from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app
from flaskblog.models import User, Post

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


