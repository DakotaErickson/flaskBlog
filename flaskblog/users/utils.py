import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from flask_login import current_user

def savePicture(formPicture):
    randomHex = secrets.token_hex(8)
    _, fileExtension = os.path.splitext(formPicture.filename)
    pictureFileName = randomHex + fileExtension
    picturePath = os.path.join(
        current_app.root_path, 'static/profilePics', pictureFileName)

    # image resizing
    outputSize = (125, 125)
    i = Image.open(formPicture)
    i.thumbnail(outputSize)
    i.save(picturePath)

    prev_picture = os.path.join(
        current_app.root_path, 'static/profilePics', current_user.imageFile)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return pictureFileName

def sendResetEmail(user):
    token = user.getResetToken()
    msg = Message('Password Reset Request',
                    sender=os.environ.get('EMAIL'),
                    recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
{url_for('users.resetToken', token=token, _external=True)} 
If you did not make this request then ignore this email and no changes will be made.
'''
    mail.send(msg)