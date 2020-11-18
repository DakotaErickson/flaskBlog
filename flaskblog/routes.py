from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'author': 'Dakota',
        'title': 'Blog Post 1',
        'content': 'First Blog Post',
        'date_posted': 'November 16, 2020'
    },
    {
        'author': 'Samantha',
        'title': 'Blog Post 2',
        'content': 'Second Blog Post',
        'date_posted': 'November 17, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPW = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newUser = User(username=form.username.data, email=form.email.data, password=hashedPW)
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
    return render_template('resume.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
