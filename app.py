from flask import Flask, render_template
import json
from db import setup_db , insert_company, insert_job,edit_job,remove_job,remove_company,insert_job_app,remove_job_app,get_job_apps
app = Flask(__name__)

setup_db()
#insert_company("Facebook")
#insert_job("Ass eatta","http://facebook.com",6969420,4)
#insert_job_app(6,7)
#remove_job_app(5)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/auth/login')
def about():
    return render_template('/auth/login.html')

@app.route('/api/get_job_apps')
def get_job_apps_endpoint():
    return json.dumps(get_job_apps())