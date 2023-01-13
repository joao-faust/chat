import socketio
from json import loads, dumps

from custom_print import custom_print

sio = socketio.Client()
user = {
  'token': None,
}


@sio.on('show-help')
def show_help(data):
  dic = loads(data)
  for command in dic['help']:
    print(command)
  print()


@sio.on('show-participants')
def show_participants(data):
  custom_print('participants', 8)
  dic = loads(data)
  for p in dic['participants']:
    print(p)
  custom_print('', 14, '', '\n')


# when a user connects to the server, a event is emitted to verify the token integrity
@sio.on('connect')
def connect():
  sio.emit('verify-token', dumps({'token': user['token']}))


@sio.on('disconnect-client')
def disconnect_client():
  sio.disconnect()


@sio.on('client-disconnected')
def client_disconnected(data):
  dic = loads(data)
  print(dic['msg'])


@sio.on('joined-chat')
def joined_chat(data):
  dic = loads(data)
  print(dic['msg'])


# when a user connects to the server, it shows them a message indicating
# that they can start sending messages
@sio.on('start-sending-msg')
def start_sending_msg():
  print('\nType "!help" if you need it')

  while True:
    try:
      msg = input('\n')
    except EOFError:
      sio.emit('exit-chat')
      break
    if msg == '!exit':
      sio.emit('exit-chat')
      break
    elif msg == '!help':
      sio.emit('help', dumps({'command': '!help'}))
    elif msg == '!on':
      sio.emit('participants', dumps({'command': '!on'}))
    else:
      data = dumps({'token': user['token'], 'msg': msg})
      sio.emit('send-msg-server', data)


@sio.on('send-msg-client')
def send_msg_client(data):
  dic = loads(data)
  print('{}> {}\n'.format(dic['nickname'], dic['msg']))


# the main function
def socket_client(token):
  user['token'] = token
  server_url = 'http://localhost:3000'

  try:
    sio.connect(server_url)
    sio.wait()
  except KeyboardInterrupt:
    return
