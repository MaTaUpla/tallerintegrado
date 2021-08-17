import requests, json, sys

def get_access_token():
  x = requests.post(f'https://id.twitch.tv/oauth2/token?client_id=26b5dh6hzpw4owvi5qwnen1rvya3ps&client_secret=p5ujweure88momot9uj4jwn0o7swv7&grant_type=client_credentials')

  return json.loads(x.text)["access_token"]

BASE_URL = 'https://api.twitch.tv/helix/'
ID = '26b5dh6hzpw4owvi5qwnen1rvya3ps'
TOKEN = 'p5ujweure88momot9uj4jwn0o7swv7'
HEADERS = {'Client-ID': ID, 'Authorization': f'Bearer {get_access_token()}' }
INDENT = 2



#OBTENER RESPONSE DE LA LLAMADA DE TWITCH API
def get_response(query):
  url = BASE_URL + query
  response = requests.get(url, headers=HEADERS)
  return response

#IMPRIMIR RESPONSE CON JSON

def print_response(response):
  response_json = response.json()
  print_response = json.dumps(response_json, indent=INDENT)
  return(print_response)

def get_user_query(user_login):
  return 'users?login={0}'.format(user_login)

def get_topgames():
  url = BASE_URL + 'games/top?limit=5'
  response = requests.get(url, headers=HEADERS)
  return response

def get_top():
  url = BASE_URL + 'users/follows?to_id='
  response = requests.get(url, headers=HEADERS)
  return response

def get_toplive():
  url = BASE_URL + 'streams?first=4'
  response = requests.get(url, headers=HEADERS)
  return response