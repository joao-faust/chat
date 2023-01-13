from requests import post
from getpass import getpass
from json import loads
from enum import Enum
from sys import exit

from custom_print import custom_print


# a enum for errors, because the api returns the type of the error and not the error message
class Errors(Enum):
  SHORT_NICK_ERROR = 'Min length allowed in nickname is 4'
  LONG_NICK_ERROR = 'Max length allowed in nickname is 20'
  SHORT_PASSWD_ERROR = 'Min length allowed in password is 8'
  LONG_PASSWD_ERROR = 'Max length allowed in password is 72'
  DIFFERENT_PASSWDS_ERROR = "Passwords don't match"
  CREDENTIALS_ERROR = 'Invalid credentials'
  EXISTS_NICK_ERROR = 'Nickname already exists'


def nickname_input():
  isValid, nickname = False, None
  while not isValid:
    nickname = input('Nickname> ')
    if len(nickname) < 4:
      print(Errors.SHORT_NICK_ERROR.value)
    elif len(nickname) > 20:
      print(Errors.LONG_NICK_ERROR.value)
    else:
      isValid = True
  return nickname


def password_input():
  isValid, password = False, None
  while not isValid:
    password = getpass('Password> ')
    if len(password) < 8:
      print(Errors.SHORT_PASSWD_ERROR.value)
    elif len(password) > 72:
      print(Errors.LONG_PASSWD_ERROR.value)
    else:
      isValid = True
  return password


def cfpassword_input(password):
  isValid, cfpassword = False, None
  while not isValid:
    cfpassword = getpass('Confirm Password> ')
    if cfpassword != password:
      print(Errors.DIFFERENT_PASSWDS_ERROR.value)
    else:
      isValid = True
  return cfpassword


def login(api_url):
  custom_print('login', 10, '\n', '\n')
  try:
    nickname = input('Nickname> ')
    password = getpass('Passoword> ')
  except KeyboardInterrupt:
    exit(0)

  data = {'nickname': nickname, 'password': password}

  result = post(f'{api_url}/user/login', json=data)
  dic = loads(result.content)
  if result.status_code == 400:
    print(Errors[dic['type']].value)
    return login(api_url)

  return result.headers['auth-token']


def add_user(api_url):
  custom_print('register', 10, '\n', '\n')
  try:
    nickname = nickname_input()
    password = password_input()
    cfpassword = cfpassword_input(password)
  except KeyboardInterrupt:
    exit(0)

  data = {'nickname': nickname, 'password': password, 'cfpassword': cfpassword}
  result = post(f'{api_url}/user/add', json=data)
  dic = loads(result.content)

  if result.status_code == 400:
    print(Errors[dic['type']].value)
    return add_user(api_url)

  token = login(api_url)
  return token


# the main function
def user():
  action_type = None
  while action_type != 'y' and action_type != 'n':
    try:
      action_type = input('Do you already have an account? Y or N> ').lower()
    except KeyboardInterrupt:
      exit(0)

  api_url = 'http://localhost:3000'
  if action_type == 'y':
    token = login(api_url)
    return token

  token = add_user(api_url)
  return token
