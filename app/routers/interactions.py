from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import (
    Comment, Complaint, ComplaintStatus, Resolution, ResolutionStatus,
    TimelineEvent, User, UserRole, Notification, Brand
)
from app.schemas import CommentCreate, ResolutionCreate, ResolutionRespond
from app.auth import get_current_user_optional, get_current_user, require_role
from app.serializers import complaint_to_out

router = APIRouter(tags=["interactions"])


def _add_timeline(db, complaint_id, event_type, title, description=None, actor=None):
    db.add(TimelineEvent(
        complaint_id=complaint_id,
        event_type=event_type,
        title=title,
        description=description,
        actor_name=actor,
    ))


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


@router.post("/api/complaints/{complaint_id}/comments")
def add_comment(
    complaint_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404)

    is_official = user and user.role == UserRole.BRAND_REP
    comment = Comment(
        complaint_id=complaint_id,
        author_id=user.id if user else None,
        guest_name=data.guest_name if not user else None,
        parent_id=data.parent_id,
        body=data.body,
        is_official_brand_reply=is_official,
    )
    db.add(comment)
    complaint.comment_count = (complaint.comment_count or 0) + 1

    actor = user.display_name if user else (data.guest_name or "Guest")
    if is_official:
        complaint.status = ComplaintStatus.BUSINESS_RESPONDED
        _add_timeline(db, complaint_id, "brand_response", "Official brand response", data.body[:100], actor)
        if complaint.author_id:
            db.add(Notification(
                user_id=complaint.author_id,
                title="Brand responded to your complaint",
                message=data.body[:100],
                notification_type="brand_response",
                link=f"/complaint/{complaint_id}",
            ))
    else:
        _add_timeline(db, complaint_id, "comment", "New community comment", data.body[:80], actor)

    db.commit()
    return _get_complaint_full(complaint_id, db)


@router.post("/api/complaints/{complaint_id}/resolutions")
def propose_resolution(
    complaint_id: int,
    data: ResolutionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.BRAND_REP, UserRole.ADMIN)),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404)

    resolution = Resolution(
        complaint_id=complaint_id,
        proposed_by_user_id=user.id,
        resolution_type=data.resolution_type,
        description=data.description,
        evidence_urls=data.evidence_urls,
        status=ResolutionStatus.PROPOSED,
    )
    db.add(resolution)
    complaint.status = ComplaintStatus.RESOLUTION_PROPOSED
    _add_timeline(db, complaint_id, "resolution_proposed", f"Resolution proposed: {data.resolution_type}",
                  data.description, user.display_name)

    if complaint.author_id:
        db.add(Notification(
            user_id=complaint.author_id,
            title="Resolution proposed for your complaint",
            message=data.description[:100],
            notification_type="resolution_proposed",
            link=f"/complaint/{complaint_id}",
        ))
    db.commit()
    return _get_complaint_full(complaint_id, db)


@router.post("/api/complaints/{complaint_id}/resolutions/{resolution_id}/respond")
def respond_to_resolution(
    complaint_id: int,
    resolution_id: int,
    data: ResolutionRespond,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(404)
    if complaint.author_id != user.id:
        raise HTTPException(403, "Only the original consumer can confirm resolution")

    resolution = db.query(Resolution).filter(
        Resolution.id == resolution_id, Resolution.complaint_id == complaint_id
    ).first()
    if not resolution:
        raise HTTPException(404)

    if data.action == "accept":
        resolution.status = ResolutionStatus.ACCEPTED
        resolution.confirmed_at = datetime.utcnow()
        resolution.consumer_response = data.response
        complaint.status = ComplaintStatus.RESOLVED
        complaint.resolved_at = datetime.utcnow()
        if data.resolution_rating:
            complaint.resolution_rating = data.resolution_rating
        _add_timeline(db, complaint_id, "resolved", "Consumer confirmed resolution", data.response, user.display_name)
        if complaint.brand_id:
            brand = db.query(Brand).filter(Brand.id == complaint.brand_id).first()
            if brand:
                brand.resolved_count = (brand.resolved_count or 0) + 1
    elif data.action == "partial":
        resolution.status = ResolutionStatus.ACCEPTED
        complaint.status = ComplaintStatus.PARTIALLY_RESOLVED
        complaint.resolution_feedback = data.response
        _add_timeline(db, complaint_id, "partial", "Partially resolved", data.response, user.display_name)
    elif data.action == "reject":
        resolution.status = ResolutionStatus.REJECTED
        resolution.rejection_reason = data.rejection_reason
        complaint.status = ComplaintStatus.REOPENED
        _add_timeline(db, complaint_id, "reopened", "Resolution rejected by consumer",
                      data.rejection_reason, user.display_name)
    else:
        raise HTTPException(400, "Invalid action")

    db.commit()
    return _get_complaint_full(complaint_id, db)
