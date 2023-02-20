from threading import Thread, Event


class Server(Thread):
  def __init__(self, sio, sever_url):
    Thread.__init__(self)
    self.__sio = sio
    self.__server_url = sever_url


  def run(self):
    self.__sio.connect(self.__server_url)
    self.__sio.wait()

