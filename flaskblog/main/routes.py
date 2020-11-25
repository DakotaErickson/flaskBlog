import os, requests, json
from math import ceil
from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')

@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")
