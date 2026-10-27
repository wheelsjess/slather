// GET /api/admin/entries.csv (or .json, for the /admin page) with "Authorization: Bearer <ADMIN_KEY>": every prize entry, fastest first.
import { store } from '../lib/common.mjs';

// quote every cell; a leading = + - @ gets an apostrophe so a spreadsheet never runs a player's text as a formula
const csv = v => { let t = String(v ?? ''); if (/^[=+\-@\t\r]/.test(t)) t = "'" + t; return `"${t.replace(/"/g, '""')}"`; };

export default async req => {
  const key = process.env.ADMIN_KEY, auth = req.headers.get('authorization') || '';
  if (!key || auth !== 'Bearer ' + key) return new Response('unauthorised', { status: 401 });
  const s = store(), { blobs } = await s.list({ prefix: 'entry/' });
  const rows = (await Promise.all(blobs.map(b => s.get(b.key, { type: 'json' })))).filter(Boolean).sort((a, b) => a.time - b.time);
  if (new URL(req.url).pathname.endsWith('.json')) return new Response(JSON.stringify({ entries: rows }), { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
  const cols = ['rank', 'time', 'initials', 'email', 'name', 'address1', 'address2', 'suburb', 'state', 'postcode', 'marketing', 'country', 'ip', 'runId', 'finishedAt', 'enteredAt'];
  const lines = [cols.join(','), ...rows.map((r, n) => [n + 1, r.time, r.initials, r.email, r.name, r.address1, r.address2, r.suburb, r.state, r.postcode, r.marketing, r.country, r.ip, r.runId,
    new Date(r.finishedAt).toISOString(), new Date(r.enteredAt).toISOString()].map(csv).join(','))];
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/csv', 'Cache-Control': 'no-store', 'Content-Disposition': 'attachment; filename="sun-fighter-entries.csv"' } });
};

export const config = { path: ['/api/admin/entries.csv', '/api/admin/entries.json'], method: 'GET', rateLimit: { windowLimit: 20, windowSize: 60, aggregateBy: ['ip', 'domain'] } };
