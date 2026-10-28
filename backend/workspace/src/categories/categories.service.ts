import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../database/prisma.service';

@Injectable()
export class CategoriesService {
  constructor(private readonly prisma: PrismaService) {}

  list(userId: string) {
    return this.prisma.category.findMany({ where: { userId }, orderBy: { name: 'asc' } });
  }

  create(userId: string, name: string) {
    return this.prisma.category.create({ data: { userId, name: name.trim() } });
  }

  async update(userId: string, id: string, name: string) {
    const result = await this.prisma.category.updateMany({
      where: { id, userId },
      data: { name: name.trim() },
    });
    if (!result.count) throw new NotFoundException('Category not found');
    return this.prisma.category.findFirstOrThrow({ where: { id, userId } });
  }

  async remove(userId: string, id: string): Promise<void> {
    const result = await this.prisma.category.deleteMany({ where: { id, userId } });
    if (!result.count) throw new NotFoundException('Category not found');
  }
}
