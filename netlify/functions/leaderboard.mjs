// GET /api/leaderboard: the fastest verified times (initials and time only, never emails).
import { json, store, allRuns } from '../lib/common.mjs';

export default async () => {
  const runs = await allRuns(store());
  return json({ runs: runs.slice(0, 50).map(({ i, t }) => ({ i, t })), total: runs.length }, 200,
    { 'Cache-Control': 'public, max-age=0', 'Netlify-CDN-Cache-Control': 'public, s-maxage=15, stale-while-revalidate=30' });
};

export const config = { path: '/api/leaderboard', method: 'GET' };
