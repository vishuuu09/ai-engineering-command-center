import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../database/prisma.service';
import { CreateExpenseDto, ExpenseQueryDto, UpdateExpenseDto } from './expense.dto';

@Injectable()
export class ExpensesService {
  constructor(private readonly prisma: PrismaService) {}

  async list(userId: string, query: ExpenseQueryDto) {
    const where: Prisma.ExpenseWhereInput = { userId };
    if (query.categoryId) where.categoryId = query.categoryId;
    if (query.currency) where.currency = query.currency;
    if (query.startDate || query.endDate) {
      where.occurredAt = {
        ...(query.startDate ? { gte: new Date(query.startDate) } : {}),
        ...(query.endDate ? { lte: new Date(query.endDate) } : {}),
      };
      if (query.startDate && query.endDate && new Date(query.startDate) > new Date(query.endDate)) {
        throw new BadRequestException('startDate must be before or equal to endDate');
      }
    }
    const page = query.page || 1;
    const limit = query.limit || 20;
    const [items, total] = await Promise.all([
      this.prisma.expense.findMany({
        where,
        orderBy: [{ occurredAt: 'desc' }, { id: 'desc' }],
        skip: (page - 1) * limit,
        take: limit,
        include: { category: { select: { id: true, name: true } } },
      }),
      this.prisma.expense.count({ where }),
    ]);
    return { items, page, limit, total };
  }

  async get(userId: string, id: string) {
    const expense = await this.prisma.expense.findFirst({
      where: { id, userId },
      include: { category: { select: { id: true, name: true } } },
    });
    if (!expense) throw new NotFoundException('Expense not found');
    return expense;
  }

  async create(userId: string, dto: CreateExpenseDto) {
    await this.assertOwnedCategory(userId, dto.categoryId);
    return this.prisma.expense.create({
      data: {
        userId,
        categoryId: dto.categoryId,
        amountMinor: dto.amountMinor,
        currency: dto.currency,
        description: dto.description.trim(),
        occurredAt: new Date(dto.occurredAt),
      },
      include: { category: { select: { id: true, name: true } } },
    });
  }

  async update(userId: string, id: string, dto: UpdateExpenseDto) {
    const existing = await this.prisma.expense.findFirst({ where: { id, userId } });
    if (!existing) throw new NotFoundException('Expense not found');
    if (dto.categoryId) await this.assertOwnedCategory(userId, dto.categoryId);
    await this.prisma.expense.update({
      where: { id },
      data: {
        ...(dto.categoryId ? { categoryId: dto.categoryId } : {}),
        ...(dto.amountMinor !== undefined ? { amountMinor: dto.amountMinor } : {}),
        ...(dto.currency ? { currency: dto.currency } : {}),
        ...(dto.description !== undefined ? { description: dto.description.trim() } : {}),
        ...(dto.occurredAt ? { occurredAt: new Date(dto.occurredAt) } : {}),
      },
    });
    return this.get(userId, id);
  }

  async remove(userId: string, id: string): Promise<void> {
    const result = await this.prisma.expense.deleteMany({ where: { id, userId } });
    if (!result.count) throw new NotFoundException('Expense not found');
  }

  private async assertOwnedCategory(userId: string, categoryId: string): Promise<void> {
    const category = await this.prisma.category.findFirst({ where: { id: categoryId, userId } });
    if (!category) throw new NotFoundException('Category not found');
  }
}
