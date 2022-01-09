from os import read
import poplib
import yaml
from email.parser import Parser
from string import punctuation
from thefuzz import fuzz
from thefuzz import process


def P(a): print(a)


def smash(msg):
    return " ".join(
        [i[:-1] if i[-1] == '=' else i for i in filter(None, msg.splitlines())])


def parse(msg):
    m = smash(msg)
    role = [
        "interest in",
        "application for",
        "position",
        "applying to",
        "interest in our",
        "role",
        "applying to the"
    ]

    company = [
        "role at",
        "applying to",
        "apply to",
        "opportunity at",
        "interest in",
        "role with"
    ]

    applying = [
        "applying",
        "application",
        "interest in",
    ]

    rejection = [
        "not be moving forward",
        "not being considered for"
    ]

    interview = [
        "interview"
    ]

    oa = [
        "hackerrank",
        "online assessment"
    ]

    acceptance = [
        "offer"
        "congratulations"
    ]


    roles = parse_data(role, m, 'roles')
    companies = parse_data(company, m, 'companies')
    ratios = {}
    ratios['applying'] = parse_status(applying, m, 'applying')
    ratios['rejection'] = parse_status(rejection, m, 'rejection')
    ratios['interview'] = parse_status(interview, m, 'interview')
    ratios['oa'] = parse_status(oa, m, 'oa')
    ratios['acceptance'] = parse_status(acceptance, m, 'acceptance')
    ratios = dict(sorted(ratios.items(), key=lambda item: item[1], reverse=True))
    P(ratios)


def parse_data(data, msg, tag):
    data_found = []
    for d in data:
        idx = msg.find(d)
        if idx > -1:
            new_role = ''
            for i in range(idx+len(d), len(msg)):
                if msg[i] not in punctuation: new_role += msg[i]
                else: break

            # Cleanup
            new_role = new_role.replace('To', '').replace('the', '')
            new_role = new_role.strip()
            if new_role != '': data_found.append(new_role)

    P(f'Found the following {tag}:')
    for i in data_found: P(f'    "{i}"')
    return data_found


def parse_status(stat, msg, tag=None):
    return sum(fuzz.partial_ratio(msg,i) for i in stat) / len(stat)


# Read from yaml
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
conn = poplib.POP3_SSL(HOST)
P(f'Welcome message:\n{conn.getwelcome().decode("utf-8")}\n')
conn.user(USER)
conn.pass_(PASS)
P(f'Connected user "{USER}" (Password: {"*"*len(PASS)}) to "{HOST}"')
P(f'Inbox stats: {conn.stat()[0]} messages, {conn.stat()[1]} bytes\n\n')

# Retrieve the nth email
for n in range(conn.stat()[0], 0, -1):
    P(f'Reading message #{n}')
    try:
        resp, lines, oct = conn.retr(n)
        lines = b"\r\n".join(lines).decode('utf-8')
    except:
        exit(f'Could not retrieve message #{n}, maybe it doesn\'t exist?')

    msg = Parser().parsestr(lines)
    P(f'   Date: {msg.get("Date")}')
    P(f'   From: {msg.get("From")}')
    P(f'Subject: {msg.get("Subject")}')

    # Get the text/plain payload only, unless there's only one option
    payload = msg.get_payload()
    if isinstance(payload, list):
        for i, p in enumerate(payload):
            if 'plain' in p['Content-Type']:
                parse(p.as_string())
    else:
        P('=== Entire message (trimmed to 240 chars) ===')
        P(f'Type: {msg["Content-Type"]}')
        P(payload[:241])
        # Parse for keywords here, may need BS4 or something
    P('\n')
