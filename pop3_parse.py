from string import punctuation
from thefuzz import fuzz
from email.parser import Parser


# Makes the message one single line
def smash(msg):
    return " ".join(
        [i[:-1] if i[-1] == '=' else i for i in filter(None, msg.splitlines())])


# Parses the company, job title, and status of a job
def parse(msg):
    m = smash(msg)

    # TODO: Move these arrays into some file
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

    # Parse job title and company
    roles = parse_data(role, m, 'roles')
    companies = parse_data(company, m, 'companies')

    # Parse job status and select the highest one
    # TODO: Use the ratios given and display to the user "we think that this
    # is 77% an OA, can you confirm?"
    ratios = {}
    ratios['Applying'] = parse_status(applying, m, 'applying')
    ratios['Rejection'] = parse_status(rejection, m, 'rejection')
    ratios['Interview'] = parse_status(interview, m, 'interview')
    ratios['OA'] = parse_status(oa, m, 'oa')
    ratios['Acceptance'] = parse_status(acceptance, m, 'acceptance')
    status = max(ratios, key=ratios.get)

    obj = {'roles':roles, 'companies':companies, 'ratios':status, 'message':m}
    return obj


# Parse through msg with the given data arr
def parse_data(data, msg, tag):
    data_found = ""
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
            if new_role != '': data_found += new_role + ' '
    return data_found


# Parse job status using fuzzy matching
def parse_status(stat, msg, tag=None):
    return sum(fuzz.partial_ratio(msg,i) for i in stat) / len(stat)
