import os 
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



# dummy data: 
# can be used int he template for home.html using jinja 
# posts = [

#     {'title': 'Bond Market',
#      'author': 'john Doe', 
#      'content': 'HSBC' , 
#      'date_posted': '01-01-2024'
#      }, 

#     {'title': 'Gilts Market',
#      'author': 'John Smith', 
#      'content': 'JP Morgan', 
#      'date_posted': '01-01-2024'
#      } 


# ]




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
@app.route("/about")
def about(): 
    return render_template('about.html', title = "About Page")

# creating routes for registrationa nd logn 
# placing in get and post methods 
# check for post data valid for the form
# we will add in password hashing 
# and also add a custom validation for the form when signing up to avoid dupliacte users
@app.route("/register", methods = ['GET', 'POST'])
def register(): 

    # if the user is already loggined in: 
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('home'))


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
        return redirect(url_for('login'))
    
    # else if there is no user form submitted its just the register page
    return render_template('register.html', title = "Register", form =form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if the user is already logged in: 
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('home'))



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


            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# create logout route: 
# redirects to home
@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('home'))

# save picture: 
def save_picture(form_picture): 
    # saves the users picture, but not the filename: 
    # hex makes a random filename for the item 
    random_hex = secrets.token_hex(8)
    # splits out the filename into two objects, we wont use the first 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # get full path where the image will be saved 
    # using root path atrtribute of the app 
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize image: 
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)


    # save the image to the filestystem 
    # this does not update the database
    i.save(picture_path)

    # return picture filename: 
    return picture_fn


# adding a route for account 
# when a user is loggined in they will see this route: 
# login required decoretor so you can access when logged in 
# you have to tell the extension where the login route is located
@app.route("/account", methods = ['GET', 'POST'])
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
        return redirect(url_for('account'))
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


# New route for a user to create a new post: 
@app.route("/post/new", methods = ['GET', 'POST'])
# need a login required decorator as user needs to be logged in 
@login_required
def new_post(): 
    # create instance of the form
    form = PostForm()
    # this validates the form when it is sent via POST request 
    # flashes a message to the screen 
    # then redirects to the home page
    if form.validate_on_submit(): 

        # adding the post to the database: 
        # here we are using the class model that we made earlier and passing in its values 
        # here we are using backref as author, but you dont need to and can use user_id
        post = Post(title = form.title.data, 
                    content = form.content.data, 
                    author = current_user
                    )
        
        # add values: 
        db.session.add(post)
        # commit to db 
        db.session.commit()

        flash("Your Post has been created!", 'success')
        return redirect(url_for('home'))

    # passing in the form into the html template
    return render_template("create_post.html", title = "New Post", 
                           form = form, 
                           legend = "New Post")

# now creating a way to delete the posts we make 
# this would be to update and delete posts 

## a route will take you to a specific page and post: 
### flask lets you add variables within a route
# so if the id of a route is part of the route we make this function: 
# the varuable is post_id and is then passed into the Post.query commanmd 
# hence we can extract the id
# so each post will hae a url like localhost:5000/post_1
@app.route("/post/<int:post_id>")
def post(post_id):
    # we fetch the post 
    post = Post.query.get_or_404(post_id)
    # render template for the returned post 
    return render_template('post.html', title = post.title, post = post)
     

# a new route to delete a post 
# this will be a new form to update the post
# a suer must be logged in to update a post: 
# variables within a route lets you go to specific pages
@login_required
@app.route("/post/<int:post_id>/update",methods= ['GET', 'POST'])
def update_post(post_id):


    # we fetch the post 
    post = Post.query.get_or_404(post_id)
    # only a posts author can amend their own post: 
    # conditional check to make sure they are who they are: 
    # using backref of author
    if post.author != current_user: 
        abort(403)
    
    # create form to post a new form: 
    form = PostForm()

    # check validation: 
    if form.validate_on_submit(): 
        post.title = form.title.data 
        post.content = form.content.data
        # comitt changes but do not need to add these as theses are already there 
        db.session.commit()
        # flash messahge to screen 
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('post', post_id = post.id))
    # this populates the fields as its a get request
    elif request.method == "GET": 
        form.title.data = post.title 
        form.content.data = post.content


    # render template for the returned post 
    return render_template('create_post.html', title = 'Update Post', 
                           form = form, legend = "Update Post")
     


# A route to delete a post: 
@login_required
@app.route("/post/<int:post_id>/delete",methods= [ 'POST'])
def delete_post(post_id):


    # we fetch the post 
    post = Post.query.get_or_404(post_id)
    # only a posts author can amend their own post: 
    # conditional check to make sure they are who they are: 
    # using backref of author
    if post.author != current_user: 
        abort(403)
    # delete the post from teh db 
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    # return to home page: 
    return redirect(url_for('home'))
    

# making a new route so that when you click on a users name it takes you to a page 
# with just their posts: 
@app.route("/user/<string:username>")
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