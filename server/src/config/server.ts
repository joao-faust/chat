import express from 'express';
import http from 'http';
import bodyParser from 'body-parser';

import userRouter from '../routes/user';

const app = express();
const server = http.createServer(app);

app.use('/user', bodyParser.json(), userRouter);

export default server;
