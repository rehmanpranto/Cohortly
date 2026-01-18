import { v4 as uuidv4 } from 'uuid';

export const generateVerificationCode = (): string => {
  return uuidv4().replace(/-/g, '').toUpperCase().substring(0, 16);
};

export const generateTransactionId = (): string => {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substring(2, 15);
  return `TXN${timestamp}${randomStr}`.toUpperCase();
};

export const calculateRefreshTokenExpiry = (days: number): Date => {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return date;
};

export const isDeadlinePassed = (deadline: Date): boolean => {
  return new Date() > deadline;
};
