import poplib
from flask import Flask, render_template, request
from pop3_parse import *
import json
from db import setup_db , insert_company, insert_job, edit_job, remove_job, remove_company, get_job_apps, update_job_status, get_companies


### Main ###
app = Flask(__name__)
setup_db()


# Email enter
@app.route('/')
def index():
    return render_template('email.html')


# Future login
@app.route('/auth/login')
def auth_login():
    return render_template('/auth/login.html')


# Get emails and do all the processing
# TODO: Break this up
@app.route('/make_pop3_conn', methods=['POST'])
def pop3_connect():
    USER = request.form['email']
    PASS = request.form['password']
    HOST = request.form['host']
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

    # Loop through the retrieved emails and get their payloads
    for n in range(1, conn.stat()[0] + 1):
        msg = Parser().parsestr(b"\r\n".join(conn.retr(n)[1]).decode('utf-8'))
        payload = msg.get_payload()
        if isinstance(payload, list):
            for i, p in enumerate(payload):
                if 'plain' in p['Content-Type']:
                    # Add a company to the companies list
                    newmsg = parse(p.as_string())
                    newmsg['date'] = msg.get('Date')
                    insert_company(newmsg['companies'])

                    # Add a job using the data from the companies list
                    # TODO: insert_company needs to return the ID number of the
                    # company or it needs to insert the company if it doesn't
                    # exist AND instert the job at the same time
                    companies = get_companies()
                    for c in companies:
                        if c['company_name'] == newmsg['companies']:
                            cono = c['company_id']
                    insert_job(newmsg['roles'], 'https://', 1, cono)

                    # Get the job ID  to set the status of the job
                    apps = get_job_apps()
                    for a in apps:
                        if a['job_title'] == newmsg['roles']:
                            jobid = a['job_id']
                            break
                    stat = {'Applying': 2, 'Rejection': 7, 'Interview': 4, 'OA':6}
                    update_job_status(jobid, stat[newmsg['ratios']])

    # Retrieve all jobs and return a set of them to be rendered
    # TODO: Backend needs to see if a job exists already or something
    all_jobs = get_job_apps()
    used = set()
    jobs = []
    for a in all_jobs:
        if a['job_title'] not in used and a['status_text'] != 'None':
            used.add(a['job_title'])
            jobs.append(a)
    return render_template('job.html', jobs=jobs)


##### API Endpoints #####
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
