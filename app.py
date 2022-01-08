from flask import Flask, render_template
from db import setup
app = Flask(__name__)

setup()
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/auth/login')
def about():
    return render_template('/auth/login.html')