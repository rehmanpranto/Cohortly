import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import config from '../config/config';
import { UserRole } from '@prisma/client';

export const hashPassword = async (password: string): Promise<string> => {
  return bcrypt.hash(password, 10);
};

export const comparePassword = async (
  password: string,
  hash: string
): Promise<boolean> => {
  return bcrypt.compare(password, hash);
};

export const generateAccessToken = (payload: {
  id: string;
  email: string;
  role: UserRole;
}): string => {
  return jwt.sign(payload, config.jwt.accessSecret as string, {
    expiresIn: config.jwt.accessExpiry,
  });
};

export const generateRefreshToken = (payload: {
  id: string;
  email: string;
  role: UserRole;
}): string => {
  return jwt.sign(payload, config.jwt.refreshSecret as string, {
    expiresIn: config.jwt.refreshExpiry,
  });
};

export const verifyRefreshToken = (token: string): {
  id: string;
  email: string;
  role: UserRole;
} => {
  return jwt.verify(token, config.jwt.refreshSecret) as {
    id: string;
    email: string;
    role: UserRole;
  };
};
