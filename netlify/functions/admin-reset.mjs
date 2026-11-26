// POST /api/admin/reset with "Authorization: Bearer <ADMIN_KEY>": wipes the test leaderboard and entries before launch.
// Refused once the Competition Period has started, so real entries can never be cleared by accident.
import { json, store, COMP } from '../lib/common.mjs';

export default async req => {
  const key = process.env.ADMIN_KEY, auth = req.headers.get('authorization') || '';
  if (!key || auth !== 'Bearer ' + key) return new Response('unauthorised', { status: 401 });
  if (Date.now() >= COMP.open) return json({ error: 'the competition has started: data can no longer be cleared from here' }, 403);
  const s = store(); let removed = 0;
  for (const prefix of ['t/', 'best/', 'used/', 'entry/']) {
    const { blobs } = await s.list({ prefix });
    for (const b of blobs) { await s.delete(b.key); removed++; }
  }
  return json({ ok: true, removed });
};

export const config = { path: '/api/admin/reset', method: 'POST' };
