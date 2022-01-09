from flask import Flask, render_template
from db import setup_db , insert_company, insert_job,edit_job,remove_job,remove_company
app = Flask(__name__)

setup_db()
insert_company("Wigger")
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/auth/login')
def about():
    return render_template('/auth/login.html')