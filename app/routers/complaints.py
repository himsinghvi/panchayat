from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from app.database import get_db
from app.models import (
    Complaint, ComplaintStatus, TimelineEvent, Brand, User, UserRole, Notification, Comment
)
from app.schemas import (
    ComplaintCreate, ComplaintOut, ComplaintListItem, ComplaintUpdate, SocialMentionsResponse,
)
from app.services.social_mentions_service import fetch_social_mentions
from app.auth import get_current_user_optional, get_current_user, require_role
from app.serializers import complaint_to_out, complaint_to_list_item


from app.services.weight_service import calculate_complaint_weight
from app.services.ai_service import summarize_complaint, quality_check

router = APIRouter(prefix="/api/complaints", tags=["complaints"])


def _get_complaint_full(complaint_id: int, db: Session):
    complaint = db.query(Complaint).options(
        joinedload(Complaint.author),
        joinedload(Complaint.brand),
        joinedload(Complaint.location),
        joinedload(Complaint.timeline),
        joinedload(Complaint.resolutions),
        joinedload(Complaint.comments).joinedload(Comment.author),
    ).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    return complaint_to_out(complaint)


def _next_case_number(db: Session) -> str:
    count = db.query(Complaint).count() + 1
    year = datetime.utcnow().year
    return f"CP-{year}-{count:06d}"


def _add_timeline(db, complaint_id, event_type, title, description=None, actor=None):
    db.add(TimelineEvent(
        complaint_id=complaint_id,
        event_type=event_type,
        title=title,
        description=description,
        actor_name=actor,
    ))


@router.get("", response_model=list[ComplaintListItem])
def list_complaints(
    status: str | None = None,
    category: str | None = None,
    city: str | None = None,
    brand_id: int | None = None,
    feed: str = "recent",
    limit: int = Query(20, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Complaint).options(
        joinedload(Complaint.author),
        joinedload(Complaint.brand),
        joinedload(Complaint.comments).joinedload(Comment.author),
    )
    if status:
        q = q.filter(Complaint.status == status)
    if category:
        q = q.filter(Complaint.category == category)
    if city:
        q = q.filter(Complaint.city.ilike(f"%{city}%"))
    if brand_id:
        q = q.filter(Complaint.brand_id == brand_id)

    if feed == "trending":
        q = q.order_by(desc(Complaint.me_too_count + Complaint.comment_count + Complaint.weight_score))
    elif feed == "resolved":
        q = q.filter(Complaint.status.in_([ComplaintStatus.RESOLVED, ComplaintStatus.PARTIALLY_RESOLVED]))
        q = q.order_by(desc(Complaint.resolved_at))
    else:
        q = q.order_by(desc(Complaint.created_at))

    complaints = q.offset(offset).limit(limit).all()
    return [complaint_to_list_item(c) for c in complaints]


@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    return _get_complaint_full(complaint_id, db)


@router.get("/{complaint_id}/social-mentions", response_model=SocialMentionsResponse)
def get_complaint_social_mentions(
    complaint_id: int,
    platforms: str = Query("all", description="Comma-separated: all,twitter,reddit,linkedin,facebook,instagram,hackernews"),
    db: Session = Depends(get_db),
):
    complaint = db.query(Complaint).options(joinedload(Complaint.brand)).filter(
        Complaint.id == complaint_id
    ).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    brand = complaint.brand
    platform_list = [p.strip().lower() for p in platforms.split(",") if p.strip()]
    result = fetch_social_mentions(
        brand_name=brand.name if brand else "",
        title=complaint.title or "",
        description=complaint.description or "",
        category=complaint.category or "",
        brand_slug=brand.slug if brand else "",
        platforms=platform_list,
    )
    result["complaint_id"] = complaint_id
    return result


@router.post("", response_model=ComplaintOut)
def create_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    guest = user is None
    if guest and not data.guest_name:
        data.guest_name = "Guest User"

    evidence_count = len(data.evidence_urls or [])
    weight = calculate_complaint_weight(user, data.is_anonymous, evidence_count, guest)

    brand = None
    if data.brand_id:
        brand = db.query(Brand).filter(Brand.id == data.brand_id).first()

    qc = quality_check(data.description, data.title)
    evidence_level = min(evidence_count, 5)

    complaint = Complaint(
        case_number=_next_case_number(db),
        author_id=user.id if user else None,
        guest_name=data.guest_name if guest else None,
        guest_email=data.guest_email if guest else None,
        is_anonymous=data.is_anonymous,
        title=data.title,
        description=data.description,
        category=data.category,
        complaint_type=data.complaint_type,
        rating=data.rating,
        brand_id=data.brand_id,
        brand_name_free=data.brand_name_free,
        location_id=data.location_id,
        product_name=data.product_name,
        purchase_date=data.purchase_date,
        incident_date=data.incident_date,
        amount=data.amount,
        desired_resolution=data.desired_resolution,
        visibility=data.visibility,
        evidence_urls=data.evidence_urls,
        evidence_level=evidence_level,
        weight_score=weight,
        city=data.city,
        area=data.area,
        status=ComplaintStatus.AWAITING_RESPONSE,
        ai_topics=qc.get("duplicate_hints", []),
    )
    db.add(complaint)
    db.flush()

    actor = user.display_name if user else (data.guest_name or "Guest")
    _add_timeline(db, complaint.id, "created", "Complaint published", data.description[:100], actor)
    if weight < 0.8:
        _add_timeline(db, complaint.id, "priority", "Lower priority — guest submission",
                      "Login or verify to increase visibility and resolution speed.")

    complaint.ai_summary = summarize_complaint(complaint.title, complaint.description, "awaiting_response")

    if brand:
        brand.complaint_count = (brand.complaint_count or 0) + 1
        if brand.claimed_by_user_id:
            db.add(Notification(
                user_id=brand.claimed_by_user_id,
                title="New complaint received",
                message=f"New complaint: {complaint.title}",
                notification_type="new_complaint",
                link=f"/complaint/{complaint.id}",
            ))

    db.commit()
    return _get_complaint_full(complaint.id, db)


@router.post("/{complaint_id}/me-too")
def me_too(
    complaint_id: int,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404)
    complaint.me_too_count += 1
    db.commit()
    return {"me_too_count": complaint.me_too_count}


@router.patch("/{complaint_id}", response_model=ComplaintOut)
def update_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404)
    if data.resolution_rating is not None:
        complaint.resolution_rating = data.resolution_rating
    if data.resolution_feedback:
        complaint.resolution_feedback = data.resolution_feedback
    db.commit()
    return _get_complaint_full(complaint_id, db)
