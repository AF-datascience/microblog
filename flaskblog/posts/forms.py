# moving all forms that are for a posts
# as we are making a blueprint 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# A new class form to create a  psot : 
class PostForm(FlaskForm): 
    # validator as every title needs to exist
    title = StringField('Title', validators=[DataRequired()])
    # text area field is needed for the post 
    # every post needs content
    content = TextAreaField('Content', validators=[DataRequired()])
    # submit the field: 
    submit = SubmitField('Post')