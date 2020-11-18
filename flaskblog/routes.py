from flask import render_template, flash, redirect, url_for
from flaskblog import app
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful login attempt', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/resume')
def resume():
    return render_template('resume.html')
