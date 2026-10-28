import { ConflictException, Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as argon2 from 'argon2';
import { UsersService } from '../users/users.service';

@Injectable()
export class AuthService {
  constructor(
    private readonly users: UsersService,
    private readonly jwt: JwtService,
  ) {}

  async register(emailInput: string, password: string) {
    const email = emailInput.trim().toLowerCase();
    if (await this.users.findByEmail(email)) {
      throw new ConflictException('Email is already registered');
    }

    const passwordHash = await argon2.hash(password, { type: argon2.argon2id });
    const user = await this.users.create(email, passwordHash);
    return { accessToken: await this.signToken(user.id, user.email), tokenType: 'Bearer' };
  }

  async login(emailInput: string, password: string) {
    const user = await this.users.findByEmail(emailInput.trim().toLowerCase());
    if (!user || !(await argon2.verify(user.passwordHash, password))) {
      throw new UnauthorizedException('Invalid email or password');
    }
    return { accessToken: await this.signToken(user.id, user.email), tokenType: 'Bearer' };
  }

  private signToken(userId: string, email: string): Promise<string> {
    return this.jwt.signAsync({ sub: userId, email });
  }
}
