import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsISO8601, IsOptional, IsString, IsUUID, Matches } from 'class-validator';

export class SummaryQueryDto {
  @ApiProperty({ format: 'date-time', description: 'Inclusive UTC start timestamp' })
  @IsISO8601({ strict: true })
  startDate!: string;

  @ApiProperty({ format: 'date-time', description: 'Inclusive UTC end timestamp' })
  @IsISO8601({ strict: true })
  endDate!: string;

  @ApiProperty({ example: 'USD', description: 'Required to avoid combining different currencies' })
  @IsString()
  @Matches(/^[A-Z]{3}$/)
  currency!: string;

  @ApiPropertyOptional({ format: 'uuid' })
  @IsOptional()
  @IsUUID()
  categoryId?: string;
}
