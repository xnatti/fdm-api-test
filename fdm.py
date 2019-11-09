import config as cfg
import json
import requests
import pprint

pp = pprint.PrettyPrinter(indent = 4)


fdm_password_grant = {
 'grant_type': 'password',
 'username': cfg.user,
 'password': cfg.password
}


headers = {
 'Content-Type': 'application/json'
}

response = requests.post('https://' + cfg.fdm_ip + '/api/fdm/latest/fdm/token', data=json.dumps(fdm_password_grant), headers=headers, verify=False)

