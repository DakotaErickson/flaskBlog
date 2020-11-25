# from flask import render_template, url_for, flash, redirect, request, Blueprint
# from flask_login import login_user, current_user, logout_user, login_required
# from flaskblog import db, bcrypt
# from flaskblog.models import User, Post
# from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
# from flaskblog.users.utils import savePicture, sendResetEmail

# users = Blueprint('users', __name__)


# @users.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashedPW = bcrypt.generate_password_hash(
#             form.password.data).decode('utf-8')
#         newUser = User(username=form.username.data,
#                        email=form.email.data, password=hashedPW)
#         db.session.add(newUser)
#         db.session.commit()
#         flash(f'Account created successfully! Please login.', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('register.html', title='Register', form=form)


# @users.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             nextPage = request.args.get('next')
#             return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
#         else:
#             flash('Unsuccessful login attempt. Check email and password.', 'danger')
#     return render_template('login.html', title='Login', form=form)


# @users.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('main.home'))


# @users.route('/account', methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.profilePic.data:
#             pictureFile = savePicture(form.profilePic.data)
#             current_user.imageFile = pictureFile
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Account updated', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     imageFile = url_for(
#         'static', filename='profilePics/' + current_user.imageFile)
#     return render_template('account.html', title='Account', imageFile=imageFile, form=form)


# @users.route('/user/<string:username>')
# def userPosts(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.datePosted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('userPosts.html', posts=posts, title='Posts', user=user)


# @users.route('/resetPassword', methods=['GET', 'POST'])
# def resetRequest():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         sendResetEmail(user)
#         flash('If your email is on file you will recieve instructions on how to reset your password.', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('resetRequest.html', title='Reset Password', form=form)


# @users.route('/resetPassword/<token>', methods=['GET', 'POST'])
# def resetToken(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     user = User.verifyResetToken(token)
#     if user is None:
#         flask('Invalid or expired token', 'warning')
#         return redirect(url_for('users.resetRequest'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashedPW = bcrypt.generate_password_hash(
#             form.password.data).decode('utf-8')
#         user.password = hashedPW
#         db.session.commit()
#         flash(f'Password changed successfully! Please login.', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('resetToken.html', title='Reset Password', form=form)
