from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')

@main.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")
