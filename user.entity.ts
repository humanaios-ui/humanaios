export interface User {
  id: string;
  org_id: string;
  email: string;
  password_hash?: string;
  name: string | null;
  role: 'admin' | 'operator' | 'viewer';
  auth_provider: 'email' | 'google' | 'github';
  avatar_url: string | null;
  is_active: boolean;
  last_login_at: Date | null;
  created_at: Date;
  updated_at: Date;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: 'free' | 'starter' | 'pro' | 'enterprise';
  settings: Record<string, any>;
  created_at: Date;
  updated_at: Date;
}

export type CreateUserDto = {
  email: string;
  password: string;
  name?: string;
  org_name?: string;
};

export type LoginDto = {
  email: string;
  password: string;
};
