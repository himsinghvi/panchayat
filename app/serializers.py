from sqlalchemy.orm import Session
from app.models import Complaint, Comment, Brand, User, ComplaintStatus
from app.schemas import ComplaintOut, ComplaintListItem, CommentOut, BrandOut, RecentCommentPreview


def brand_to_out(brand: Brand) -> BrandOut:
    resolution_rate = 0.0
    if brand.complaint_count > 0:
        resolution_rate = round((brand.resolved_count / brand.complaint_count) * 100, 1)
    return BrandOut(
        id=brand.id,
        name=brand.name,
        slug=brand.slug,
        category=brand.category,
        description=brand.description,
        logo_url=brand.logo_url,
        website=brand.website,
        headquarters=brand.headquarters,
        verification_status=brand.verification_status,
        average_rating=brand.average_rating,
        complaint_count=brand.complaint_count,
        resolved_count=brand.resolved_count,
        resolution_rate=resolution_rate,
        response_rate=brand.response_rate,
        avg_response_hours=brand.avg_response_hours,
    )


def _author_name(complaint: Complaint) -> str:
    if complaint.is_anonymous:
        return "Anonymous Consumer"
    if complaint.author:
        return complaint.author.display_name
    return complaint.guest_name or "Guest User"


def _recent_comments(complaint: Complaint) -> list[RecentCommentPreview]:
    comments = sorted(complaint.comments or [], key=lambda c: c.created_at, reverse=True)[:3]
    result = []
    for c in comments:
        author = c.guest_name or (c.author.display_name if c.author else "Guest")
        result.append(RecentCommentPreview(
            author_name=author,
            body=c.body,
            is_official_brand_reply=c.is_official_brand_reply,
            created_at=c.created_at,
        ))
    return result


def complaint_to_list_item(complaint: Complaint, match_reasons: list[str] | None = None) -> ComplaintListItem:
    has_response = complaint.status in (
        ComplaintStatus.BUSINESS_RESPONDED,
        ComplaintStatus.RESOLUTION_PROPOSED,
        ComplaintStatus.RESOLVED,
        ComplaintStatus.PARTIALLY_RESOLVED,
    )
    return ComplaintListItem(
        id=complaint.id,
        case_number=complaint.case_number,
        title=complaint.title,
        description=complaint.description[:200] + ("..." if len(complaint.description) > 200 else ""),
        category=complaint.category,
        status=complaint.status.value,
        rating=complaint.rating,
        weight_score=complaint.weight_score,
        me_too_count=complaint.me_too_count,
        comment_count=len(complaint.comments or []) or complaint.comment_count,
        recent_comments=_recent_comments(complaint),
        ai_summary=complaint.ai_summary,
        city=complaint.city,
        area=complaint.area,
        author_name=_author_name(complaint),
        brand_name=complaint.brand.name if complaint.brand else complaint.brand_name_free,
        brand_id=complaint.brand_id,
        created_at=complaint.created_at,
        has_brand_response=has_response,
        evidence_count=len(complaint.evidence_urls or []),
        match_reasons=match_reasons or [],
    )


def _comment_tree(comments: list, parent_id=None) -> list[CommentOut]:
    result = []
    for c in comments:
        if c.parent_id == parent_id:
            author = "Anonymous" if not c.author else c.author.display_name
            if c.guest_name:
                author = c.guest_name
            result.append(CommentOut(
                id=c.id,
                body=c.body,
                author_name=author,
                is_official_brand_reply=c.is_official_brand_reply,
                upvote_count=c.upvote_count,
                created_at=c.created_at,
                replies=_comment_tree(comments, c.id),
            ))
    return result


def complaint_to_out(complaint: Complaint) -> ComplaintOut:
    return ComplaintOut(
        id=complaint.id,
        case_number=complaint.case_number,
        title=complaint.title,
        description=complaint.description,
        category=complaint.category,
        complaint_type=complaint.complaint_type,
        severity=complaint.severity,
        rating=complaint.rating,
        status=complaint.status.value,
        visibility=complaint.visibility,
        evidence_level=complaint.evidence_level,
        evidence_urls=complaint.evidence_urls or [],
        weight_score=complaint.weight_score,
        me_too_count=complaint.me_too_count,
        upvote_count=complaint.upvote_count,
        comment_count=complaint.comment_count,
        ai_summary=complaint.ai_summary,
        ai_sentiment=complaint.ai_sentiment,
        ai_topics=complaint.ai_topics or [],
        product_name=complaint.product_name,
        purchase_date=complaint.purchase_date,
        amount=complaint.amount,
        desired_resolution=complaint.desired_resolution,
        city=complaint.city,
        area=complaint.area,
        resolution_rating=complaint.resolution_rating,
        resolution_feedback=complaint.resolution_feedback,
        is_anonymous=complaint.is_anonymous,
        author_name=_author_name(complaint),
        author_credibility=complaint.author.credibility_score if complaint.author else 30.0,
        author_verified=complaint.author.verified if complaint.author else False,
        brand_name=complaint.brand.name if complaint.brand else complaint.brand_name_free,
        brand_id=complaint.brand_id,
        brand_verified=complaint.brand.verification_status == "verified" if complaint.brand else False,
        location_name=complaint.location.name if complaint.location else None,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
        resolved_at=complaint.resolved_at,
        timeline=[{
            "id": e.id, "event_type": e.event_type, "title": e.title,
            "description": e.description, "actor_name": e.actor_name, "created_at": e.created_at,
        } for e in (complaint.timeline or [])],
        resolutions=[{
            "id": r.id, "resolution_type": r.resolution_type, "description": r.description,
            "status": r.status.value, "consumer_response": r.consumer_response,
            "rejection_reason": r.rejection_reason, "created_at": r.created_at,
            "confirmed_at": r.confirmed_at,
        } for r in (complaint.resolutions or [])],
        comments=_comment_tree(complaint.comments or []),
    )
