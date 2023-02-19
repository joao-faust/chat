import { Server } from 'socket.io';

import JwtToken from './controllers/JwtToken';
import server from './config/server';
import Participant from './services/Participant';
import { Command, Msg, Token } from './types';

const io = new Server(server);
const participants: string[] = [];

io.on('connection', (socket) => {
  socket.on('verify-token', (data: string) => {
    const { token } = <Token>JSON.parse(data);
    const payload = JwtToken.validate(token);
    if (!payload) {
      socket.disconnect(true);
      return;
    }

    const { nickname } = payload;
    Participant.add(participants, nickname);

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
      Participant.remove(participants, nickname);
      socket.disconnect(true);
    });

    socket.on('send-msg-server', (data: string) => {
      const { msg } = <Msg>JSON.parse(data);

      if (msg.length > 0) {
        const msgBody = JSON.stringify({ msg, nickname });
        socket.broadcast.emit('send-msg-client', msgBody);
      }
    });
  });
});
