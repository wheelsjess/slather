// Shared helpers for the Sun Fighter functions: signed run tokens, storage, JSON responses.
import { createHmac, createHash, randomUUID, timingSafeEqual } from 'node:crypto';
import { getStore } from '@netlify/blobs';

export const store = () => getStore({ name: 'sun-fighter', consistency: 'strong' });

export const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...headers } });

export const MIN_RUN = Number(process.env.MIN_RUN_SECONDS || 20);   // nobody kills the Sun faster than this
export const MAX_AGE = 2 * 60 * 60 * 1000;                          // a run token is good for two hours

function secret() {
  const s = process.env.RUN_SECRET;
  if (!s || s.length < 16) throw new Error('RUN_SECRET is not set (Site settings > Environment variables)');
  return s;
}
const b64 = s => Buffer.from(s).toString('base64url');
const sign = data => createHmac('sha256', secret()).update(data).digest('base64url');

// "<payload>.<signature>": the server stamps when the fight started, so the client can't claim more time passed than really did
export function makeToken(payload) { const p = b64(JSON.stringify(payload)); return p + '.' + sign(p); }
export function readToken(token) {
  if (typeof token !== 'string' || !token.includes('.')) return null;
  const [p, sig] = token.split('.'), want = sign(p);
  if (!sig || sig.length !== want.length || !timingSafeEqual(Buffer.from(sig), Buffer.from(want))) return null;
  try { return JSON.parse(Buffer.from(p, 'base64url').toString()); } catch { return null; }
}

export const newId = () => randomUUID();
export const hashEmail = email => createHash('sha256').update(email.trim().toLowerCase()).digest('hex');
export const cleanInitials = i => (String(i || '').toUpperCase().replace(/[^A-Z]/g, '') + 'AAA').slice(0, 3);

// leaderboard rows live in the key itself, so listing the keys is enough to rank: t/<centiseconds, zero-padded>-<initials>-<run id>
export const runKey = (t, i, id) => `t/${String(Math.round(t * 100)).padStart(9, '0')}-${i}-${id}`;
export function parseRunKey(key) {
  const m = /^t\/(\d{9})-([A-Z]{3})-(.+)$/.exec(key);
  return m ? { t: Number(m[1]) / 100, i: m[2], id: m[3] } : null;
}
export async function allRuns(s) {
  const { blobs } = await s.list({ prefix: 't/' });
  return blobs.map(b => parseRunKey(b.key)).filter(Boolean).sort((a, b) => a.t - b.t);
}
