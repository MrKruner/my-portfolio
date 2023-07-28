from flask import Flask, Blueprint, render_template

views= Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')