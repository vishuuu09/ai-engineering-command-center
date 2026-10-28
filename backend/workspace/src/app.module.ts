import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { CategoriesModule } from './categories/categories.module';
import { requestLoggingMiddleware } from './common/request-logging.middleware';
import { PrismaModule } from './database/prisma.module';
import { ExpensesModule } from './expenses/expenses.module';
import { HealthModule } from './health/health.module';
import { environmentSchema } from './config/env.validation';
import { SummariesModule } from './summaries/summaries.module';
import { UsersModule } from './users/users.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true, validationSchema: environmentSchema }),
    PrismaModule,
    UsersModule,
    AuthModule,
    CategoriesModule,
    ExpensesModule,
    SummariesModule,
    HealthModule,
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(requestLoggingMiddleware).forRoutes('*');
  }
}
