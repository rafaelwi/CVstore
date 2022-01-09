import poplib
from flask import Flask, render_template, request
from pop3_parse import *
import json
from db import setup_db , insert_company, insert_job,edit_job,remove_job,remove_company,get_job_apps,update_job_status,get_companies

app = Flask(__name__)

setup_db()
#insert_company("Facebook")
#insert_job("Ass eatta","http://facebook.com",6969420,1)
#insert_job_app(1,7)
#remove_job_app(5)
#remove_job_app(3)
#remove_job(3)
#update_job_app_status(6,4)
@app.route('/')
def hello():
    return render_template('email.html')
    # return 'Hello, World!'

@app.route('/auth/login')
def about():
    return render_template('/auth/login.html')

@app.route('/make_pop3_conn', methods=['POST'])
def pop3_connect():
    USER = request.form['email']
    PASS = request.form['password']
    HOST = request.form['host']
    f = request.form.to_dict()
    print(f'Establishing POP3 SSL connection with {HOST}')
    try:
        conn = poplib.POP3_SSL(HOST)
        conn.user(USER)
        conn.pass_(PASS)
        print("Login success")
    except:
        print("Login failed")
        return f"""
        Could not establish a connection with host "{HOST}"<br>
        This could be for one of the following reasons:<br>
        - The host only supports POP3 and not POP3 SSL, please ensure that the host given is POP3 SSL<br>
        - Email and/or password are incorrect, try in a browser first<br>
        - POP3 has not been enabled for your email<br>
        - Gmail: Enable "Less secure app access" at https://myaccount.google.com/lesssecureapps
        """
    messages=[]
    for n in range(1,conn.stat()[0]+1):
        msg = Parser().parsestr(b"\r\n".join(conn.retr(n)[1]).decode('utf-8'))
        payload = msg.get_payload()
        if isinstance(payload, list):
            for i, p in enumerate(payload):
                if 'plain' in p['Content-Type']:
                    messages.append(parse(p.as_string()))

    # for i in messages:
    return f"""
        Connected user "{USER}" (Password: {"*"*len(PASS)}) to "{HOST}"<br>
        Inbox stats: {conn.stat()[0]} messages, {conn.stat()[1]} bytes<br><br>
        Messages:<br>
        {messages}
    """

@app.route('/api/get_job_apps')
def get_job_apps_endpoint():
    print(get_job_apps())
    return json.dumps(get_job_apps())

@app.route('/api/update_job_status', methods = ['POST'])
def update_job_status_endpoint():
    data = request.form
    print(data['job_id'])
    update_job_status(data['job_id'],data['status_id'])
    return 'Updated'

@app.route('/api/remove_job', methods = ['POST'])
def remove_job_endpoint():
    data = request.form
    remove_job(data['job_id'])
    return 'Job removed'

@app.route('/api/insert_job', methods = ['POST'])
def insert_job_endpoint():
    data = request.form
    insert_job(data['job_title'],data['application_url'],data['salary'],data['company_id'])
    return 'Job added'

@app.route('/api/get_companies')
def get_companies_endpoint():
    return json.dumps(get_companies())

@app.route('/api/remove_company' , methods = ['POST'])
def remove_company_endpoint():
    data = request.form
    remove_company(data['company_id'])
    return 'Company removed'

@app.route('/api/insert_company' , methods = ['POST'])
def insert_company_endpoint():
    data = request.form
    insert_company(data['company_name'])
    return 'Company added'

