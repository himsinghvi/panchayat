from sqlalchemy import inspect, text
from app.database import engine, SessionLocal
from app.models import Ad


def migrate_db():
    """Add new columns to existing tables (SQLite-safe)."""
    insp = inspect(engine)
    if "ads" not in insp.get_table_names():
        return
    existing = {c["name"] for c in insp.get_columns("ads")}
    additions = {
        "cities": "TEXT DEFAULT '[]'",
        "locations": "TEXT DEFAULT '[]'",
        "personas": "TEXT DEFAULT '[]'",
        "roles": "TEXT DEFAULT '[]'",
    }
    with engine.begin() as conn:
        for col, typedef in additions.items():
            if col not in existing:
                conn.execute(text(f"ALTER TABLE ads ADD COLUMN {col} {typedef}"))


AD_TARGETING = {
    "Consumer Rights Helpline Guide": {
        "cities": [], "locations": [], "personas": [], "roles": ["consumer"],
    },
    "Extended Warranty for Electronics": {
        "cities": [], "locations": [], "personas": ["Frustrated Home Buyer"],
        "categories": ["Product", "Warranty"], "keywords": ["warranty", "appliance", "electronics", "AC"],
    },
    "Invoice Organizer App": {
        "cities": [], "locations": [], "personas": [],
        "categories": ["Billing", "Product"], "keywords": ["invoice", "receipt", "evidence", "billing"],
    },
    "AC Installation Experts": {
        "cities": ["Pune", "Mumbai", "Bengaluru"],
        "locations": ["Koregaon Park", "Viman Nagar", "Andheri"],
        "personas": ["Frustrated Home Buyer"],
        "categories": ["Installation"], "keywords": ["installation", "AC", "appliance", "delay"],
    },
    "Refund Tracker Tool": {
        "cities": ["Mumbai", "Pune"],
        "locations": [], "personas": ["Budget-Conscious Shopper"],
        "categories": ["Refund", "Delivery"], "keywords": ["refund", "delivery", "ecommerce"],
    },
    "Legal Aid for Consumer Disputes": {
        "cities": [], "locations": [], "personas": [],
        "categories": ["Safety", "Other"], "keywords": ["legal", "dispute", "unresolved", "reopened"],
    },
}


def sync_ad_targeting():
    """Ensure existing ads have targeting metadata."""
    db = SessionLocal()
    try:
        for ad in db.query(Ad).all():
            if ad.cities is None:
                ad.cities = []
            if ad.locations is None:
                ad.locations = []
            if ad.personas is None:
                ad.personas = []
            if ad.roles is None:
                ad.roles = []
            hints = AD_TARGETING.get(ad.title, {})
            for field in ("cities", "locations", "personas", "roles", "categories", "keywords"):
                if field in hints and not getattr(ad, field):
                    setattr(ad, field, hints[field])
        db.commit()
    finally:
        db.close()


SAMPLE_DISCUSSIONS = [
    ("CP-2026-000002", "rahul_mehta", "Has anyone else waited 3+ weeks for a QuickCart refund?"),
    ("CP-2026-000002", "sneha_kulkarni", "We apologize for the delay. Your refund has been escalated to our payments team.", True),
    ("CP-2026-000003", "anjali_reddy", "AutoDrive service centers need better coupon tracking systems."),
    ("CP-2026-000004", "meera_patel", "Always compare warranty prices online before buying at store!", False),
    ("CP-2026-000005", "priya_sharma", "Expired groceries are a serious health risk. Please be careful."),
]


def sync_sample_comments():
    """Ensure complaints have discussion content, not just counts."""
    from app.models import Complaint, Comment, User
    db = SessionLocal()
    try:
        for case_no, username, body, *rest in SAMPLE_DISCUSSIONS:
            is_official = rest[0] if rest else False
            complaint = db.query(Complaint).filter(Complaint.case_number == case_no).first()
            if not complaint:
                continue
            user = db.query(User).filter(User.username == username).first()
            exists = db.query(Comment).filter(
                Comment.complaint_id == complaint.id, Comment.body == body
            ).first()
            if exists:
                continue
            db.add(Comment(
                complaint_id=complaint.id,
                author_id=user.id if user else None,
                body=body,
                is_official_brand_reply=is_official,
            ))
        db.commit()
        for complaint in db.query(Complaint).all():
            count = db.query(Comment).filter(Comment.complaint_id == complaint.id).count()
            complaint.comment_count = count
        db.commit()
    finally:
        db.close()
