import { z } from 'zod';

// 用户认证验证
export const loginSchema = z.object({
  username: z.string().min(1, '用户名不能为空').max(50, '用户名不能超过50个字符'),
  password: z.string().min(1, '密码不能为空').min(6, '密码至少6位'),
});

export const registerSchema = z.object({
  username: z.string().min(1, '用户名不能为空').max(50, '用户名不能超过50个字符'),
  email: z.string(),
  password: z.string().min(6, '密码至少6位'),
  confirmPassword: z.string().min(1, '请确认密码'),
}).refine((data) => data.password === data.confirmPassword, {
  message: '密码不一致',
  path: ['confirmPassword'],
});

export const userUpdateSchema = z.object({
  email: z.string(),
  password: z.string(),
  confirmPassword: z.string(),
}).refine((data) => {
  if (data.password && data.confirmPassword) {
    return data.password === data.confirmPassword;
  }
  return true;
}, {
  message: '密码不一致',
  path: ['confirmPassword'],
});

// 渠道验证
export const channelCreateSchema = z.object({
  name: z.string().min(1, '渠道名称不能为空').max(100, '渠道名称不能超过100个字符'),
  channel_type: z.string().min(1, '请选择渠道类型'),
  config: z.record(z.string(), z.unknown()),
  is_active: z.boolean(),
});

export const channelUpdateSchema = z.object({
  name: z.string().min(1, '渠道名称不能为空').max(100, '渠道名称不能超过100个字符').optional(),
  channel_type: z.string().min(1, '请选择渠道类型').optional(),
  config: z.record(z.string(), z.unknown()).optional(),
  is_active: z.boolean().optional(),
});

// 分组验证
export const groupCreateSchema = z.object({
  name: z.string().min(1, '分组名称不能为空').max(100, '分组名称不能超过100个字符'),
  description: z.string().max(500, '描述不能超过500个字符'),
});

export const groupUpdateSchema = z.object({
  name: z.string().min(1, '分组名称不能为空').max(100, '分组名称不能超过100个字符').optional(),
  description: z.string().max(500, '描述不能超过500个字符').optional().or(z.literal('')),
});

// 验证工具函数
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validateURL(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

export function validateRequired(value: unknown): boolean {
  if (typeof value === 'string') {
    return value.trim().length > 0;
  }
  return value !== null && value !== undefined;
}