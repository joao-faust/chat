import json
import sys

from requests import post
from getpass import getpass

from utils.Error import Error
from utils.custom_print import custom_print

api_url = 'http://localhost:3000'


# Asks for the nickname until a valid nickname is entered
def ask_for_nickname():
  isValid = False
  nickname = ''
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
  isValid = False
  password = ''
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
  isValid = False
  cfpassword = ''
  while not isValid:
    cfpassword = getpass('Confirm Password> ')
    if cfpassword != password:
      print(Error.DIFFERENT_PASSWDS_ERROR.value)
    else:
      isValid = True
  return cfpassword


def login():
  custom_print('login', 10, '\n', '\n')
  try:
    nickname = input('Nickname> ')
    password = getpass('Passoword> ')
  except:
    sys.exit(0)

  data = {'nickname': nickname, 'password': password}
  result = post(f'{api_url}/user/login', json=data)
  dic = json.loads(result.content)

  if result.status_code == 400:
    print(Error[dic['type']].value)
    return login()

  with open('jwt_token.txt', 'w') as file:
    jwt_token = result.headers['auth-token']
    file.write(jwt_token)


def add_user():
  custom_print('register', 10, '\n', '\n')
  try:
    nickname = ask_for_nickname()
    password = aks_for_password()
    cfpassword = ask_for_cfpassword(password)
  except:
    sys.exit(0)

  data = {'nickname': nickname, 'password': password, 'cfpassword': cfpassword}
  result = post(f'{api_url}/user/add', json=data)
  dic = json.loads(result.content)

  if result.status_code == 400:
    print(Error[dic['type']].value)
    return add_user()
  login()


# main function
def user():
  action_type = ''
  while action_type != 'y' and action_type != 'n':
    try:
      action_type = input('Do you already have an account? Y or N> ').lower()
    except:
      sys.exit(0)

  if action_type == 'y':
    login()
    return
  add_user()
