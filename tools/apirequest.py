#!/usr/bin/python
import os
import requests
import time
time.sleep(20)

CI_BUILD_ID = os.environ.get('CI_BUILD_ID')
CI_BUILD_NAME = os.environ.get('CI_BUILD_NAME')
JENKINS_URL = os.environ.get('JENKINS_URL')

TOKEN = "Token     3b8c6198b097157e7f0bb6792b5c23ea4a67f5d9" 
status = "passed"

header = {"Authorization":TOKEN,}
url = "http://10.140.179.112:8000/upstatus/{}/".format(CI_BUILD_ID)
data = {"name":CI_BUILD_NAME,
        "status":status,
        "buildurl":JENKINS_URL,}

rst = requests.post(url,data,headers=header)