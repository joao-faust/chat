import 'dotenv/config';

import dbConnect from './config/dbConfig';
import server from './config/server';
import './events';

const PORT = <string>process.env.PORT;

dbConnect().then(() => {
  server.listen(PORT, () => {
    console.log(`Running on port: ${PORT}`);
  });
});
