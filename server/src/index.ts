import 'dotenv/config';

import dbConnect from './config/dbConfig';
import server from './config/server';
import './services/socketServer';

const PORT = <string>process.env.PORT;

dbConnect().then(() => {
  server.listen(PORT, () => {
    console.log(`Running on port: ${PORT}`);
  });
});
