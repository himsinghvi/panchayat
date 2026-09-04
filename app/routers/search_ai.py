from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Complaint, Brand
from app.schemas import (
    SearchResults, AIDraftRequest, AIDraftResponse, AIQualityCheck,
    AdSuggestRequest, AdTargetingSuggestion, BrandSearchResult,
)
from app.serializers import complaint_to_list_item, brand_to_out
from app.services.ai_service import smart_draft_complaint, quality_check, suggest_resolution, suggest_ad_targeting
from app.services.search_service import smart_search

router = APIRouter(prefix="/api", tags=["search", "ai"])


@router.get("/search", response_model=SearchResults)
def search(
    q: str = Query(..., min_length=1),
    category: str | None = None,
    status: str | None = None,
    city: str | None = None,
    db: Session = Depends(get_db),
):
    result = smart_search(db, q, category=category, status=status, city=city)

    complaint_items = [
        complaint_to_list_item(c, match_reasons=reasons)
        for _, c, reasons in result["complaints"]
    ]

    brand_items = []
    for _, b, reasons in result["brands"]:
        base = brand_to_out(b)
        brand_items.append(BrandSearchResult(**base.model_dump(), match_reasons=reasons))

    return SearchResults(
        complaints=complaint_items,
        brands=brand_items,
        query=q,
        expanded_terms=result["terms"][:15],
        total=len(complaint_items) + len(brand_items),
        search_mode="smart",
    )


@router.post("/ai/draft", response_model=AIDraftResponse)
def ai_draft(data: AIDraftRequest):
    result = smart_draft_complaint(data.raw_text)
    return AIDraftResponse(
        title=result.get("title", ""),
        description=result.get("description", data.raw_text),
        category=result.get("category", "Other"),
        brand_name=result.get("brand_name"),
        product_name=result.get("product_name"),
        city=result.get("city"),
        area=result.get("area"),
        amount=result.get("amount"),
        desired_resolution=result.get("desired_resolution"),
        quality_warnings=result.get("quality_warnings", []),
        suggested_entities={
            "brand": result.get("brand_name"),
            "product": result.get("product_name"),
            "location": f"{result.get('area', '')} {result.get('city', '')}".strip(),
        },
    )


@router.post("/ai/quality-check", response_model=AIQualityCheck)
def ai_quality_check(title: str = "", description: str = ""):
    result = quality_check(description, title)
    return AIQualityCheck(**result)


@router.post("/ai/suggest-ad-targeting", response_model=AdTargetingSuggestion)
def ai_suggest_ad_targeting(data: AdSuggestRequest):
    result = suggest_ad_targeting(data.title, data.description)
    return AdTargetingSuggestion(
        categories=result.get("categories", []),
        keywords=result.get("keywords", []),
        cities=result.get("cities", []),
        locations=result.get("locations", []),
        personas=result.get("personas", []),
        roles=result.get("roles", []),
        reasoning=result.get("reasoning", ""),
    )


@router.get("/ai/suggest-resolution")
def ai_suggest_resolution(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        return {"suggestion": "Investigate and respond promptly."}
    return {"suggestion": suggest_resolution(complaint.description, complaint.category)}


@router.get("/locations")
def list_locations(db: Session = Depends(get_db)):
    from app.models import Location
    locations = db.query(Location).all()
    return [{"id": l.id, "name": l.name, "city": l.city, "area": l.area} for l in locations]


@router.get("/stats/home")
def home_stats(db: Session = Depends(get_db)):
    from app.models import ComplaintStatus
    total = db.query(Complaint).count()
    resolved = db.query(Complaint).filter(
        Complaint.status.in_([ComplaintStatus.RESOLVED, ComplaintStatus.PARTIALLY_RESOLVED])
    ).count()
    brands = db.query(Brand).count()
    return {
        "total_complaints": total,
        "resolved_complaints": resolved,
        "total_brands": brands,
        "resolution_rate": round(resolved / total * 100, 1) if total else 0,
    }
