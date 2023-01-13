import UserModel from '../models/User';

export const validateNickname = (nickname: string) => {
  if (nickname.length < 4) {
    return 'SHORT_NICK_ERROR';
  }
  if (nickname.length > 20) {
    return 'LONG_NICK_ERROR';
  }
  return 'OK';
};

export const validatePassword = (password: string, cfPasswd: string) => {
  if (password.length < 8) {
    return 'SHORT_PASSWD_ERROR';
  }
  if (password.length > 20) {
    return 'LONG_PASSWD_ERROR';
  }
  if (cfPasswd !== password) {
    return 'DIFFERENT_PASSWDS_ERROR';
  }
  return 'OK';
};

export const existsNikcname = async (nickname: string) => {
  const user = await UserModel.findOne({ nickname });
  if (user) {
    return 'EXISTS_NICK_ERROR';
  }
  return 'OK';
};
