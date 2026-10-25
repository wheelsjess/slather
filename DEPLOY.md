# Deploying Sun Fighter on Netlify

The game is one static page (`index.html`). The shared leaderboard and the prize entries run on Netlify Functions (`netlify/functions/`) and are stored in Netlify Blobs, so there's no separate database to set up. Once the repo is connected, every push to the production branch goes live automatically in about a minute.

## One-time setup

1. **Create the site.** In Netlify, choose **Add new project → Import an existing project → GitHub**, and pick this repo. The build settings come from `netlify.toml`, so leave them as they are.
2. **Pick the branch that goes live.** Under **Project configuration → Build & deploy → Branches and deploy contexts**, set the production branch to the branch the game is developed on (currently `claude/evil-sun-boss-game-z8k6ga`), or merge that branch into `main`.
3. **Add environment variables** under **Project configuration → Environment variables**:

   | Variable | What it's for |
   |---|---|
   | `RUN_SECRET` | Signs the run tokens that stop fake times. Any long random string (at least 16 characters); keep it private. |
   | `ADMIN_KEY` | Password for downloading the prize entries. Another long random string. |
   | `MIN_RUN_SECONDS` | Optional. The fastest time the server accepts (default 20). Set it just under the best time a good player can really manage. |

   Redeploy after adding them (**Deploys → Trigger deploy**).
4. **Add the domain.** Under **Domain management → Add a domain**, enter `sunfighter.slather.com.au`. Netlify shows a CNAME record. Add it wherever slather.com.au's DNS is managed (often the registrar, or Shopify if the domain was bought through Shopify). It doesn't touch the Shopify store. Netlify then issues the HTTPS certificate on its own.
5. **Link the competition terms.** Set `CLAIM_TERMS` in `index.html` (near `startClaim()`) to the terms page URL, for example a Shopify page at `slather.com.au/pages/sun-fighter-terms`.
6. **Link to it from the store**, for example with a homepage banner or a menu item pointing at `https://sunfighter.slather.com.au`.

## How it works

| Endpoint | What it does |
|---|---|
| `POST /api/run/start` | Called when a fight begins. Returns a token signed with the server's clock. |
| `POST /api/run/finish` | Called on a win with the token, initials and time. Rejects tampered or reused tokens, times under `MIN_RUN_SECONDS`, and any time longer than has really passed since the token was issued. Saves the run and returns a claim token for that exact run. |
| `GET /api/leaderboard` | The 50 fastest verified times (initials and time only). |
| `POST /api/claim` | A prize entry. Needs the claim token, an email, the terms tick and the Australia answer. Keeps one entry per email (their best time) and records the marketing opt-in separately. |
| `GET /api/admin/entries.csv` | Every entry, fastest first. Needs `ADMIN_KEY`. |

All endpoints are rate-limited per IP. The leaderboard never exposes emails.

When the page isn't on slather.com.au, a `*.netlify.app` address or localhost (for example in the Claude preview), the game falls back to the old behaviour: times stay on the player's device and prize entries aren't sent anywhere.

## Downloading entries

```sh
curl -H "Authorization: Bearer YOUR_ADMIN_KEY" https://sunfighter.slather.com.au/api/admin/entries.csv -o entries.csv
```

The CSV has rank, time, initials, email, marketing opt-in, country (from the visitor's IP), IP and timestamps. Only add people who ticked the marketing box to the mailing list.

## Before picking winners

The server checks make cheating harder, but a determined player can still submit a believable fake time. Before sending prizes:

- review the top 50 for duplicate people (same IP or similar emails) and non-Australian countries;
- treat times far ahead of the pack with suspicion;
- reserve the right to verify winners in the terms.
