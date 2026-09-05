"""Fetch and synthesize brand-related social chatter for complaints."""

from __future__ import annotations

import hashlib
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import quote_plus

import httpx

from app.config import get_settings
from app.services.text_utils import extract_meaningful_tokens, STOP_WORDS

PLATFORM_META = {
    "twitter": {"label": "X (Twitter)", "icon": "twitter"},
    "reddit": {"label": "Reddit", "icon": "reddit"},
    "linkedin": {"label": "LinkedIn", "icon": "linkedin"},
    "facebook": {"label": "Facebook", "icon": "facebook"},
    "instagram": {"label": "Instagram", "icon": "instagram"},
    "hackernews": {"label": "Hacker News", "icon": "news"},
}

API_SOURCE_DEFS = [
    {
        "platform": "twitter",
        "label": "X (Twitter)",
        "method": "X API v2 recent search",
        "docs_url": "https://developer.twitter.com/en/docs/twitter-api",
        "check": lambda s: bool(s.twitter_bearer_token),
    },
    {
        "platform": "reddit",
        "label": "Reddit",
        "method": "Reddit OAuth API",
        "docs_url": "https://www.reddit.com/dev/api",
        "check": lambda s: bool(s.reddit_client_id and s.reddit_client_secret),
    },
    {
        "platform": "facebook",
        "label": "Facebook",
        "method": "Meta Graph API (Page posts)",
        "docs_url": "https://developers.facebook.com/docs/graph-api",
        "check": lambda s: bool(s.meta_access_token and s.meta_page_id),
    },
    {
        "platform": "instagram",
        "label": "Instagram",
        "method": "Meta Graph API (tagged media)",
        "docs_url": "https://developers.facebook.com/docs/instagram-api",
        "check": lambda s: bool(s.meta_access_token and s.meta_instagram_business_id),
    },
    {
        "platform": "linkedin",
        "label": "LinkedIn",
        "method": "LinkedIn REST API",
        "docs_url": "https://learn.microsoft.com/en-us/linkedin/",
        "check": lambda s: bool(s.linkedin_access_token),
    },
    {
        "platform": "serpapi",
        "label": "SerpAPI (multi-platform)",
        "method": "Google site search via SerpAPI",
        "docs_url": "https://serpapi.com/",
        "check": lambda s: bool(s.serpapi_key),
    },
]

DEMO_TEMPLATES = [
    ("twitter", "@consumer_{n}", "Still waiting for {brand} to respond about my {issue}. #{tag} #CustomerService"),
    ("twitter", "@pune_consumer", "Anyone else having {issue} issues with {brand}? Day {days} and no resolution."),
    ("reddit", "u/frustrated_buyer", "Posted on r/IndiaConsumer about {brand} — {issue}. Support is ignoring emails."),
    ("linkedin", "Priya Sharma", "Sharing my experience with {brand}'s after-sales support. {issue} — hoping for accountability."),
    ("facebook", "Consumer Rights Pune", "Multiple members reporting {issue} problems with {brand} this week."),
    ("instagram", "@review_watch", "Story highlight: {brand} {issue} — DM us if you faced the same."),
]

BRAND_HANDLES = {
    "coolbreeze": "@CoolBreezeIN",
    "quickcart": "@QuickCartIndia",
    "megamart": "@MegaMartIN",
    "autodrive": "@AutoDriveMotors",
    "freshfoods": "@FreshFoodsIN",
    "techfix": "@TechFixService",
}

SERP_SITE_MAP = {
    "twitter": ["twitter.com", "x.com"],
    "linkedin": ["linkedin.com"],
    "facebook": ["facebook.com"],
    "instagram": ["instagram.com"],
}

_reddit_token_cache: dict = {"token": None, "expires_at": 0.0}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _stable_id(*parts: str) -> str:
    return hashlib.md5("|".join(parts).encode()).hexdigest()[:12]


def get_social_api_status() -> list[dict]:
    settings = get_settings()
    return [
        {
            "platform": src["platform"],
            "label": src["label"],
            "configured": src["check"](settings),
            "method": src["method"],
            "docs_url": src.get("docs_url"),
        }
        for src in API_SOURCE_DEFS
    ]


def build_search_query(brand_name: str, title: str, description: str, category: str = "") -> str:
    keywords = extract_meaningful_tokens(f"{title} {description} {category}")[:5]
    brand_part = brand_name.strip() if brand_name else ""
    kw_part = " ".join(keywords[:3]) if keywords else category or "complaint"
    if brand_part:
        return f"{brand_part} {kw_part}".strip()
    return kw_part


def _guess_sentiment(text: str) -> str:
    lower = text.lower()
    neg = ("bad", "worst", "delay", "refund", "scam", "fraud", "angry", "terrible", "poor", "ignore", "waiting")
    pos = ("resolved", "thank", "great", "happy", "excellent", "fixed", "refunded")
    if any(w in lower for w in neg):
        return "negative"
    if any(w in lower for w in pos):
        return "positive"
    return "neutral"


def _query_matches(text: str, query: str) -> bool:
    if not text or not query:
        return True
    tokens = [t.lower() for t in re.findall(r"[a-zA-Z]{3,}", query)]
    lower = text.lower()
    return any(t in lower for t in tokens[:4]) if tokens else True


def _mention(
    platform: str,
    author: str,
    text: str,
    *,
    handle: str | None = None,
    url: str | None = None,
    posted_at: str | None = None,
    relevance: float = 0.6,
    engagement: str | None = None,
    id_seed: str = "",
) -> dict:
    return {
        "id": _stable_id(platform, id_seed or text[:40]),
        "platform": platform,
        "platform_label": PLATFORM_META.get(platform, {}).get("label", platform),
        "author": author,
        "handle": handle,
        "text": text[:500],
        "url": url,
        "posted_at": posted_at,
        "relevance_score": relevance,
        "sentiment": _guess_sentiment(text),
        "source": "live",
        "engagement": engagement,
    }


def _platform_search_links(brand_name: str, query: str) -> list[dict]:
    q = quote_plus(query)
    brand_q = quote_plus(brand_name or query)
    tag = re.sub(r"[^a-zA-Z0-9]", "", brand_name or "complaint")
    return [
        {
            "platform": "twitter",
            "label": PLATFORM_META["twitter"]["label"],
            "url": f"https://twitter.com/search?q={q}&f=live",
            "hint": "Search recent posts on X",
        },
        {
            "platform": "reddit",
            "label": PLATFORM_META["reddit"]["label"],
            "url": f"https://www.reddit.com/search/?q={q}&sort=new",
            "hint": "Search Reddit discussions",
        },
        {
            "platform": "linkedin",
            "label": PLATFORM_META["linkedin"]["label"],
            "url": f"https://www.linkedin.com/search/results/content/?keywords={brand_q}",
            "hint": "Search LinkedIn posts",
        },
        {
            "platform": "facebook",
            "label": PLATFORM_META["facebook"]["label"],
            "url": f"https://www.facebook.com/search/posts?q={brand_q}",
            "hint": "Search Facebook posts",
        },
        {
            "platform": "instagram",
            "label": PLATFORM_META["instagram"]["label"],
            "url": f"https://www.instagram.com/explore/tags/{tag}/",
            "hint": "Browse related Instagram tags",
        },
    ]


def _reddit_access_token(client_id: str, client_secret: str, user_agent: str) -> str | None:
    now = time.time()
    if _reddit_token_cache["token"] and _reddit_token_cache["expires_at"] > now:
        return _reddit_token_cache["token"]
    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=(client_id, client_secret),
                data={"grant_type": "client_credentials"},
                headers={"User-Agent": user_agent},
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            token = data.get("access_token")
            if token:
                _reddit_token_cache["token"] = token
                _reddit_token_cache["expires_at"] = now + max(60, data.get("expires_in", 3600) - 60)
            return token
    except Exception:
        return None


def _fetch_reddit(query: str, limit: int = 8) -> list[dict]:
    settings = get_settings()
    headers = {"User-Agent": settings.reddit_user_agent or "PanchaayatSocialBot/1.0"}
    base_url = "https://www.reddit.com"
    token = None
    if settings.reddit_client_id and settings.reddit_client_secret:
        token = _reddit_access_token(
            settings.reddit_client_id,
            settings.reddit_client_secret,
            settings.reddit_user_agent,
        )
        if token:
            headers["Authorization"] = f"Bearer {token}"
            base_url = "https://oauth.reddit.com"

    results = []
    try:
        with httpx.Client(timeout=8.0, headers=headers) as client:
            resp = client.get(
                f"{base_url}/search",
                params={"q": query, "sort": "new", "limit": limit, "type": "link"},
            )
            if resp.status_code != 200:
                return results
            data = resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                title = post.get("title", "")
                selftext = post.get("selftext", "") or ""
                text = f"{title}. {selftext}".strip()[:500]
                if not text:
                    continue
                created = datetime.fromtimestamp(post.get("created_utc", 0), tz=timezone.utc)
                results.append(_mention(
                    "reddit",
                    post.get("author", "reddit_user"),
                    text,
                    handle=f"u/{post.get('author', 'user')}",
                    url=f"https://reddit.com{post.get('permalink', '')}",
                    posted_at=created.isoformat(),
                    relevance=min(1.0, 0.55 + post.get("num_comments", 0) * 0.02),
                    engagement=f"{post.get('score', 0)} upvotes · {post.get('num_comments', 0)} comments",
                    id_seed=post.get("id", ""),
                ))
    except Exception:
        pass
    return results


def _fetch_twitter(query: str, bearer_token: str, limit: int = 10) -> list[dict]:
    results = []
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                "https://api.twitter.com/2/tweets/search/recent",
                headers={"Authorization": f"Bearer {bearer_token}"},
                params={
                    "query": f"{query} -is:retweet lang:en",
                    "max_results": min(max(limit, 10), 100),
                    "tweet.fields": "created_at,public_metrics,author_id",
                    "expansions": "author_id",
                    "user.fields": "username,name",
                },
            )
            if resp.status_code != 200:
                return results
            payload = resp.json()
            users = {u["id"]: u for u in payload.get("includes", {}).get("users", [])}
            for tweet in payload.get("data", []):
                author = users.get(tweet.get("author_id", ""), {})
                username = author.get("username", "user")
                metrics = tweet.get("public_metrics", {})
                results.append(_mention(
                    "twitter",
                    author.get("name", username),
                    tweet.get("text", ""),
                    handle=f"@{username}",
                    url=f"https://twitter.com/{username}/status/{tweet.get('id')}",
                    posted_at=tweet.get("created_at"),
                    relevance=0.75,
                    engagement=(
                        f"{metrics.get('like_count', 0)} likes · "
                        f"{metrics.get('reply_count', 0)} replies"
                    ),
                    id_seed=tweet.get("id", ""),
                ))
    except Exception:
        pass
    return results


def _fetch_serpapi_site(query: str, api_key: str, platform: str, sites: list[str], limit: int = 5) -> list[dict]:
    site_clause = " OR ".join(f"site:{s}" for s in sites)
    results = []
    try:
        with httpx.Client(timeout=12.0) as client:
            resp = client.get(
                "https://serpapi.com/search.json",
                params={
                    "engine": "google",
                    "q": f"({site_clause}) {query}",
                    "api_key": api_key,
                    "num": limit,
                },
            )
            if resp.status_code != 200:
                return results
            for item in resp.json().get("organic_results", [])[:limit]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                text = f"{title}. {snippet}".strip()
                if not text:
                    continue
                results.append(_mention(
                    platform,
                    item.get("source", platform.title()),
                    text,
                    url=item.get("link"),
                    relevance=0.65,
                    id_seed=item.get("link", text[:30]),
                ))
    except Exception:
        pass
    return results


def _fetch_meta_facebook_posts(query: str, access_token: str, page_id: str, limit: int = 8) -> list[dict]:
    results = []
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                f"https://graph.facebook.com/v21.0/{page_id}/posts",
                params={
                    "access_token": access_token,
                    "fields": "message,created_time,permalink_url,likes.summary(true),comments.summary(true)",
                    "limit": limit,
                },
            )
            if resp.status_code != 200:
                return results
            for post in resp.json().get("data", []):
                message = post.get("message", "")
                if not message or not _query_matches(message, query):
                    continue
                likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
                comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
                results.append(_mention(
                    "facebook",
                    "Facebook Page",
                    message,
                    url=post.get("permalink_url"),
                    posted_at=post.get("created_time"),
                    relevance=0.7,
                    engagement=f"{likes} likes · {comments} comments",
                    id_seed=post.get("id", ""),
                ))
    except Exception:
        pass
    return results


def _fetch_meta_instagram_tags(query: str, access_token: str, ig_business_id: str, limit: int = 8) -> list[dict]:
    results = []
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                f"https://graph.facebook.com/v21.0/{ig_business_id}/tags",
                params={
                    "access_token": access_token,
                    "fields": "caption,permalink,timestamp,like_count,comments_count,username",
                    "limit": limit,
                },
            )
            if resp.status_code != 200:
                return results
            for media in resp.json().get("data", []):
                caption = media.get("caption", "") or ""
                if caption and not _query_matches(caption, query):
                    continue
                username = media.get("username", "instagram_user")
                text = caption or f"Tagged media from @{username}"
                results.append(_mention(
                    "instagram",
                    username,
                    text,
                    handle=f"@{username}",
                    url=media.get("permalink"),
                    posted_at=media.get("timestamp"),
                    relevance=0.68,
                    engagement=(
                        f"{media.get('like_count', 0)} likes · "
                        f"{media.get('comments_count', 0)} comments"
                    ),
                    id_seed=media.get("id", ""),
                ))
    except Exception:
        pass
    return results


def _fetch_linkedin(query: str, access_token: str, limit: int = 8) -> list[dict]:
    results = []
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                "https://api.linkedin.com/rest/posts",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "LinkedIn-Version": "202405",
                    "X-Restli-Protocol-Version": "2.0.0",
                },
                params={"q": "search", "keywords": query, "count": limit},
            )
            if resp.status_code != 200:
                return results
            elements = resp.json().get("elements", [])
            for item in elements[:limit]:
                commentary = item.get("commentary", "")
                if isinstance(commentary, dict):
                    text = commentary.get("text", "") or str(commentary)
                else:
                    text = str(commentary or item.get("text", ""))
                if not text:
                    continue
                author = item.get("author", "LinkedIn member")
                if isinstance(author, dict):
                    author = author.get("name", "LinkedIn member")
                results.append(_mention(
                    "linkedin",
                    str(author),
                    text,
                    url=item.get("permalink") or item.get("url"),
                    posted_at=item.get("createdAt") or item.get("created_at"),
                    relevance=0.72,
                    id_seed=str(item.get("id", text[:20])),
                ))
    except Exception:
        pass
    return results


def _fetch_hackernews(query: str, limit: int = 5) -> list[dict]:
    results = []
    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get(
                "https://hn.algolia.com/api/v1/search",
                params={"query": query, "tags": "story", "hitsPerPage": limit},
            )
            if resp.status_code != 200:
                return results
            for hit in resp.json().get("hits", []):
                text = hit.get("title", "")
                if hit.get("story_text"):
                    text = f"{text} — {hit['story_text'][:300]}"
                ts = hit.get("created_at_i")
                posted = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else None
                results.append(_mention(
                    "hackernews",
                    hit.get("author", "hn_user"),
                    text[:500],
                    handle=hit.get("author"),
                    url=hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    posted_at=posted,
                    relevance=0.5,
                    engagement=f"{hit.get('points', 0)} points",
                    id_seed=hit.get("objectID", ""),
                ))
    except Exception:
        pass
    return results


def _demo_mentions(
    brand_name: str,
    title: str,
    category: str,
    brand_slug: str = "",
    count: int = 4,
) -> list[dict]:
    issue = category.lower() if category else "service"
    if title:
        words = [w for w in re.findall(r"[A-Za-z]{4,}", title) if w.lower() not in STOP_WORDS]
        if words:
            issue = words[0].lower()

    tag = re.sub(r"[^a-zA-Z0-9]", "", brand_name or "Brand")
    handle = BRAND_HANDLES.get(brand_slug, f"@{tag}")
    seed = int(hashlib.md5(f"{brand_name}{title}".encode()).hexdigest()[:8], 16)
    mentions = []
    for i, (platform, author_tpl, tmpl) in enumerate(DEMO_TEMPLATES[:count]):
        days = (seed % 14) + 1
        author = author_tpl.format(n=seed % 1000)
        text = tmpl.format(brand=brand_name or "the brand", issue=issue, tag=tag, days=days)
        posted = _utcnow() - timedelta(days=days % 7, hours=(seed + i) % 48)
        mentions.append({
            "id": _stable_id("demo", brand_name, str(i), title),
            "platform": platform,
            "platform_label": PLATFORM_META.get(platform, {}).get("label", platform),
            "author": author.replace("@", "").replace("u/", ""),
            "handle": author if author.startswith(("@", "u/")) else handle,
            "text": text,
            "url": _platform_search_links(brand_name, brand_name)[
                ["twitter", "reddit", "linkedin", "facebook", "instagram"].index(platform)
            ]["url"],
            "posted_at": posted.isoformat(),
            "relevance_score": 0.72 - i * 0.05,
            "sentiment": "negative" if i < 3 else "neutral",
            "source": "demo",
            "engagement": f"{(seed + i * 3) % 40} reactions",
        })
    return mentions


def _build_notes(settings, configured: list[str]) -> list[str]:
    notes = [
        "Hacker News and Reddit are always queried (Reddit uses OAuth when REDDIT_CLIENT_ID/SECRET are set).",
    ]
    if configured:
        notes.append(f"API-connected sources active: {', '.join(configured)}.")
    else:
        notes.append(
            "Add API keys in .env (TWITTER_BEARER_TOKEN, REDDIT_CLIENT_ID, META_ACCESS_TOKEN, "
            "LINKEDIN_ACCESS_TOKEN, or SERPAPI_KEY) for richer live results."
        )
    if settings.social_mentions_include_demo:
        notes.append("Illustrative demo posts may appear when live matches are sparse — labelled below.")
    return notes


def fetch_social_mentions(
    brand_name: str,
    title: str = "",
    description: str = "",
    category: str = "",
    brand_slug: str = "",
    platforms: Optional[list[str]] = None,
    include_demo: Optional[bool] = None,
) -> dict:
    settings = get_settings()
    if include_demo is None:
        include_demo = settings.social_mentions_include_demo

    query = build_search_query(brand_name, title, description, category)
    requested = platforms or ["all"]
    search_all = "all" in requested
    api_status = get_social_api_status()
    configured_platforms = [s["platform"] for s in api_status if s["configured"]]

    live: list[dict] = []

    def wants(platform: str) -> bool:
        return search_all or platform in requested

    if wants("reddit"):
        live.extend(_fetch_reddit(query))
    if wants("hackernews"):
        live.extend(_fetch_hackernews(query))

    if wants("twitter") and settings.twitter_bearer_token:
        live.extend(_fetch_twitter(query, settings.twitter_bearer_token))

    if wants("facebook") and settings.meta_access_token and settings.meta_page_id:
        live.extend(_fetch_meta_facebook_posts(query, settings.meta_access_token, settings.meta_page_id))

    if wants("instagram") and settings.meta_access_token and settings.meta_instagram_business_id:
        live.extend(_fetch_meta_instagram_tags(query, settings.meta_access_token, settings.meta_instagram_business_id))

    if wants("linkedin") and settings.linkedin_access_token:
        live.extend(_fetch_linkedin(query, settings.linkedin_access_token))

    if settings.serpapi_key:
        serp_platforms = []
        if wants("twitter") and "twitter" not in configured_platforms:
            serp_platforms.append("twitter")
        if wants("linkedin") and "linkedin" not in configured_platforms:
            serp_platforms.append("linkedin")
        if wants("facebook") and "facebook" not in configured_platforms:
            serp_platforms.append("facebook")
        if wants("instagram") and "instagram" not in configured_platforms:
            serp_platforms.append("instagram")
        for plat in serp_platforms:
            live.extend(_fetch_serpapi_site(query, settings.serpapi_key, plat, SERP_SITE_MAP[plat]))

    seen = set()
    unique_live = []
    for m in sorted(live, key=lambda x: -x["relevance_score"]):
        key = m["text"][:80].lower()
        if key not in seen:
            seen.add(key)
            unique_live.append(m)

    mentions = unique_live[:15]

    if include_demo and len(mentions) < 4:
        demo = _demo_mentions(brand_name, title, category, brand_slug, count=5 - len(mentions))
        existing_ids = {m["id"] for m in mentions}
        for d in demo:
            if d["id"] not in existing_ids:
                mentions.append(d)

    if platforms and not search_all:
        mentions = [m for m in mentions if m["platform"] in requested]

    mentions.sort(key=lambda x: (-x["relevance_score"], x.get("posted_at") or ""))

    searched = list(PLATFORM_META.keys()) if search_all else [p for p in requested if p != "all"]

    return {
        "brand_name": brand_name or "Unknown",
        "query_used": query,
        "fetched_at": _utcnow().isoformat(),
        "platforms_searched": searched or list(PLATFORM_META.keys()),
        "mentions": mentions,
        "search_links": _platform_search_links(brand_name, query),
        "live_count": len(unique_live),
        "notes": _build_notes(settings, configured_platforms),
        "api_sources": api_status,
    }
