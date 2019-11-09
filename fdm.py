import config as cfg
import json
import requests
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent = 4)


fdm_password_grant = {
 'grant_type': 'password',
 'username': cfg.user,
 'password': cfg.password
}


headers = {
 'Content-Type': 'application/json'
}

accessTokens = {}

def getNewTokens():
 response = requests.post('https://' + cfg.fdm_ip + '/api/fdm/latest/fdm/token', data=json.dumps(fdm_password_grant), headers=headers, verify=False)
 responseJSON = json.loads(bytes.decode(response.content))
 for item in responseJSON:
  accessTokens[item] = responseJSON[item]
 accessTokens['datetime'] = datetime.today()


