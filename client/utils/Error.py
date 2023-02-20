from enum import Enum


# enum for errors, because the api returns the type of the error and not the error message
class Error(Enum):
  SHORT_NICK_ERROR = 'Min length allowed in nickname is 4'
  LONG_NICK_ERROR = 'Max length allowed in nickname is 20'
  SHORT_PASSWD_ERROR = 'Min length allowed in password is 8'
  LONG_PASSWD_ERROR = 'Max length allowed in password is 72'
  DIFFERENT_PASSWDS_ERROR = "Passwords don't match"
  CREDENTIALS_ERROR = 'Invalid credentials'
  EXISTS_NICK_ERROR = 'Nickname already exists'
