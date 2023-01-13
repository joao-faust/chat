import { Request, Response } from 'express';
import { hashSync, compareSync } from 'bcryptjs';
import { sign } from 'jsonwebtoken';

import UserModel from '../models/User';
import {
  validateNickname,
  validatePassword,
  existsNikcname,
} from './userValidations';

interface IAddUser {
  nickname: string;
  password: string;
  cfpassword: string;
}

interface ILoginUser {
  nickname: string;
  password: string;
}

const stringify = JSON.stringify;

export const addUser = async (req: Request, res: Response) => {
  const { nickname, password, cfpassword } = <IAddUser>req.body;

  const nicknameValidation = validateNickname(nickname);
  if (nicknameValidation !== 'OK') {
    return res.status(400).send(stringify({ type: nicknameValidation }));
  }
  const existsNikcValidation = await existsNikcname(nickname);
  if (existsNikcValidation !== 'OK') {
    return res.status(400).send(stringify({ type: existsNikcValidation }));
  }
  const passwordValidation = validatePassword(password, cfpassword);
  if (passwordValidation !== 'OK') {
    return res.status(400).send(stringify({ type: passwordValidation }));
  }

  const hashed = hashSync(password, 10);
  try {
    const user = new UserModel({ nickname, password: hashed });
    await user.save();
  } catch (error) {
    return res.status(500).send(stringify('Internal Error'));
  }

  res.status(201).send(JSON.stringify({ type: 'add_user' }));
};

export const login = async (req: Request, res: Response) => {
  const { nickname, password } = <ILoginUser>req.body;

  const user = await UserModel.findOne({ nickname });
  if (user && compareSync(password, user.password)) {
    const TOKEN_SECRET = <string>process.env.TOKEN_SECRET;
    const token = sign({ nickname }, TOKEN_SECRET);

    res.header('auth-token', token);
    return res.send(stringify({ type: 'OK' }));
  }

  res.status(400).send(stringify({ type: 'CREDENTIALS_ERROR' }));
};
