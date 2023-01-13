from user import user
from socket_client import socket_client


if __name__ == '__main__':
  token = user()
  socket_client(token)
