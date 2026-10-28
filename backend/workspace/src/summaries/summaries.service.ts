import { BadRequestException, Injectable } from '@nestjs/common';
import { PrismaService } from '../database/prisma.service';
import { SummaryQueryDto } from './summary.dto';

@Injectable()
export class SummariesService {
  constructor(private readonly prisma: PrismaService) {}

  async spending(userId: string, query: SummaryQueryDto) {
    const start = new Date(query.startDate);
    const end = new Date(query.endDate);
    if (start > end) throw new BadRequestException('startDate must be before or equal to endDate');

    const where = {
      userId,
      currency: query.currency,
      occurredAt: { gte: start, lte: end },
      ...(query.categoryId ? { categoryId: query.categoryId } : {}),
    };
    const [overall, grouped] = await Promise.all([
      this.prisma.expense.aggregate({ where, _sum: { amountMinor: true }, _count: { _all: true } }),
      this.prisma.expense.groupBy({
        by: ['categoryId'],
        where,
        _sum: { amountMinor: true },
        _count: { _all: true },
        orderBy: { categoryId: 'asc' },
      }),
    ]);
    const categories = await Promise.all(grouped.map(async (item) => {
      const category = await this.prisma.category.findFirst({
        where: { id: item.categoryId, userId },
        select: { id: true, name: true },
      });
      return {
        category,
        totalMinor: item._sum.amountMinor ?? 0,
        expenseCount: item._count._all,
      };
    }));

    return {
      currency: query.currency,
      startDate: start.toISOString(),
      endDate: end.toISOString(),
      totalMinor: overall._sum.amountMinor ?? 0,
      expenseCount: overall._count._all,
      categories,
    };
  }
}
