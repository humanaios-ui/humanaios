import { Controller, Post, Body, HttpCode } from '@nestjs/common';
import { CreateUserDto, LoginDto } from '../users/user.entity';

@Controller('auth')
export class AuthController {
  constructor() {}

  @Post('register')
  async register(@Body() createUserDto: CreateUserDto) {
    return {
      access_token: 'test-token-' + Date.now(),
      user: {
        id: 'test-user-id',
        email: createUserDto.email,
        name: createUserDto.name || 'Test User',
        role: 'admin',
        org_id: 'test-org-id'
      }
    };
  }

  @Post('login')
  @HttpCode(200)
  async login(@Body() loginDto: LoginDto) {
    return {
      access_token: 'test-token-' + Date.now(),
      user: {
        id: 'test-user-id',
        email: loginDto.email,
        name: 'Test User',
        role: 'admin',
        org_id: 'test-org-id'
      }
    };
  }

  @Post('verify')
  async verify() {
    return { valid: true };
  }
}
