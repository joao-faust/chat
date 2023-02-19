import json
from threading import Thread


class Server(Thread):
  def __init__(self, sio, sever_url):
    self.__sio = sio
    self.__server_url = sever_url
    Thread.__init__(self)


  def run(self):
    self.__sio.connect(self.__server_url)
    self.__sio.wait()


class Message(Thread):
  def __init__(self, sio):
    self.__sio = sio
    Thread.__init__(self)


  # when a user connects to the server, it shows them a message indicating
  # that they can start sending messages
  def run(self):
    print('\nType "!help" if you need it')

    while True:
      msg = input('\n')
      try:
        if msg == '!exit':
          self.__sio.emit('exit-chat')
          break
        elif msg == '!help':
          self.__sio.emit('help', json.dumps({'command': '!help'}))
        elif msg == '!on':
          self.__sio.emit('participants', json.dumps({'command': '!on'}))
        else:
          data = json.dumps({'msg': msg})
          self.__sio.emit('send-msg-server', data)
      except:
        break
