import { Server } from 'socket.io';

import authToken from './authToken';
import server from '../config/server';

type Msg = { msg: string };
type Token = { token: string };
type Command = { command: string };

const io = new Server(server);
const participants: string[] = [];

const addUser = (nickname: string) => {
  const index = participants.indexOf(nickname);
  index === -1 ? participants.push(nickname) : '';
};

const removeUser = (nickname: string) => {
  const index = participants.indexOf(nickname);
  index !== -1 ? participants.splice(index, 1) : '';
};

io.on('connection', (socket) => {
  socket.on('verify-token', (data: string) => {
    const { token } = <Token>JSON.parse(data);
    const payload = authToken(token);
    if (!payload) {
      socket.disconnect(true);
      return;
    }

    const { nickname } = payload;
    addUser(nickname);

    // informs the user that they can start sending messages
    socket.emit('start-sending-msg');

    const msg = `${nickname} joined the chat\n`;
    socket.broadcast.emit('joined-chat', JSON.stringify({ msg }));

    socket.on('help', (data: string) => {
      const { command } = <Command>JSON.parse(data);
      if (command !== '!help') {
        return;
      }

      const help = [
        '!exit - exit from the chat',
        '!on - show the participants',
      ];
      socket.emit('show-help', JSON.stringify({ help }));
    });

    socket.on('participants', (data: string) => {
      const { command } = <Command>JSON.parse(data);
      if (command !== '!on') {
        return;
      }

      socket.emit('show-participants', JSON.stringify({ participants }));
    });

    socket.on('exit-chat', () => {
      const msg = `${payload.nickname} exit from the chat\n`;
      socket.broadcast.emit('client-disconnected', JSON.stringify({ msg }));
      removeUser(nickname);
      socket.disconnect(true);
    });

    // sends a message to everybody on the chat
    socket.on('send-msg-server', (data: string) => {
      const { msg } = <Msg>JSON.parse(data);

      if (msg.length > 0) {
        const msgBody = JSON.stringify({ msg, nickname });
        socket.broadcast.emit('send-msg-client', msgBody);
      }
    });
  });
});
