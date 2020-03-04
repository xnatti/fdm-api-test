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
fdm_info = {}
fdm_info['baseURI'] = 'https://' + cfg.fdm_ip + '/api/fdm/latest'


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



def getPolicyID():
 response = requests.get('https://' + cfg.fdm_ip + '/api/fdm/latest/policy/accesspolicies', headers=headers, verify=False)
 responseJSON = json.loads(bytes.decode(response.content))
 fdm_info['policy_URI'] = responseJSON['items'][0]['links']['self']
 fdm_info['policy_ID'] = responseJSON['items'][0]['id']


def getTimeRangeObjects():
 response = requests.get(fdm_info['baseURI'] + '/object/timeranges', headers=headers, verify=False)
 return response


def addAbsoluteTimeRange(start,end,name):
 '''
  start and end dates are in the form of YYYY-MM-DDTHH:MM
 '''
 path = '/object/timeranges'
 timerange = {
  'name': name,
  'description': 'made by api',
  'effectiveStartDateTime': start,
  'effectiveEndDateTime': end,
  'type': 'timerangeobject'
 }
 response = requests.post(fdm_info['baseURI'] + path, data=json.dumps(timerange), headers=headers, verify=False)



def addRecurrenceTimeRange():
 path = '/object/timeranges'
 timerange = {
  'name': name,
  'description': 'made by api',
  'recurrenceList': [
   {
    'days': [
     'MON'
    ],
   'recurrenceType': 'DAILY_INTERVAL',
   'dailyStartTime': '22:00',
   'dailyEndTime': '23:00',
   'type': 'recurrence'
   }
  ], 
  'type': 'timerangeobject'
 }




getNewTokens()
updateHeaders()
getPolicyID()



