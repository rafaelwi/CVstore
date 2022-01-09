from flask import Flask, render_template
from db import setup_db , insert_company, insert_job,edit_job,remove_job,remove_company,insert_job_app,remove_job_app
app = Flask(__name__)

setup_db()
#insert_company("Facebook")
#insert_job("Pussy magnet","http://facebook.com",6969,4)
#insert_job_app(3,1)
remove_job_app(5)
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/auth/login')
def about():
    return render_template('/auth/login.html')