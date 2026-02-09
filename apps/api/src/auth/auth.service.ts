import { Injectable, ConflictException, Inject, forwardRef, OnModuleInit } from '@nestjs/common';
import { ModuleRef } from '@nestjs/core';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import { CreateUserDto, User } from '../users/user.entity';

@Injectable()
export class AuthService implements OnModuleInit {
  private jwtService: JwtService;

  constructor(
    @Inject(forwardRef(() => UsersService))
    private usersService: UsersService,
    private moduleRef: ModuleRef,
  ) {
    console.log('AuthService constructor called!');
    console.log('  - usersService:', !!this.usersService);
  }

  async onModuleInit() {
    this.jwtService = this.moduleRef.get(JwtService, { strict: false });
    console.log('AuthService onModuleInit - jwtService:', !!this.jwtService);
  }

  async validateUser(email: string, password: string): Promise<any> {
    const user = await this.usersService.findByEmail(email);
    if (!user) {
      return null;
    }

    const isPasswordValid = await this.usersService.validatePassword(user, password);
    if (!isPasswordValid) {
      return null;
    }

    const { password_hash, ...result } = user;
    return result;
  }

  async login(user: User) {
    await this.usersService.updateLastLogin(user.id);

    const payload = { email: user.email, sub: user.id, role: user.role };
    return {
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        org_id: user.org_id,
      },
    };
  }

  async register(createUserDto: CreateUserDto) {
    const existingUser = await this.usersService.findByEmail(createUserDto.email);
    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }

    const user = await this.usersService.create(createUserDto);
    return this.login(user);
  }
}
