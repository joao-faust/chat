import { verify } from 'jsonwebtoken';

import { IUserPayload } from '../interfaces';

class JwtToken {
  public static validate(token: string) {
    const TOKEN_SECRET = <string>process.env.TOKEN_SECRET;
    try {
      const decoded = <IUserPayload>verify(token, TOKEN_SECRET);
      return decoded;
    } catch (error) {
      return null;
    }
  }
}

export default JwtToken;
