import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { AuthenticatedUser, CurrentUser } from '../common/current-user.decorator';
import { JwtAuthGuard } from '../common/jwt-auth.guard';
import { SummaryQueryDto } from './summary.dto';
import { SummariesService } from './summaries.service';

@ApiTags('summaries')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('summaries')
export class SummariesController {
  constructor(private readonly summaries: SummariesService) {}

  @Get('spending')
  @ApiOperation({ summary: 'Summarize spending by category for one currency and date range' })
  spending(@CurrentUser() user: AuthenticatedUser, @Query() query: SummaryQueryDto) {
    return this.summaries.spending(user.userId, query);
  }
}
