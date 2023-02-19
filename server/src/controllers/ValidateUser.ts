import UserModel from '../models/User';

class ValidateUser {
  private userModel;

  constructor() {
    this.userModel = UserModel;
  }

  public static nickname(nickname: string) {
    if (nickname.length < 4) {
      return 'SHORT_NICK_ERROR';
    }
    if (nickname.length > 20) {
      return 'LONG_NICK_ERROR';
    }
    return 'NO_ERRORS';
  }

  public static password(password: string, cfPasswd: string) {
    if (password.length < 8) {
      return 'SHORT_PASSWD_ERROR';
    }
    if (password.length > 20) {
      return 'LONG_PASSWD_ERROR';
    }
    if (cfPasswd !== password) {
      return 'DIFFERENT_PASSWDS_ERROR';
    }
    return 'NO_ERRORS';
  }

  public async searchNickname(nickname: string) {
    const user = await this.userModel.findOne({ nickname });
    if (user) {
      return 'EXISTS_NICK_ERROR';
    }
    return 'NO_ERRORS';
  }
}

export default ValidateUser;
