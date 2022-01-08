import poplib
import yaml

def P(a): print(a)

# Read from yaml
# Note for gmail, you may want to use `recent:myemailhere@gmail.com` to get all
# messages from the last month
try:
    with open('secrets/email.yaml') as f:
        y = yaml.safe_load(f)
        HOST = y['host']
        USER = y['user']
        PASS = y['pass']
except:
    P('Missing file "secrets/email.yaml"!')
    P('Please create the file with fields:')
    P('host: pop.email.server.com')
    P('user: my@email.com')
    P('pass: P4SSW0RD')
    P('The secrets/ directory has been placed in .gitignore, so it will not be published')
    exit()

# POP example: get the number of messages in their inbox
P(f'Establishing POP3 SSL connection with {HOST}')
try:
    conn = poplib.POP3_SSL(HOST)
    P(f'Welcome message:\n{conn.getwelcome().decode("utf-8")}\n')

    conn.user(USER)
    conn.pass_(PASS)

    P(f'Connected user "{USER}" (Password: {"*"*len(PASS)}) to "{HOST}"')
    P(f'Inbox stats: {conn.stat()[0]} messages, {conn.stat()[1]} bytes')
except:
    P(f'Could not establish a connection with {HOST}')
    P('This could be for one of the following reasons:')
    P('- The host only supports POP3 and not POP3 SSL, please ensure that the host given is POP3 SSL')
    P('- Email and/or password are incorrect, try in a browser first')
    P('- POP3 has not been enabled for your email')
    P('- Gmail: Enable "Less secure app access" at https://myaccount.google.com/lesssecureapps')
    exit()
