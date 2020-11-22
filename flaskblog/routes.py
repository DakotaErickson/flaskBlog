import secrets
import os 
import json
from math import ceil
import requests
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/group?id=5809844,5746545,5419384&appid=dec3905e6011fd6078f2f0444f6e25c9')
    responseJson = response.json()
    cityList = responseJson['list']
    seattleKelvin = cityList[0]['main']['temp']
    seattleFahrenheit = kelvinToFahrenheit(seattleKelvin)
    portlandKelvin = cityList[1]['main']['temp']
    portlandFahrenheit = kelvinToFahrenheit(portlandKelvin)
    denverKelvin = cityList[0]['main']['temp']
    denverFahrenheit = kelvinToFahrenheit(denverKelvin)
    return render_template('home.html', posts=posts, title='Home', seattleTemp=seattleFahrenheit, portlandTemp=portlandFahrenheit, denverTemp=denverFahrenheit)


def kelvinToFahrenheit(temp):
    return ceil((temp - 273.15) * 1.8 + 32)


@app.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template('posts.html', posts=posts, title='Posts')


@app.route('/post/<int:postId>')
def post(postId):
    post = Post.query.get_or_404(postId)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        newPost = Post(title=form.title.data,
                       content=form.content.data, author=current_user)
        db.session.add(newPost)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template('newPost.html', title='New Post', form=form, legend='New Post')


@app.route('/post/<int:postId>/edit', methods=['GET', 'POST'])
@login_required
def edit(postId):
    post = Post.query.get_or_404(postId)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('post', postId=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('editPost.html', title="Edit Post", form=form, legend='Edit Post')


@app.route('/deletePost/<int:postId>', methods=['POST'])
@login_required
def deletePost(postId):
    post = Post.query.get_or_404(postId)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted', 'success')
    return redirect(url_for('posts'))


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPW = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        newUser = User(username=form.username.data,
                       email=form.email.data, password=hashedPW)
        db.session.add(newUser)
        db.session.commit()
        flash(f'Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('home'))
        else:
            flash('Unsuccessful login attempt. Check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def savePicture(formPicture):
    randomHex = secrets.token_hex(8)
    _, fileExtension = os.path.splitext(formPicture.filename)
    pictureFileName = randomHex + fileExtension
    picturePath = os.path.join(
        app.root_path, 'static/profilePics', pictureFileName)

    # image resizing
    outputSize = (125, 125)
    i = Image.open(formPicture)
    i.thumbnail(outputSize)
    i.save(picturePath)

    prev_picture = os.path.join(
        app.root_path, 'static/profilePics', current_user.imageFile)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return pictureFileName


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profilePic.data:
            pictureFile = savePicture(form.profilePic.data)
            current_user.imageFile = pictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for(
        'static', filename='profilePics/' + current_user.imageFile)
    return render_template('account.html', title='Account', imageFile=imageFile, form=form)
