"""Context-aware ad matching by category, keywords, city, location, persona, and role."""


def _norm_list(items) -> list[str]:
    if not items:
        return []
    if isinstance(items, str):
        return [s.strip().lower() for s in items.split(",") if s.strip()]
    return [str(s).strip().lower() for s in items if str(s).strip()]


def _matches_any(target: str, values: list[str]) -> bool:
    if not values:
        return True  # no restriction = matches all
    if not target:
        return False
    t = target.lower()
    return any(v == t or v in t or t in v for v in values)


def _overlap(a: list[str], b: list[str]) -> bool:
    if not b:
        return True
    if not a:
        return False
    return bool(set(a) & set(b))


def match_ads(
    ads: list,
    category: str = "",
    keywords: list | str | None = None,
    topics: list | str | None = None,
    city: str = "",
    area: str = "",
    persona: str = "",
    role: str = "",
) -> list:
    """Score and rank ads by contextual relevance."""
    kw_list = _norm_list(keywords) + _norm_list(topics)
    cat = (category or "").strip().lower()
    city_l = (city or "").strip().lower()
    area_l = (area or "").strip().lower()
    persona_l = (persona or "").strip().lower()
    role_l = (role or "").strip().lower()
    location_ctx = " ".join(filter(None, [area_l, city_l]))

    scored = []
    for ad in ads:
        if not ad.active:
            continue

        ad_cats = _norm_list(ad.categories)
        ad_kws = _norm_list(ad.keywords)
        ad_cities = _norm_list(ad.cities)
        ad_locs = _norm_list(ad.locations)
        ad_personas = _norm_list(ad.personas)
        ad_roles = _norm_list(ad.roles)

        # Hard filters: if ad targets a dimension, context must match
        if ad_cities and not _matches_any(city_l, ad_cities):
            continue
        if ad_locs and area_l and not any(
            loc in location_ctx or location_ctx in loc for loc in ad_locs
        ):
            continue
        if ad_personas and persona_l and not _matches_any(persona_l, ad_personas):
            continue
        if ad_roles and role_l and not _matches_any(role_l, ad_roles):
            continue

        score = ad.priority or 0

        # Category match
        if cat and ad_cats:
            if cat in ad_cats or any(cat in c or c in cat for c in ad_cats):
                score += 20
        elif not ad_cats:
            score += 2  # generic ad, slight boost

        # Keyword/topic overlap
        if kw_list and ad_kws:
            overlap = sum(1 for k in kw_list if any(k in ak or ak in k for ak in ad_kws))
            score += overlap * 8

        # City/location soft boost
        if city_l and ad_cities and _matches_any(city_l, ad_cities):
            score += 12
        if location_ctx and ad_locs:
            if any(loc in location_ctx or location_ctx in loc for loc in ad_locs):
                score += 10

        # Persona/role boost
        if persona_l and ad_personas and _matches_any(persona_l, ad_personas):
            score += 15
        if role_l and ad_roles and _matches_any(role_l, ad_roles):
            score += 10

        # Text relevance in title/description
        blob = f"{ad.title} {ad.description or ''}".lower()
        for k in kw_list + ([cat] if cat else []):
            if k and k in blob:
                score += 4

        scored.append((score, ad))

    scored.sort(key=lambda x: (-x[0], -(x[1].priority or 0)))
    return [ad for _, ad in scored[:3]]
