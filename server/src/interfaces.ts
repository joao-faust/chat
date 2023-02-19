export interface IAddUser {
  nickname: string;
  password: string;
  cfpassword: string;
}

export interface ILoginUser {
  nickname: string;
  password: string;
}

export interface IUserPayload {
  nickname: string;
  expire: number;
  iat: number;
}
