from core.user import user
from core.events import start_client


if __name__ == '__main__':
  token = user()
  start_client(token)
