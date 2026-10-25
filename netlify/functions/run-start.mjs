// POST /api/run/start: called when a fight begins; hands back a signed token stamped with the server's clock.
import { json, makeToken, newId } from '../lib/common.mjs';

export default async () => json({ token: makeToken({ id: newId(), start: Date.now() }) });

export const config = { path: '/api/run/start', method: 'POST', rateLimit: { windowLimit: 30, windowSize: 60, aggregateBy: ['ip', 'domain'] } };
