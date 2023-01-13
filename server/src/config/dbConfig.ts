import { connect as connectDb, connection, set } from 'mongoose';

set('strictQuery', true);

const DB_URI = <string>process.env.DB_URI;

const connect = async () => {
  try {
    await connectDb(DB_URI);
  } catch (error) {
    console.error(error);
  }
};

connection.once('open', () => console.log('Database connected'));
connection.on('error', (error) => console.error(error));

export default connect;
