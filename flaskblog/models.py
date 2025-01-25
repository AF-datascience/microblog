# class models are the database 
# each class is a table in the database 
from datetime import datetime
from flaskblog import db

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



