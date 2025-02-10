from flask import render_template, url_for, flash, redirect, request, Blueprint 
from flask_login import login_user, current_user, logout_user, login_required 
from flaskblog import db, bcrypt 
from flaskblog.models import User, Post 
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email
# creating a blueprint - just like a flask instance 
# passing in name of blueprint
users = Blueprint('users', __name__)

# we dont use the global app variable to create the routes anymore 
# we make routes specially for the users blueprint and register these with the applciation later 
# so it all becomes users.route


# These are the routes from our exisitng routes.py file 
# but we are making them as flask blueprints instead: 

# creating routes for registrationa nd logn 
# placing in get and post methods 
# check for post data valid for the form
# we will add in password hashing 
# and also add a custom validation for the form when signing up to avoid dupliacte users
@users.route("/register", methods = ['GET', 'POST'])
def register(): 

    # if the user is already loggined in: 
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('main.home'))


    form = RegistrationForm()
    if form.validate_on_submit(): 
        # setting password 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create a new user 
        user = User(username = form.username.data, 
                    email = form.email.data, 
                    password = hashed_password)
        
        # add user to database 
        db.session.add(user)
        # commit change to database 
        db.session.commit()
        flash('Your account has been created! You can now Login', 'success')
        return redirect(url_for('users.login'))
    
    # else if there is no user form submitted its just the register page
    return render_template('register.html', title = "Register", form =form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    # if the user is already logged in: 
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('main.home'))



    form = LoginForm()
    if form.validate_on_submit():
        # checks that the email entered into the form matches our database
        # checking the database if username is valid and password: 
        user = User.query.filter_by(email = form.email.data).first()
        # checks that password is correct too: 
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            # if user exists and password is valid then log the user in: 
            login_user(user, remember = form.remember.data)
            # to return a user to the correct website they were viewing before logging in 
            next_page = request.args.get('next')


            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# create logout route: 
# redirects to home
@users.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('main.home'))

# adding a route for account 
# when a user is loggined in they will see this route: 
# login required decoretor so you can access when logged in 
# you have to tell the extension where the login route is located
@users.route("/account", methods = ['GET', 'POST'])
@login_required
def account(): 
    # create instance of the updating account information form: 
    form = UpdateAccountForm()

    if form.validate_on_submit(): 
            # if the form uis valid we can update our curren tusername and email and photo
            # can change values from current user varaibles
            # changing current user values for username and email from the form 

            # adding another conditional to see if there is any picture data: 
        if form.picture.data: 
                # set the users profile picture 
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # checl that a picture exists: 
        
        current_user.username = form.username.data
        current_user.email = form.email.data 
        # commit to the database
        db.session.commit()
        # add user image: 
        flash('Your Account has been Updated!', 'success')
        # This avoids reloading POST requests constantly 
        return redirect(url_for('users.account'))
    # else conditional to check if its a get request 
    # so we can populate the fields with current user information
    elif request.method == 'GET': 
        form.username.data = current_user.username 
        form.email.data = current_user.email




    # setting the image file to be sent to acccount template
    # this will take teh image_file used when making the account
    # we have default image that is used
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)


# making a new route so that when you click on a users name it takes you to a page 
# with just their posts: 
@users.route("/user/<string:username>")
# render the template from the templates directory
def user_posts(username): 
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
 
    # getting info for the users posts only: 
    user = User.query.filter_by(username = username).first_or_404()

    # paginate method will be set so we can see 5 posts per pages: 
    # need to make a way so that the we can see the other pages in the posts home route: 
    # filters the posts for the user
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page, per_page = 2)
    # posts = Post.query.all()
    # we are also rendering a new user posts page on html 
    # this is where we see posts only from that user! 
    return render_template('user_posts.html', posts = posts, user = user)



# create new routes for requesting email so that 
# reset password information will be sent
# this just handles where they enter their email and information is sent to them 
# to change the actual password
@users.route("/reset_password", methods = ['GET', 'POST'])
def reset_request(): 
    # we want user to be logoutted to get to this page
        # if the user is already logged in: 
        # which means they will always be in the home 
        # if they are logged in
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('main.home')) 

    # create the form 
    form = RequestResetForm()

    # handle if form was validated on submit 
    # so they have submitted an email 
    if form.validate_on_submit(): 
        user = User.query.filter_by(email = form.email.data).first()
        # after we have user we want to send an email with this token 
        send_reset_email(user)
        flash("An email has been sent with instructions", 'info')
        return redirect(url_for('users.login'))
    # render template: 
    return render_template('reset_request.html', title = "Reset Password", 
                           form = form)
    

# create a route where the user reesets their password
# we can check the token is part of the user 
# so it checks they are the same person 
# this is where they reset the password with the token active
@users.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token): 
    # we want user to be logoutted to get to this page
        # if the user is already logged in: 
        # which means they will always be in the home 
        # if they are logged in
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('main.home')) 
    # check with token code: 
    # this token is passed via the url 
    # it takes a token, if the token is valid it return 
    # the user with that user id 
    # user id is the payload into the initial token 
    # if there is no token, then its invalid or expired
    user = User.verify_reset_token(token)

    # check if valid 
    if user is None: 
        flash ("That is an invalid or expired Token", 'warning')
        return redirect(url_for('users.reset_request'))
    # so we can now place the form as its valid: 
    form = ResetPasswordForm() 
    # render template to rset password
    if form.validate_on_submit(): 
        # setting password 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # change password 
        user.password = hashed_password
        # commit change to database 
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('users.login'))

    
    return render_template('reset_token.html', title = 'Reset Passowrd', form = form)
