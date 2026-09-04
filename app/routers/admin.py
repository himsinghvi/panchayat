from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ad, User, UserRole, Report, Notification
from app.schemas import AdOut, AdCreate, AdUpdate
from app.auth import require_role, get_current_user_optional, get_current_user
from app.services.ad_service import match_ads

router = APIRouter(tags=["ads", "admin"])


@router.get("/api/ads", response_model=list[AdOut])
def get_ads(
    category: str | None = None,
    keywords: str | None = None,
    city: str | None = None,
    area: str | None = None,
    persona: str | None = None,
    role: str | None = None,
    placement: str = "sidebar",
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    ads = db.query(Ad).filter(Ad.placement == placement).all()
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

    # Enrich context from logged-in user when not explicitly passed
    if user:
        if not persona and user.persona_tag:
            persona = user.persona_tag
        if not city and user.city:
            city = user.city
        if not role and user.role:
            role = user.role.value if hasattr(user.role, "value") else str(user.role)

    matched = match_ads(
        ads, category=category or "", keywords=kw_list,
        city=city or "", area=area or "",
        persona=persona or "", role=role or "",
    )
    if not matched:
        # Fallback: active ads by priority (no targeting restrictions preferred)
        fallback = [a for a in ads if a.active]
        fallback.sort(key=lambda a: (-(a.priority or 0), a.id))
        matched = fallback[:3]
    return [AdOut.model_validate(a) for a in matched if a.active]


@router.get("/api/admin/ads", response_model=list[AdOut])
def admin_list_ads(db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.ADMIN))):
    return [AdOut.model_validate(a) for a in db.query(Ad).order_by(Ad.id).all()]


@router.post("/api/admin/ads", response_model=AdOut)
def create_ad(data: AdCreate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.ADMIN))):
    ad = Ad(**data.model_dump())
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return AdOut.model_validate(ad)


@router.put("/api/admin/ads/{ad_id}", response_model=AdOut)
def update_ad(
    ad_id: int,
    data: AdUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN)),
):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(404, "Ad not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ad, key, value)
    db.commit()
    db.refresh(ad)
    return AdOut.model_validate(ad)


@router.delete("/api/admin/ads/{ad_id}")
def delete_ad(ad_id: int, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.ADMIN))):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(404)
    db.delete(ad)
    db.commit()
    return {"ok": True}


@router.get("/api/notifications")
def get_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    notifs = db.query(Notification).filter(Notification.user_id == user.id).order_by(
        Notification.created_at.desc()
    ).limit(50).all()
    return [{
        "id": n.id, "title": n.title, "message": n.message,
        "type": n.notification_type, "link": n.link, "read": n.read,
        "created_at": n.created_at.isoformat(),
    } for n in notifs]


@router.post("/api/reports")
def report_content(
    target_type: str,
    target_id: int,
    reason: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db.add(Report(target_type=target_type, target_id=target_id,
                  reported_by_user_id=user.id, reason=reason))
    db.commit()
    return {"ok": True, "message": "Report submitted for moderation review"}
