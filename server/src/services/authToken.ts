import { verify } from 'jsonwebtoken';

interface IUserPayload {
  nickname: string;
  expire: number;
  iat: number;
}

const auth = (token: string) => {
  const TOKEN_SECRET = <string>process.env.TOKEN_SECRET;
  try {
    const decoded = <IUserPayload>verify(token, TOKEN_SECRET);
    return decoded;
  } catch (error) {
    return null;
  }
};

export default auth;
