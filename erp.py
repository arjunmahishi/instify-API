import requests
import re
from bs4 import BeautifulSoup
import hashlib
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)
URL_MAIN = "http://evarsity.srmuniv.ac.in/srmsip/"

def stripDownJS(text):
    return text.strip()[25:49]

def getDynamicFields(session):
    "Returns the required fields to make a post request. Return type: dict"

    loginInfo = {
        "username": "",
        "password": "",
        "captcha": ""
    }

    loginHTML = session.get(URL_MAIN).text

    soup = BeautifulSoup(loginHTML, 'html.parser')

    inputs = soup.find_all('input')
    for ele in inputs:
        if ele.has_attr('name'):
            if ele['name'] == "smhid":
                loginInfo['smhid'] = ele['value']
            if ele['name'] == "txtp":
                loginInfo['txtp'] = ele['value']
        if ele.has_attr('class') and ele['class'][0] == "inputcls":
            if ele.has_attr('placeholder') and ele['placeholder'] == "Enter above Verification Code * ":
                loginInfo['captcha-real'] = ele['id']

    loginInfo['username'] = stripDownJS(str(re.findall('.+value=username', loginHTML)[0]))
    loginInfo['password'] = stripDownJS(str(re.findall('.+value=password', loginHTML)[0]))
    loginInfo['captcha'] = stripDownJS(str(re.findall('.+value=1', loginHTML)[0]))

    return loginInfo

def login(username, password):
    session = requests.Session()
    dynamicFields = getDynamicFields(session)

    payload = {
        "hidmd5u": hashlib.md5(username).hexdigest(),
        "hidmd5p": hashlib.md5(password).hexdigest(),
        "accountname": "iamalsouser",
        "password": "iamalsouserpwd",
        "smhid": dynamicFields['smhid'],
        "txtp": dynamicFields['txtp'],
        dynamicFields['username']: username,
        dynamicFields['password']: password,
        dynamicFields['captcha']: "1",
        dynamicFields['captcha-real']: "captcha value"
    }

    headers = {'content-type': "application/x-www-form-urlencoded"}

    pp.pprint(payload)

    response = session.post(URL_MAIN, data=payload, headers=headers)

    return response.text


if __name__ == "__main__":
    login(sys.argv[1], sys.argv[2])
