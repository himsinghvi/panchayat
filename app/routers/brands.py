from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.database import get_db
from app.models import Brand, Complaint, ComplaintStatus, Comment, User, UserRole
from app.schemas import BrandOut, ComplaintListItem, DashboardStats, SocialMentionsResponse
from app.services.social_mentions_service import fetch_social_mentions
from app.serializers import brand_to_out, complaint_to_list_item
from app.auth import get_current_user, require_role

router = APIRouter(prefix="/api/brands", tags=["brands"])


@router.get("", response_model=list[BrandOut])
def list_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).order_by(Brand.complaint_count.desc()).all()
    return [brand_to_out(b) for b in brands]


@router.get("/{brand_id}", response_model=BrandOut)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(404)
    return brand_to_out(brand)


@router.get("/slug/{slug}", response_model=BrandOut)
def get_brand_by_slug(slug: str, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.slug == slug).first()
    if not brand:
        raise HTTPException(404)
    return brand_to_out(brand)


@router.get("/{brand_id}/social-mentions", response_model=SocialMentionsResponse)
def get_brand_social_mentions(
    brand_id: int,
    platforms: str = Query("all"),
    db: Session = Depends(get_db),
):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(404)
    platform_list = [p.strip().lower() for p in platforms.split(",") if p.strip()]
    result = fetch_social_mentions(
        brand_name=brand.name,
        title="",
        description=brand.description or "",
        category=brand.category or "",
        brand_slug=brand.slug,
        platforms=platform_list,
    )
    result["brand_id"] = brand_id
    return result


@router.get("/{brand_id}/complaints", response_model=list[ComplaintListItem])
def brand_complaints(brand_id: int, db: Session = Depends(get_db)):
    complaints = db.query(Complaint).options(
        joinedload(Complaint.author),
        joinedload(Complaint.brand),
        joinedload(Complaint.comments).joinedload(Comment.author),
    ).filter(Complaint.brand_id == brand_id).order_by(Complaint.created_at.desc()).all()
    return [complaint_to_list_item(c) for c in complaints]


@router.get("/dashboard/stats", response_model=DashboardStats)
def brand_dashboard_stats(
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.BRAND_REP, UserRole.ADMIN)),
):
    brand = db.query(Brand).filter(Brand.claimed_by_user_id == user.id).first()
    if not brand and user.role != UserRole.ADMIN:
        raise HTTPException(404, "No brand claimed")

    q = db.query(Complaint)
    if brand:
        q = q.filter(Complaint.brand_id == brand.id)
    all_c = q.all()
    open_c = [c for c in all_c if c.status not in (
        ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED, ComplaintStatus.PARTIALLY_RESOLVED
    )]
    resolved = [c for c in all_c if c.status == ComplaintStatus.RESOLVED]
    rate = (len(resolved) / len(all_c) * 100) if all_c else 0

    categories = {}
    for c in all_c:
        categories[c.category] = categories.get(c.category, 0) + 1
    trending = sorted([{"category": k, "count": v} for k, v in categories.items()],
                      key=lambda x: -x["count"])[:5]

    return DashboardStats(
        total_complaints=len(all_c),
        open_complaints=len(open_c),
        resolved_complaints=len(resolved),
        resolution_rate=round(rate, 1),
        avg_response_hours=brand.avg_response_hours if brand else 0,
        trending_categories=trending,
    )
