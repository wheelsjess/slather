// POST /api/claim { claim, email, terms, marketing, australia }: a prize entry for a verified run. One entry per email, best time kept.
import { json, store, readToken, hashEmail } from '../lib/common.mjs';

export default async (req, context) => {
  let body; try { body = await req.json(); } catch { return json({ error: 'bad request' }, 400); }
  const c = readToken(body.claim), email = String(body.email || '').trim();
  if (!c || !c.run) return json({ error: 'invalid claim' }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) return json({ error: 'invalid email' }, 422);
  if (body.terms !== true || body.australia !== true) return json({ error: 'terms not accepted' }, 422);
  const s = store(), key = 'entry/' + hashEmail(email), old = await s.get(key, { type: 'json' });
  const entry = {
    email, initials: c.i, time: c.t, runId: c.run, finishedAt: c.at, enteredAt: Date.now(),
    australia: true, terms: true, marketing: body.marketing === true,
    country: context.geo?.country?.code || '', ip: context.ip || '',
  };
  if (old && old.time <= entry.time) { old.marketing = entry.marketing; old.updatedAt = entry.enteredAt; await s.setJSON(key, old); }   // keep their best time, honour the latest consent
  else await s.setJSON(key, entry);
  return json({ ok: true });
};

export const config = { path: '/api/claim', method: 'POST', rateLimit: { windowLimit: 5, windowSize: 60, aggregateBy: ['ip', 'domain'] } };
