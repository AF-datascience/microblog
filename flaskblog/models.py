# class models are the database 
# each class is a table in the database 
from datetime import datetime
from flaskblog import db, login_manager, app
# this is for users emails and passwords to genrerate a secure time sensitve token 
# so that only someone with access to the users email can reset their password
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin

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

# create function that loads a user based on the id 
# so we are adding functionality to the database models and the 
# login manager will handle the sessions for us 
# this is a decorated functio nto reloading the user_id from the session 
# so flask-login needs to find user by id 

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id))


# posts has author as a backreference
# this means that we can access the users posts via the author


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # creating methods that make it easier to generate tokens used for resetting emails and passwords
    def get_reset_token(self): 
        # create serializers
        s = Serializer(app.config['SECRET KEY'])
        # return a token with this serailizer 
        # this is the payload
        return s.dumps({'user_id': self.id})
    
    # methd to verify a token 
    # takes a token as argument 
    # creates a serializer 
    # loads a token 
    # with exception returns none 
    # else returns a users id 
    # does not use self method - is static method
    # do not expect self as an argument
    @staticmethod
    def verify_reset_token(token): 
        s = Serializer(app.config['SECRET KEY'])
        try: 
            user_id = s.loads(token)['user_id']
        except:     
            return None
        
        # reutnr user id: 
        return User.query.get(user_id)
    # create 

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



