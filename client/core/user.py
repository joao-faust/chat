import json
from requests import post
from getpass import getpass

from util.Error import Error
from util.custom_print import custom_print


# Asks for the nickname until a valid nickname is entered
def ask_for_nickname():
  isValid, nickname = False, None
  while not isValid:
    nickname = input('Nickname> ')
    if len(nickname) < 4:
      print(Error.SHORT_NICK_ERROR.value)
    elif len(nickname) > 20:
      print(Error.LONG_NICK_ERROR.value)
    else:
      isValid = True
  return nickname


# Asks for the passowrd until a valid password is entered
def aks_for_password():
  isValid, password = False, None
  while not isValid:
    password = getpass('Password> ')
    if len(password) < 8:
      print(Error.SHORT_PASSWD_ERROR.value)
    elif len(password) > 72:
      print(Error.LONG_PASSWD_ERROR.value)
    else:
      isValid = True
  return password


# Asks for the confirm password until it matches the password
def ask_for_cfpassword(password):
  isValid, cfpassword = False, None
  while not isValid:
    cfpassword = getpass('Confirm Password> ')
    if cfpassword != password:
      print(Error.DIFFERENT_PASSWDS_ERROR.value)
    else:
      isValid = True
  return cfpassword


def login(api_url):
  custom_print('login', 10, '\n', '\n')
  nickname = input('Nickname> ')
  password = getpass('Passoword> ')

  data = {'nickname': nickname, 'password': password}

  result = post(f'{api_url}/user/login', json=data)
  dic = json.loads(result.content)
  if result.status_code == 400:
    print(Error[dic['type']].value)
    return login(api_url)

  return result.headers['auth-token']


def add_user(api_url):
  custom_print('register', 10, '\n', '\n')
  nickname = ask_for_nickname()
  password = aks_for_password()
  cfpassword = ask_for_cfpassword(password)

  data = {'nickname': nickname, 'password': password, 'cfpassword': cfpassword}
  result = post(f'{api_url}/user/add', json=data)
  dic = json.loads(result.content)

  if result.status_code == 400:
    print(Error[dic['type']].value)
    return add_user(api_url)

  token = login(api_url)
  return token


# main function
def user():
  action_type = None
  while action_type != 'y' and action_type != 'n':
    action_type = input('Do you already have an account? Y or N> ').lower()

  api_url = 'http://localhost:3000'
  if action_type == 'y':
    token = login(api_url)
    return token

  token = add_user(api_url)
  return token
