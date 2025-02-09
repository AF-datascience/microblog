from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db 
from flaskblog.models import Post 
from flaskblog.posts.forms import PostForm


# creating a blueprint - just like a flask instance 
# passing in name of blueprint
posts = Blueprint('posts', __name__)

# we dont use the global app variable to create the routes anymore 
# we make routes specially for the users blueprint and register these with the applciation later 
# so it all becomes posts.route


# New route for a user to create a new post: 
@posts.route("/post/new", methods = ['GET', 'POST'])
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
        return redirect(url_for('main.home'))

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
@posts.route("/post/<int:post_id>")
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
@posts.route("/post/<int:post_id>/update",methods= ['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id = post.id))
    # this populates the fields as its a get request
    elif request.method == "GET": 
        form.title.data = post.title 
        form.content.data = post.content


    # render template for the returned post 
    return render_template('create_post.html', title = 'Update Post', 
                           form = form, legend = "Update Post")
     


# A route to delete a post: 
@login_required
@posts.route("/post/<int:post_id>/delete",methods= [ 'POST'])
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
    return redirect(url_for('main.home'))
    