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
| Theme | Light theme, Inter font, CSS animations |

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

### Brands
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/brands` | List all brands |
| GET | `/api/brands/slug/{slug}` | Brand by slug |
| GET | `/api/brands/{id}/complaints` | Brand's complaints |
| GET | `/api/brands/dashboard/stats` | Brand KPI dashboard |

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
│   │   └── admin.py           # Ads & notifications
│   └── services/
│       ├── ai_service.py      # Azure OpenAI + fallbacks
│       ├── search_service.py  # Smart search with synonyms
│       ├── ad_service.py        # Contextual ad matching
│       └── weight_service.py  # Guest vs registered weight
├── frontend/
│   ├── src/
│   │   ├── pages/             # All screen components
│   │   ├── components/        # Navbar, ComplaintCard, AdBanner, etc.
│   │   ├── context/           # AuthContext
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
