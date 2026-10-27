// POST /api/claim { claim, email, name, address1, address2, suburb, state, postcode, terms, marketing, australia }:
// a prize entry for a verified run. One entry per email: best time kept, latest postal address and consent honoured.
import { json, store, readToken, hashEmail } from '../lib/common.mjs';

const STATES = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'];
const field = (v, max) => String(v ?? '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max);

export default async (req, context) => {
  let body; try { body = await req.json(); } catch { return json({ error: 'bad request' }, 400); }
  const c = readToken(body.claim), email = String(body.email || '').trim();
  if (!c || !c.run) return json({ error: 'invalid claim' }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) return json({ error: 'invalid email' }, 422);
  if (body.terms !== true || body.australia !== true) return json({ error: 'terms not accepted' }, 422);
  const post = { name: field(body.name, 100), address1: field(body.address1, 120), address2: field(body.address2, 120),
    suburb: field(body.suburb, 60), state: field(body.state, 3).toUpperCase(), postcode: field(body.postcode, 4) };
  if (post.name.length < 2 || post.address1.length < 4 || post.suburb.length < 2 || !STATES.includes(post.state) || !/^\d{4}$/.test(post.postcode))
    return json({ error: 'invalid address' }, 422);
  const s = store(), key = 'entry/' + hashEmail(email), old = await s.get(key, { type: 'json' });
  const entry = {
    email, ...post, initials: c.i, time: c.t, runId: c.run, finishedAt: c.at, enteredAt: Date.now(),
    australia: true, terms: true, marketing: body.marketing === true,
    country: context.geo?.country?.code || '', ip: context.ip || '',
  };
  if (old && old.time <= entry.time) { Object.assign(old, post, { marketing: entry.marketing, updatedAt: entry.enteredAt }); await s.setJSON(key, old); }   // keep their best time, honour the latest address and consent
  else await s.setJSON(key, entry);
  return json({ ok: true });
};

export const config = { path: '/api/claim', method: 'POST', rateLimit: { windowLimit: 5, windowSize: 60, aggregateBy: ['ip', 'domain'] } };
