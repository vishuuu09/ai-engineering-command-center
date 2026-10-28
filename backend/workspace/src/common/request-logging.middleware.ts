import { randomUUID } from 'crypto';
import { NextFunction, Request, Response } from 'express';

export function requestLoggingMiddleware(req: Request, res: Response, next: NextFunction): void {
  const requestId = req.header('x-request-id') || randomUUID();
  res.setHeader('x-request-id', requestId);
  const startedAt = Date.now();
  res.on('finish', () => {
    console.log(JSON.stringify({
      level: 'info',
      message: 'http_request',
      requestId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      durationMs: Date.now() - startedAt,
    }));
  });
  next();
}
