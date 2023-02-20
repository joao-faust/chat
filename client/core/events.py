import socketio
import json
import sys

from core.threads import Server
from utils.custom_print import custom_print

sio = socketio.Client()
jwt_token = None


# when a user connects to the server, a event is emitted to verify the token integrity
@sio.on('connect')
def connect():
  sio.emit('verify-token', json.dumps({'token': jwt_token}))


@sio.on('show-help')
def show_help(data):
  dic = json.loads(data)
  for command in dic['help']:
    print(command)
  print()


@sio.on('show-participants')
def show_participants(data):
  custom_print('participants', 8)
  dic = json.loads(data)
  for p in dic['participants']:
    print(p)
  custom_print('', 14, '', '\n')


@sio.on('client-disconnected')
def client_disconnected(data):
  dic = json.loads(data)
  print(dic['msg'])


@sio.on('joined-chat')
def joined_chat(data):
  dic = json.loads(data)
  print(dic['msg'])


@sio.on('send-msg-client')
def send_msg_client(data):
  dic = json.loads(data)
  print('{}> {}\n'.format(dic['nickname'], dic['msg']))


# when a user connects to the server, it shows them a message indicating
# that they can start sending messages
def send_events_to_server():
  print('\nType "!help" if you need it')
  while True:
    try:
      msg = input('\n')
    except:
      break
    try:
      if msg == '!exit':
        sio.emit('exit-chat')
        break
      elif msg == '!help':
        sio.emit('help', json.dumps({'command': '!help'}))
      elif msg == '!on':
        sio.emit('participants', json.dumps({'command': '!on'}))
      else:
        data = json.dumps({'msg': msg})
        sio.emit('send-msg-server', data)
    except:
      break


# main function
def start_client(token):
  global jwt_token
  jwt_token = token

  server = Server(sio, 'http://localhost:3000')
  server.start()

  send_events_to_server()
