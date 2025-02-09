import os
import secrets 
from PIL import Image 
from flask import url_for 
from flask_mail import Message 
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


# define function to send a reset email to a user 
def send_reset_email(user): 
    # now we will send an email to a user
    # send a user an email with reset token 
    # using method we added to user model 
    token = user.get_reset_token()
    # send email with usrl using msg class 
    msg = Message('Password Reset Request', sender =
                  'noreply@demo.com', 
                  recipients = [user.email])
    # body of the msg: 
    msg.body = f"""
    To reset your password vist the following link: 
    {url_for('reset_token', token = token,
             _external = True)}

    If you did not make this request, ignore this email!
"""

    # now send the email: 
    mail.send(msg)