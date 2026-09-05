# Panchaayat — Consumer Voice & Resolution Platform

A unified web app where consumers share reviews, complaints, and grievances. Brands respond publicly, propose resolutions, and **only the original consumer** confirms when an issue is truly resolved.

> **Single-app architecture:** FastAPI serves both the REST API and the built React frontend from one process — no separate backend/frontend servers.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Bootstrap 5, React Router, Vite |
| Backend | Python 3.9+, FastAPI, Uvicorn |
| Database | SQLite (zero-config, file-based) |
| Auth | JWT (Bearer tokens) |
| AI | Azure OpenAI GPT (with smart rule-based fallbacks) |
| Social | Reddit, HN (public APIs) + optional X, Meta, LinkedIn, SerpAPI |
| Theme | Light / dark mode, modern (teal/coral) or classic (blue/amber) brand themes |

---

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Build frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 3. Run the app

```bash
python main.py
```

Open **http://localhost:8000**

### Optional: Azure OpenAI

Copy `.env.example` to `.env` and set credentials:

```env
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-08-01-preview
SECRET_KEY=change-this-in-production
```

Without Azure, all AI features use intelligent rule-based fallbacks.

### Optional: Social media API keys

Copy `.env.example` to `.env` and add keys for live social chatter ingestion (see [Social Media API Setup](#social-media-api-setup) below). Without keys, the app still works using public Reddit/Hacker News APIs, platform search deep links, and optional illustrative demo posts.

---

## Screens & Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page — hero, stats, trending, recently resolved, how it works |
| `/feed` | Experience feed — recent, trending, resolved; category filters |
| `/share` | 4-step complaint wizard with AI assist |
| `/complaint/:id` | Full case page — timeline, discussion, resolution loop |
| `/brand/:slug` | Brand profile — reputation metrics, complaints |
| `/search` | Smart search with natural language & filters |
| `/login` | Login + one-click demo personas |
| `/register` | Consumer registration |
| `/dashboard` | Consumer dashboard — my complaints, awaiting action |
| `/brand-dashboard` | Brand inbox — KPIs, open complaints, trending issues |
| `/admin` | Admin panel — ad management with AI targeting |
| `/how-it-works` | Platform guide & trust principles |
| `/for-business` | Business pricing, SME scenario, feature matrix |
| `/api` | Developer API documentation & hot-query reference |

---

## Core Features

### Consumer Experience

- **Share without login** — guests can post immediately (lower priority weight)
- **4-step complaint wizard** — What happened → Details → AI quality check → Preview
- **AI complaint drafting** — paste messy text, AI structures title, category, brand, location
- **AI quality check** — detects PII, aggressive language, missing info before publish
- **Visual case timeline** — immutable history of every event on a complaint
- **Status progress bar** — Shared → Awaiting → Responded → Proposed → Resolved
- **Discussion threads** — comments with official brand reply highlighting; previews on feed cards
- **"Me Too"** — signal same experience without duplicating posts
- **Post-resolution feedback** — separate resolution rating after consumer confirms
- **Escalation guidance** — NCH, E-Jagriti links on complaint pages
- **Social chatter panel** — scan related posts from X, Reddit, LinkedIn, Facebook, Instagram near each experience
- **Light / dark theme** — toggle in navbar, persisted in browser
- **Modern vs classic brand theme** — teal/coral (default) or original blue/amber via "Switch to Classic"

### Social Chatter (Brand Mentions)

On every **complaint detail** and **brand profile** page, the sidebar includes a **Social Chatter** panel:

- Click **Scan social media** to fetch brand-related posts
- Filter by platform (All, X, Reddit, LinkedIn, Facebook, Instagram, Hacker News)
- Each result shows platform, author, sentiment, engagement, and an **Open** link
- **Live** results come from configured APIs; **Illustrative** demo posts appear only when live matches are sparse
- **Search on platform** grid opens in-platform searches when full API access isn't configured

**Data sources (no keys required):**
- Reddit public JSON API
- Hacker News (Algolia API)
- Deep links to X, LinkedIn, Facebook, Instagram search pages

**With API keys configured:**
- X API v2 recent tweet search
- Reddit OAuth (higher rate limits)
- Meta Graph API (Facebook page posts, Instagram tagged media)
- LinkedIn REST API
- SerpAPI fallback for X, LinkedIn, Facebook, Instagram via Google site search

Check which integrations are active: `GET /api/social-mentions/config` (returns booleans only — never exposes keys).

### Guest vs Registered Users

| | Guest (no login) | Registered | Verified |
|--|------------------|------------|----------|
| Can post | ✅ | ✅ | ✅ |
| Weight score | 0.4× | 1.0× | up to 1.5× |
| Brand priority | Lower | Standard | Higher |
| Track complaints | ❌ | ✅ | ✅ |
| Confirm resolution | ❌ | ✅ | ✅ |
| Notifications | ❌ | ✅ | ✅ |

### Brand Experience

- **Brand dashboard** — open cases, resolution rate, avg response time, trending categories
- **Complaint inbox** — filter and respond to grievances
- **Official brand replies** — visually distinguished in discussion
- **Propose resolution** — refund, replacement, repair, apology, etc.
- **AI resolution suggestions** — practical advice for brand reps
- **Brand profile pages** — rating, complaint count, resolution rate, response rate

### Resolution Workflow (Key Differentiator)

```
Consumer posts → Brand responds → Brand proposes resolution
    → Consumer accepts / partially accepts / rejects & reopens
    → Consumer leaves updated feedback
```

Brands **cannot** unilaterally mark a complaint as permanently resolved.

### Smart Search

Not limited to exact keyword matching:

- **Natural language queries** — e.g. "delayed AC installation in Pune"
- **Synonym expansion** — refund → money back, install → setup, delay → late
- **Multi-field scoring** — title, category, brand, city, product, AI summary, topics
- **Filters** — category, status, city
- **Match reasons** — shows why each result matched
- **Expanded terms** — displays related terms used in search

### AI Features

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Complaint draft | `POST /api/ai/draft` | Structure messy text into fields |
| Quality check | `POST /api/ai/quality-check` | PII, toxicity, missing info warnings |
| Resolution suggest | `GET /api/ai/suggest-resolution` | Advice for brand reps |
| Ad targeting | `POST /api/ai/suggest-ad-targeting` | Categories, keywords, cities, personas |
| Case summary | (on create) | Auto-generated neutral summary per complaint |

All AI features work without Azure using rule-based fallbacks.

### Advertising System

- **Placements** — sidebar, inline, footer
- **Contextual matching** — by category, keywords, city, location, persona, role
- **Admin CRUD** — create, edit, delete ads at `/admin`
- **AI auto-fill** — "AI Suggest Categories & Keywords" button pre-fills targeting fields
- **Trust rule** — ads never affect complaint visibility or resolution outcomes

Sample ads seeded: warranty, installation, refund tracker, legal aid, invoice organizer.

---

## Social Media API Setup

Add these to your `.env` file (see `.env.example`). Restart the app after changes. The Social Chatter panel shows green **API connected** badges for configured sources.

### Quick reference

| Variable | Platform | Required with |
|----------|----------|---------------|
| `TWITTER_BEARER_TOKEN` | X (Twitter) | Bearer token only |
| `REDDIT_CLIENT_ID` | Reddit | `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` |
| `REDDIT_CLIENT_SECRET` | Reddit | `REDDIT_CLIENT_ID`, `REDDIT_USER_AGENT` |
| `REDDIT_USER_AGENT` | Reddit | Format: `AppName/1.0 by your_reddit_username` |
| `META_ACCESS_TOKEN` | Facebook / Instagram | `META_PAGE_ID` and/or `META_INSTAGRAM_BUSINESS_ID` |
| `META_PAGE_ID` | Facebook | Page posts via Graph API |
| `META_INSTAGRAM_BUSINESS_ID` | Instagram | Tagged media via Graph API |
| `LINKEDIN_ACCESS_TOKEN` | LinkedIn | OAuth access token with post-search scopes |
| `SERPAPI_KEY` | Multi-platform | Easiest single key for X, LinkedIn, Facebook, Instagram |
| `SOCIAL_MENTIONS_INCLUDE_DEMO` | — | Set `false` to disable illustrative demo posts |

**Tip:** If you only want one key to start, use **SerpAPI** — it covers X, LinkedIn, Facebook, and Instagram without setting up each platform separately.

---

### X (Twitter) — `TWITTER_BEARER_TOKEN`

Uses the [X API v2 recent search](https://developer.x.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) endpoint.

1. Go to [developer.x.com](https://developer.x.com/) and sign in.
2. Create a **Project** and **App** (Free tier allows limited recent search).
3. Open your app → **Keys and tokens**.
4. Under **Bearer Token**, click **Generate** and copy the token.
5. Add to `.env`:
   ```env
   TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAA...
   ```

**Notes:**
- Free tier has monthly tweet-read caps; upgrade for production volume.
- Recent search only returns tweets from the last 7 days.
- Query syntax supports operators like `-is:retweet lang:en` (already applied by the app).

---

### Reddit — `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`

Uses [Reddit OAuth2 client credentials](https://github.com/reddit-archive/reddit/wiki/OAuth2#application-only-oauth) for authenticated search (better rate limits than the public JSON endpoint).

1. Log in to Reddit and open [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
2. Click **create another app…**
3. Choose **web app** or **installed app** (script type also works for personal use).
4. Set **redirect uri** to `http://localhost:8000` (required but unused for client-credentials flow).
5. After creation, note:
   - **client id** — the string under the app name (not the secret label)
   - **client secret** — shown as "secret"
6. Add to `.env`:
   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=Panchaayat/1.0 by your_reddit_username
   ```

**Notes:**
- Replace `your_reddit_username` with your actual Reddit username (Reddit requires a descriptive User-Agent).
- Client-credentials flow allows read-only search without user login.

---

### Meta (Facebook & Instagram) — `META_ACCESS_TOKEN`, `META_PAGE_ID`, `META_INSTAGRAM_BUSINESS_ID`

Uses the [Meta Graph API](https://developers.facebook.com/docs/graph-api).

#### Facebook page posts

1. Go to [developers.facebook.com](https://developers.facebook.com/) → **My Apps** → **Create App**.
2. Choose **Business** type and complete setup.
3. Add the **Facebook Login** product (if prompted).
4. Create a **Page Access Token**:
   - Tools → [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   - Select your app and the Facebook Page you manage
   - Add permissions: `pages_read_engagement`, `pages_show_list`, `pages_read_user_content`
   - Click **Generate Access Token** (use a long-lived token for production)
5. Get your **Page ID** from Page Settings → About, or via Graph API: `GET /me/accounts`
6. Add to `.env`:
   ```env
   META_ACCESS_TOKEN=your_page_access_token
   META_PAGE_ID=your_numeric_page_id
   ```

#### Instagram tagged media

Requires an **Instagram Business** or **Creator** account linked to a Facebook Page.

1. In Meta App Dashboard, add the **Instagram Graph API** product.
2. Link your Instagram account to your Facebook Page (Instagram app → Settings → Account → Linked accounts).
3. In Graph API Explorer, query `GET /me/accounts` then `GET /{page-id}?fields=instagram_business_account` to get the Instagram Business Account ID.
4. Add to `.env`:
   ```env
   META_ACCESS_TOKEN=your_page_access_token
   META_INSTAGRAM_BUSINESS_ID=your_ig_business_account_id
   ```

**Notes:**
- Meta restricts public post search; this integration fetches posts from **your** page and **tags on your** Instagram business account, filtered by complaint keywords.
- For broad public Instagram search, use SerpAPI instead.
- Tokens expire — use [long-lived tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived) and refresh as needed.

---

### LinkedIn — `LINKEDIN_ACCESS_TOKEN`

Uses the [LinkedIn REST API](https://learn.microsoft.com/en-us/linkedin/). Post search requires Marketing API / partner access in many cases.

1. Go to [linkedin.com/developers](https://www.linkedin.com/developers/) → **Create app**.
2. Associate with a LinkedIn Page (required).
3. Under **Products**, request access to **Share on LinkedIn** and/or **Marketing Developer Platform** (approval may take time).
4. Under **Auth** → **OAuth 2.0 settings**, add redirect URL `http://localhost:8000`.
5. Generate an access token via OAuth 2.0 flow with scopes such as `r_organization_social`, `w_member_social` (exact scopes depend on approved products).
6. For testing, use the **Token generator** in the Developer Portal (short-lived).
7. Add to `.env`:
   ```env
   LINKEDIN_ACCESS_TOKEN=your_access_token
   ```

**Notes:**
- LinkedIn heavily restricts third-party post search. If the API returns 403, use **SerpAPI** (`site:linkedin.com`) as a fallback.
- Production apps typically need LinkedIn partner review.

---

### SerpAPI (recommended fallback) — `SERPAPI_KEY`

[SerpAPI](https://serpapi.com/) runs Google searches scoped to social sites — useful when platform-specific APIs are unavailable or restricted.

1. Sign up at [serpapi.com](https://serpapi.com/) (free tier includes 100 searches/month).
2. Open [Dashboard](https://serpapi.com/manage-api-key) and copy your API key.
3. Add to `.env`:
   ```env
   SERPAPI_KEY=your_serpapi_key
   ```

**What it enables:**
- `site:twitter.com` / `site:x.com` — X posts
- `site:linkedin.com` — LinkedIn content
- `site:facebook.com` — Facebook posts
- `site:instagram.com` — Instagram content

SerpAPI is used automatically for platforms that don't have a dedicated key configured. If you set `TWITTER_BEARER_TOKEN`, direct X API takes priority over SerpAPI for Twitter.

---

### Disable demo posts

When you have real API keys in production:

```env
SOCIAL_MENTIONS_INCLUDE_DEMO=false
```

---

## Demo Personas

Login at `/login` — click any persona card or use credentials below.  
**Password for all:** `demo123`

| Persona | Username | Role | Notes |
|---------|----------|------|-------|
| Priya Sharma | `priya_sharma` | Consumer | Frustrated Home Buyer, Pune, verified |
| Rahul Mehta | `rahul_mehta` | Consumer | Budget-Conscious Shopper, Mumbai |
| Anjali Reddy | `anjali_reddy` | Consumer | First-Time Car Owner, Hyderabad |
| Meera Patel | `meera_patel` | Consumer | Local Shop Advocate, Ahmedabad |
| Vikram Singh | `vikram_singh` | Brand Rep | CoolBreeze Appliances support manager |
| Sneha Kulkarni | `sneha_kulkarni` | Brand Rep | QuickCart e-commerce support lead |
| Arjun Nair | `arjun_nair` | Moderator | Community moderator |
| Platform Admin | `admin` | Admin | Ads, configuration |

---

## Seeded Demo Data

- **6 brands** — CoolBreeze, QuickCart, MegaMart, AutoDrive, FreshFoods, TechFix
- **5 sample complaints** — installation delay, refund pending, service coupon, billing overcharge, expired groceries
- **Discussion comments** — on multiple complaints including official brand replies
- **6 pre-configured ads** — with category/city/persona targeting
- **3 locations** — Pune (Viman Nagar, Koregaon Park), Hyderabad (Hitech City)

---

## API Reference

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register consumer |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Current user |
| GET | `/api/auth/personas` | List demo personas |

### Complaints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/complaints` | List (feed, category, city filters) |
| GET | `/api/complaints/{id}` | Full detail with timeline, comments |
| POST | `/api/complaints` | Create (guest or authenticated) |
| POST | `/api/complaints/{id}/me-too` | Me-too vote |
| POST | `/api/complaints/{id}/comments` | Add comment |
| POST | `/api/complaints/{id}/resolutions` | Brand proposes resolution |
| POST | `/api/complaints/{id}/resolutions/{rid}/respond` | Consumer confirms/rejects |
| GET | `/api/complaints/{id}/social-mentions` | Brand-related social posts for a complaint |

### Brands
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/brands` | List all brands |
| GET | `/api/brands/slug/{slug}` | Brand by slug |
| GET | `/api/brands/{id}/complaints` | Brand's complaints |
| GET | `/api/brands/{id}/social-mentions` | Brand-related social posts |
| GET | `/api/brands/dashboard/stats` | Brand KPI dashboard |

### Social mentions
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/social-mentions/config` | Which API integrations are configured (no secrets) |
| GET | `/api/complaints/{id}/social-mentions` | Fetch mentions for a complaint (`?platforms=all,twitter,reddit,…`) |
| GET | `/api/brands/{id}/social-mentions` | Fetch mentions for a brand |

### Search & AI
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/search` | Smart search (`q`, `category`, `status`, `city`) |
| POST | `/api/ai/draft` | AI complaint structuring |
| POST | `/api/ai/quality-check` | Pre-publish quality check |
| POST | `/api/ai/suggest-ad-targeting` | AI ad category/keyword suggestions |
| GET | `/api/stats/home` | Homepage statistics |

### Admin & Ads
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/ads` | Contextual ads for consumers |
| GET | `/api/admin/ads` | List all ads (admin) |
| POST | `/api/admin/ads` | Create ad (admin) |
| PUT | `/api/admin/ads/{id}` | Update ad (admin) |
| DELETE | `/api/admin/ads/{id}` | Delete ad (admin) |

---

## Complaint Status Lifecycle

```
PUBLISHED → AWAITING_RESPONSE → BUSINESS_RESPONDED → RESOLUTION_PROPOSED
    → RESOLVED / PARTIALLY_RESOLVED / REOPENED / ESCALATED / CLOSED
```

---

## Project Structure

```
Panchaayat/
├── main.py                    # App entry — run this
├── requirements.txt
├── .env.example
├── panchaayat.db              # SQLite database (auto-created)
├── app/
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── serializers.py         # Model → API output converters
│   ├── auth.py                # JWT auth & role guards
│   ├── seed.py                # Demo data seeding
│   ├── migrate.py             # DB migrations & comment sync
│   ├── routers/
│   │   ├── auth.py
│   │   ├── complaints.py
│   │   ├── interactions.py    # Comments, resolutions
│   │   ├── brands.py
│   │   ├── search_ai.py
│   │   ├── social.py          # Social mentions config endpoint
│   │   └── admin.py           # Ads & notifications
│   └── services/
│       ├── ai_service.py      # Azure OpenAI + fallbacks
│       ├── search_service.py  # Smart search with synonyms
│       ├── ad_service.py      # Contextual ad matching
│       ├── social_mentions_service.py  # Social API connectors
│       ├── text_utils.py      # Entity/keyword extraction
│       └── weight_service.py  # Guest vs registered weight
├── frontend/
│   ├── src/
│   │   ├── pages/             # All screen components
│   │   ├── components/        # Navbar, ComplaintCard, SocialMentionsPanel, etc.
│   │   ├── context/           # AuthContext, ThemeContext, BrandContext
│   │   └── api.js             # API client
│   └── package.json
└── static/dist/               # Built frontend (served by FastAPI)
```

---

## Development

### Rebuild frontend after UI changes

```bash
cd frontend && npm run build && cd ..
```

### Reset database

Delete `panchaayat.db` and restart — seed data will be recreated automatically.

### Port

Default: `8000`. Override with `PORT=8080 python main.py`.

---

## Deploy on Vercel

This repo is configured for Vercel serverless (see `vercel.json`).

1. Import the GitHub repo at [vercel.com/new](https://vercel.com/new)
2. **Root Directory:** leave as `.` (repository root) — **not** `frontend`
3. **Framework Preset:** Vercel should detect FastAPI automatically
4. Add environment variables in Project Settings:
   - `SECRET_KEY` — required in production (random string)
   - `AZURE_OPENAI_*` — optional, for AI features
   - `TWITTER_BEARER_TOKEN`, `REDDIT_*`, `META_*`, `LINKEDIN_ACCESS_TOKEN`, `SERPAPI_KEY` — optional, for social chatter
   - **Do not** add `DATABASE_URL` unless you have a real Postgres URL — an empty value will break startup (the app auto-uses `/tmp` on Vercel)
5. Deploy

`vercel.json` runs `cd frontend && npm ci && npm run build` so the SPA is built into `static/dist` before the Python function starts.

**Vercel limitations:**
- SQLite uses `/tmp` — data resets when the function cold-starts (fine for demos; use Postgres/Turso for production)
- File uploads are ephemeral on `/tmp`
- Set `SECRET_KEY` in Vercel env vars (never commit secrets)

After deploy, check `https://your-app.vercel.app/api/health` — should return `{"status":"ok",...}`.

---

## Trust Principles

1. Brands cannot unilaterally close complaints as resolved
2. Complete resolution history is permanently visible
3. Businesses cannot pay to remove legitimate complaints
4. AI assists but never judges guilt
5. User allegations are presented as experiences, not platform assertions
6. Ads are contextual and useful — never bias complaint visibility

---

## Changelog

### v1.0 — Initial Release
- Single-app FastAPI + React architecture
- Complaint creation wizard with AI assist
- Full resolution workflow
- Brand & consumer dashboards
- 8 demo personas with seed data
- Guest posting with weight-based priority
- Visual timeline & status progress

### v1.1 — Ads & Auth Fixes
- Admin ad panel (create, edit, delete)
- Contextual ad matching by category, city, persona, role
- JWT auth fix (admin operations work correctly)
- Ad targeting fields: cities, locations, personas, roles

### v1.2 — Search, Discussion & AI Ads
- **Smart search** — natural language, synonym expansion, multi-field scoring, filters
- **Discussion previews** — actual comment text on feed/search cards, not just counts
- **AI ad targeting** — auto-suggest categories & keywords when creating ads
- Sample discussions synced across complaints on startup
- Match reasons shown in search results

### v1.3 — Intelligent Text & Keyword Engine
- **Smarter ad AI targeting** — filters stop words (and, the, best, priced); detects products (iPhone 17), brands (Apple), intent (budget, deals)
- **Shared text intelligence** (`text_utils.py`) — entity extraction, intent phrases, product patterns
- **Improved search** — entity-aware scoring, no stop-word pollution in expanded terms
- **AI output sanitization** — merges Azure AI results with rule-based extraction for reliability

### v1.4 — UX, Themes & Marketing Pages
- **Stat cards** — reusable home/dashboard metrics with improved visual design
- **Light / dark theme** — navbar toggle, persisted via `ThemeContext`
- **Modern brand theme** — teal/coral default with logo assets; **Switch to Classic** for original blue/amber
- **For Business** (`/for-business`) — pricing, SME scenario, feature matrix
- **API docs page** (`/api`) — developer documentation and hot-query reference
- **Vercel deployment fixes** — `/tmp` SQLite paths, blank `DATABASE_URL` fallback, startup error handling

### v1.5 — Social Chatter & API Connectors
- **Social Chatter panel** on complaint detail and brand pages — scan related posts from X, Reddit, LinkedIn, Facebook, Instagram, Hacker News
- **Platform filters**, sentiment badges, live vs illustrative labelling, platform search deep links
- **API key support** — `TWITTER_BEARER_TOKEN`, Reddit OAuth, Meta Graph API, LinkedIn, SerpAPI
- **`GET /api/social-mentions/config`** — shows which integrations are configured (keys never exposed)
- **Complaint cards** — "Social chatter" teaser on feed cards
