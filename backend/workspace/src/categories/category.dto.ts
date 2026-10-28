import { ApiProperty } from '@nestjs/swagger';
import { IsString, MaxLength, MinLength } from 'class-validator';

export class CreateCategoryDto {
  @ApiProperty({ example: 'Groceries' })
  @IsString()
  @MinLength(1)
  @MaxLength(80)
  name!: string;
}

export class UpdateCategoryDto {
  @ApiProperty({ example: 'Groceries' })
  @IsString()
  @MinLength(1)
  @MaxLength(80)
  name!: string;
}
