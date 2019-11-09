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


def checkTokenValidity():
 if (datetime.today() - accessTokens['datetime']).seconds > accessTokens['expires_in']:
  print('token expiired')
 if (datetime.today() - accessTokens['datetime']).seconds > accessTokens['refresh_expires_in']:
  print('refresh token expiired')


def updateHeaders():
 headers['Authorization'] = 'Bearer ' + accessTokens['access_token']

def refreshToken():
 fdm_tokenrefresh_grant = {
  'grant_type': 'refresh_token',
  'refresh_token': accessTokens['refresh_token']
 }
 response = requests.post('https://' + cfg.fdm_ip + '/api/fdm/latest/fdm/token', data=json.dumps(fdm_tokenrefresh_grant), headers=headers, verify=False)
 responseJSON = json.loads(bytes.decode(response.content))
 for item in responseJSON:
  accessTokens[item] = responseJSON[item]
 accessTokens['datetime'] = datetime.today()
