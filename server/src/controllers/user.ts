import { Request, Response } from 'express';
import { hashSync, compareSync } from 'bcryptjs';
import { sign } from 'jsonwebtoken';

import UserModel from '../models/User';
import ValidateUser from './ValidateUser';
import { IAddUser, ILoginUser } from '../interfaces';

class User {
  private userModel;
  private validateUser;

  constructor() {
    this.userModel = UserModel;
    this.validateUser = new ValidateUser();
  }

  public add = async (req: Request, res: Response) => {
    const { nickname, password, cfpassword } = <IAddUser>req.body;

    const nicknameVal = ValidateUser.nickname(nickname);
    if (nicknameVal !== 'NO_ERRORS') {
      return res.status(400).send(JSON.stringify({ type: nicknameVal }));
    }
    const existsNikc = await this.validateUser.searchNickname(nickname);
    if (existsNikc !== 'NO_ERRORS') {
      return res.status(400).send(JSON.stringify({ type: existsNikc }));
    }
    const passwordVal = ValidateUser.password(password, cfpassword);
    if (passwordVal !== 'NO_ERRORS') {
      return res.status(400).send(JSON.stringify({ type: passwordVal }));
    }

    const hashed = hashSync(password, 10);
    try {
      const user = new this.userModel({ nickname, password: hashed });
      await user.save();
    } catch (error) {
      return res.status(500).send(JSON.stringify('Internal Error'));
    }

    res.status(201).send(JSON.stringify({ type: 'add_user' }));
  };

  public login = async (req: Request, res: Response) => {
    const { nickname, password } = <ILoginUser>req.body;

    const user = await this.userModel.findOne({ nickname });
    if (user && compareSync(password, user.password)) {
      const TOKEN_SECRET = <string>process.env.TOKEN_SECRET;
      const token = sign({ nickname }, TOKEN_SECRET);

      res.header('auth-token', token);
      return res.send(JSON.stringify({ type: 'login' }));
    }

    res.status(400).send(JSON.stringify({ type: 'CREDENTIALS_ERROR' }));
  };
}

export default User;
