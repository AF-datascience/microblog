# creating blueprint to handle errors: 
# e.g. what happens when the page is not found by the user
# blueprints are always packages e.g. have an __init__.py file 
# this handlers.py file is like our routes
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


# similair to creating routes but use errors: 
# use a different decorator
# app_errorhandler works across the entire app not just a singular blueprint

@errors.app_errorhandler(404)
def error_404(error): 
    return render_template("errors/404.html"), 404

# this is 403 page
@errors.app_errorhandler(403)
def error_403(error): 
    return render_template("errors/403.html"), 404

@errors.app_errorhandler(500)
def error_500(error): 
    return render_template("errors/500.html"), 404