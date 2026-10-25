// GET /api/admin/entries.csv with "Authorization: Bearer <ADMIN_KEY>": every prize entry, fastest first, for picking winners.
import { store } from '../lib/common.mjs';

const csv = v => `"${String(v ?? '').replace(/"/g, '""')}"`;

export default async req => {
  const key = process.env.ADMIN_KEY, auth = req.headers.get('authorization') || '';
  if (!key || auth !== 'Bearer ' + key) return new Response('unauthorised', { status: 401 });
  const s = store(), { blobs } = await s.list({ prefix: 'entry/' });
  const rows = (await Promise.all(blobs.map(b => s.get(b.key, { type: 'json' })))).filter(Boolean).sort((a, b) => a.time - b.time);
  const cols = ['rank', 'time', 'initials', 'email', 'marketing', 'country', 'ip', 'runId', 'finishedAt', 'enteredAt'];
  const lines = [cols.join(','), ...rows.map((r, n) => [n + 1, r.time, r.initials, r.email, r.marketing, r.country, r.ip, r.runId,
    new Date(r.finishedAt).toISOString(), new Date(r.enteredAt).toISOString()].map(csv).join(','))];
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/csv', 'Cache-Control': 'no-store', 'Content-Disposition': 'attachment; filename="sun-fighter-entries.csv"' } });
};

export const config = { path: '/api/admin/entries.csv', method: 'GET' };
