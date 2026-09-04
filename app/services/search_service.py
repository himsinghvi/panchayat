"""Smart search with synonym expansion, entity extraction, and multi-field scoring."""

import re
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models import Complaint, Brand, Comment
from app.services.text_utils import (
    extract_entities, search_tokens, STOP_WORDS, SEARCH_SYNONYMS,
)

# Backward compat alias
SYNONYMS = SEARCH_SYNONYMS


def expand_query(query: str) -> list[str]:
    """Expand query using entity extraction + synonyms (no stop words)."""
    terms = search_tokens(query)
    # Also add multi-word substrings from original query (3+ char words)
    for word in re.findall(r"[a-zA-Z]{3,}", query.lower()):
        if word not in STOP_WORDS:
            terms.append(word)
    return list(dict.fromkeys(terms))


def _field_score(text: str | None, terms: list[str], weight: float) -> float:
    if not text:
        return 0.0
    lower = text.lower()
    score = 0.0
    for term in terms:
        if len(term) < 2:
            continue
        if term in lower:
            # Longer / more specific terms score higher
            score += weight * (1.5 + min(len(term) / 10, 1.5))
    return score


def _score_complaint(c: Complaint, terms: list[str], original_q: str) -> tuple[float, list[str]]:
    reasons = []
    score = 0.0
    oq = original_q.lower().strip()

    fields = [
        (c.title, 18, "title"),
        (c.product_name, 16, "product"),
        (c.category, 14, "category"),
        (c.brand_name_free, 12, "brand"),
        (c.brand.name if c.brand else None, 12, "brand"),
        (c.city, 9, "city"),
        (c.area, 8, "area"),
        (c.case_number, 22, "case number"),
        (c.ai_summary, 8, "AI summary"),
        (c.description, 6, "description"),
        (c.desired_resolution, 4, "resolution"),
    ]

    for text, weight, label in fields:
        s = _field_score(text, terms, weight)
        if s > 0:
            score += s
            if label not in reasons:
                reasons.append(label)

    if c.ai_topics:
        for topic in c.ai_topics:
            tl = str(topic).lower()
            for term in terms:
                if term in tl:
                    score += 8
                    if "topic" not in reasons:
                        reasons.append("topic")
                    break

    # Entity-aware boost from query
    entities = extract_entities(original_q)
    blob = f"{c.title} {c.description} {c.product_name or ''} {(c.brand.name if c.brand else '')}".lower()
    for product in entities["products"]:
        if product.lower() in blob:
            score += 30
            reasons.append(f"product: {product}")
    for brand in entities["brands"]:
        if brand.lower() in blob:
            score += 20
            if "brand match" not in reasons:
                reasons.append(f"brand: {brand}")

    if oq in (c.title or "").lower():
        score += 28
        reasons.append("exact title match")
    if len(oq) > 5 and oq in (c.description or "").lower():
        score += 12

    return score, list(dict.fromkeys(reasons))[:5]


def _score_brand(b: Brand, terms: list[str], original_q: str) -> tuple[float, list[str]]:
    reasons = []
    score = 0.0
    oq = original_q.lower()
    for text, weight, label in [
        (b.name, 18, "brand name"),
        (b.category, 12, "category"),
        (b.description, 6, "description"),
        (b.headquarters, 9, "headquarters"),
    ]:
        s = _field_score(text, terms, weight)
        if s > 0:
            score += s
            reasons.append(label)
    if oq in b.name.lower() or b.name.lower() in oq:
        score += 35
        reasons.append("exact brand match")
    return score, list(dict.fromkeys(reasons))[:4]


def smart_search(
    db: Session,
    query: str,
    category: str | None = None,
    status: str | None = None,
    city: str | None = None,
    limit: int = 20,
) -> dict:
    terms = expand_query(query)
    original_q = query.strip()

    complaints_q = db.query(Complaint).options(
        joinedload(Complaint.author),
        joinedload(Complaint.brand),
        joinedload(Complaint.comments).joinedload(Comment.author),
    )
    if category:
        complaints_q = complaints_q.filter(Complaint.category.ilike(f"%{category}%"))
    if status:
        complaints_q = complaints_q.filter(Complaint.status == status)
    if city:
        complaints_q = complaints_q.filter(Complaint.city.ilike(f"%{city}%"))

    all_complaints = complaints_q.all()
    scored_complaints = []
    for c in all_complaints:
        score, reasons = _score_complaint(c, terms, original_q)
        if score > 0:
            scored_complaints.append((score, c, reasons))

    if not scored_complaints:
        # Fallback: meaningful tokens only (not full raw query with stop words)
        meaningful = [t for t in terms if len(t) > 2]
        clauses = []
        for t in meaningful[:6]:
            pat = f"%{t}%"
            clauses.extend([
                Complaint.title.ilike(pat),
                Complaint.description.ilike(pat),
                Complaint.product_name.ilike(pat),
                Complaint.brand_name_free.ilike(pat),
                Complaint.category.ilike(pat),
                Complaint.city.ilike(pat),
            ])
        if clauses:
            fallback = complaints_q.filter(or_(*clauses)).limit(limit).all()
            scored_complaints = [(1.0, c, ["related terms"]) for c in fallback]

    scored_complaints.sort(key=lambda x: -x[0])

    brands_q = db.query(Brand)
    all_brands = brands_q.all()
    scored_brands = []
    for b in all_brands:
        score, reasons = _score_brand(b, terms, original_q)
        if score > 0:
            scored_brands.append((score, b, reasons))

    if not scored_brands:
        meaningful = [t for t in terms if len(t) > 2]
        clauses = []
        for t in meaningful[:5]:
            pat = f"%{t}%"
            clauses.extend([
                Brand.name.ilike(pat),
                Brand.category.ilike(pat),
                Brand.description.ilike(pat),
            ])
        if clauses:
            fallback = brands_q.filter(or_(*clauses)).limit(10).all()
            scored_brands = [(1.0, b, ["related terms"]) for b in fallback]

    scored_brands.sort(key=lambda x: -x[0])

    return {
        "terms": [t for t in terms if t not in STOP_WORDS][:20],
        "complaints": scored_complaints[:limit],
        "brands": scored_brands[:10],
    }
