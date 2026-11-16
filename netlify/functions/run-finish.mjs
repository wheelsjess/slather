// POST /api/run/finish { token, initials, time, player }: records a win after sanity checks. The leaderboard keeps one line per
// player (the device's player id): only their fastest time, as the terms (clause 4.3) require.
import { json, store, readToken, makeToken, cleanInitials, runKey, allRuns, MIN_RUN, MAX_AGE } from '../lib/common.mjs';

export default async req => {
  let body; try { body = await req.json(); } catch { return json({ error: 'bad request' }, 400); }
  const tok = readToken(body.token), t = Number(body.time), now = Date.now();
  if (!tok) return json({ error: 'invalid run token' }, 400);
  if (now - tok.start > MAX_AGE) return json({ error: 'run token expired' }, 400);
  const elapsed = (now - tok.start) / 1000;
  // the in-game clock only runs while fighting, so it can never be more than the real time since the token was issued
  if (!Number.isFinite(t) || t < MIN_RUN || t > elapsed + 2) return json({ error: 'time rejected' }, 422);
  const s = store();
  if (await s.get('used/' + tok.id)) return json({ error: 'run already recorded' }, 409);
  await s.set('used/' + tok.id, '1');
  const i = cleanInitials(body.initials), pid = /^[a-z0-9-]{8,40}$/.test(body.player || '') ? body.player : tok.id;
  const prev = await s.get('best/' + pid, { type: 'json' });
  if (!prev || t < prev.t) {                                   // a new personal best replaces their old line
    if (prev) await s.delete(prev.key);
    const key = runKey(t, i, pid); await s.setJSON(key, { i, t, at: now }); await s.setJSON('best/' + pid, { key, t });
  }
  const runs = await allRuns(s), best = Math.min(t, prev ? prev.t : Infinity), rank = runs.findIndex(r => r.id === pid && r.t === best) + 1;
  // the claim token proves this exact verified run, so the prize form can't be fed a made-up time
  return json({ runId: tok.id, rank, claim: makeToken({ run: tok.id, t, i, at: now }) });
};

export const config = { path: '/api/run/finish', method: 'POST', rateLimit: { windowLimit: 10, windowSize: 60, aggregateBy: ['ip', 'domain'] } };
