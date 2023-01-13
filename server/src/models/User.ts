import { Schema, model } from 'mongoose';

const schema = new Schema(
  {
    nickname: { type: String, required: true, min: 4, max: 20 },
    password: { type: String, required: true, max: 60 },
  },
  {
    timestamps: { createdAt: true, updatedAt: true },
    toJSON: {
      virtuals: true,
      transform(doc, ret) {
        ret.id = ret._id;
        delete ret._id;
      },
    },
    versionKey: false,
  },
);

const UserModel = model('User', schema);

export default UserModel;
