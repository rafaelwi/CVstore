import poplib
from flask import Flask, render_template, request
from db import setup_db , insert_company, insert_job,edit_job,remove_job,remove_company,insert_job_app,remove_job_app
from pop3_parse import *

app = Flask(__name__)

setup_db()
#insert_company("Facebook")
#insert_job("Pussy magnet","http://facebook.com",6969,4)
#insert_job_app(3,1)
remove_job_app(5)
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
    messages=''
    for n in range(conn.stat()[0], 0, -1):
        messages += f'Message #{n}<br>'
        msg = Parser().parsestr(b"\r\n".join(conn.retr(n)[1]).decode('utf-8'))
        messages += f'   Date: {msg.get("Date")}<br>'
        messages += f'   From: {msg.get("From")}<br>'
        messages += f'Subject: {msg.get("Subject")}<br>'

        payload = msg.get_payload()
        if isinstance(payload, list):
            for i, p in enumerate(payload):
                if 'plain' in p['Content-Type']:
                    messages += parse(p.as_string())



    return f"""
        Connected user "{USER}" (Password: {"*"*len(PASS)}) to "{HOST}"<br>
        Inbox stats: {conn.stat()[0]} messages, {conn.stat()[1]} bytes<br><br>
        Messages:<br>
        {messages}
    """


