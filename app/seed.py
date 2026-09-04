"""Seed database with dummy personas, brands, complaints, and sample ads."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    User, UserRole, Brand, Location, Complaint, ComplaintStatus,
    TimelineEvent, Comment, Resolution, ResolutionStatus, Ad, Notification
)
from app.auth import hash_password


PERSONAS = [
    {
        "username": "priya_sharma",
        "email": "priya@example.com",
        "display_name": "Priya Sharma",
        "role": UserRole.CONSUMER,
        "city": "Pune",
        "persona_tag": "Frustrated Home Buyer",
        "bio": "IT professional who recently bought appliances. Cares about warranty and installation.",
        "credibility_score": 72,
        "verified": True,
        "badges": ["Verified Buyer", "Helpful Reviewer"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya",
    },
    {
        "username": "rahul_mehta",
        "email": "rahul@example.com",
        "display_name": "Rahul Mehta",
        "role": UserRole.CONSUMER,
        "city": "Mumbai",
        "persona_tag": "Budget-Conscious Shopper",
        "bio": "Compares prices across stores. Posts when refunds are delayed.",
        "credibility_score": 65,
        "verified": True,
        "badges": ["Community Helper"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Rahul",
    },
    {
        "username": "anjali_reddy",
        "email": "anjali@example.com",
        "display_name": "Anjali Reddy",
        "role": UserRole.CONSUMER,
        "city": "Hyderabad",
        "persona_tag": "First-Time Car Owner",
        "bio": "New car owner navigating service centers and warranty claims.",
        "credibility_score": 58,
        "verified": False,
        "badges": ["Early Contributor"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Anjali",
    },
    {
        "username": "vikram_singh",
        "email": "vikram@example.com",
        "display_name": "Vikram Singh",
        "role": UserRole.BRAND_REP,
        "city": "Delhi",
        "persona_tag": "Brand Support Manager",
        "bio": "Customer support lead at CoolBreeze Appliances. Resolves complaints publicly.",
        "credibility_score": 85,
        "verified": True,
        "badges": ["Official Brand Rep"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Vikram",
    },
    {
        "username": "meera_patel",
        "email": "meera@example.com",
        "display_name": "Meera Patel",
        "role": UserRole.CONSUMER,
        "city": "Ahmedabad",
        "persona_tag": "Local Shop Advocate",
        "bio": "Supports local businesses but calls out bad service. Active in community discussions.",
        "credibility_score": 78,
        "verified": True,
        "badges": ["Local Expert", "Resolution Champion"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Meera",
    },
    {
        "username": "arjun_nair",
        "email": "arjun@example.com",
        "display_name": "Arjun Nair",
        "role": UserRole.MODERATOR,
        "city": "Bengaluru",
        "persona_tag": "Community Moderator",
        "bio": "Keeps discussions constructive. Reviews flagged content.",
        "credibility_score": 90,
        "verified": True,
        "badges": ["Moderator", "Trusted Voice"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Arjun",
    },
    {
        "username": "admin",
        "email": "admin@panchaayat.in",
        "display_name": "Platform Admin",
        "role": UserRole.ADMIN,
        "city": "Pune",
        "persona_tag": "Administrator",
        "bio": "Manages platform, ads, and verification queue.",
        "credibility_score": 100,
        "verified": True,
        "badges": ["Admin"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Admin",
    },
    {
        "username": "sneha_kulkarni",
        "email": "sneha@example.com",
        "display_name": "Sneha Kulkarni",
        "role": UserRole.BRAND_REP,
        "city": "Pune",
        "persona_tag": "E-commerce Support Lead",
        "bio": "Handles customer grievances for QuickCart marketplace.",
        "credibility_score": 80,
        "verified": True,
        "badges": ["Official Brand Rep"],
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sneha",
    },
]


BRANDS = [
    {"name": "CoolBreeze Appliances", "slug": "coolbreeze", "category": "Electronics",
     "description": "Home appliances — ACs, refrigerators, washing machines.",
     "headquarters": "Delhi", "verification_status": "verified", "logo_url": "https://api.dicebear.com/7.x/identicon/svg?seed=coolbreeze"},
    {"name": "QuickCart", "slug": "quickcart", "category": "E-commerce",
     "description": "Online marketplace for electronics and daily essentials.",
     "headquarters": "Bengaluru", "verification_status": "verified", "logo_url": "https://api.dicebear.com/7.x/identicon/svg?seed=quickcart"},
    {"name": "MegaMart Electronics", "slug": "megamart", "category": "Retail",
     "description": "Electronics retail chain across Maharashtra.",
     "headquarters": "Pune", "verification_status": "claimed", "logo_url": "https://api.dicebear.com/7.x/identicon/svg?seed=megamart"},
    {"name": "AutoDrive Motors", "slug": "autodrive", "category": "Automotive",
     "description": "Car dealership and service network.",
     "headquarters": "Hyderabad", "verification_status": "verified", "logo_url": "https://api.dicebear.com/7.x/identicon/svg?seed=autodrive"},
    {"name": "FreshFoods Grocery", "slug": "freshfoods", "category": "Grocery",
     "description": "Grocery delivery and hyperlocal stores.",
     "headquarters": "Mumbai", "verification_status": "unclaimed", "logo_url": "https://api.dicebear.com/7.x/identicon/svg?seed=freshfoods"},
    {"name": "TechFix Service Center", "slug": "techfix", "category": "Service",
     "description": "Authorized service center for multiple electronics brands.",
     "headquarters": "Pune", "verification_status": "verified", "logo_url": "https://api.dicebear.com/7.x/identicon/svg?seed=techfix"},
]


SAMPLE_ADS = [
    {"title": "Consumer Rights Helpline Guide", "description": "Free ebook on filing complaints with National Consumer Helpline.",
     "advertiser": "ConsumerAware India", "categories": ["Other", "Safety"], "keywords": ["complaint", "rights", "helpline"],
     "cities": [], "locations": [], "personas": [], "roles": ["consumer"],
     "placement": "sidebar", "link_url": "#", "priority": 5},
    {"title": "Extended Warranty for Electronics", "description": "Protect your AC, fridge & washing machine beyond manufacturer warranty.",
     "advertiser": "ShieldCare", "categories": ["Product", "Warranty"], "keywords": ["warranty", "appliance", "electronics", "AC"],
     "cities": [], "locations": [], "personas": ["Frustrated Home Buyer"], "roles": ["consumer"],
     "placement": "sidebar", "link_url": "#", "priority": 8},
    {"title": "Invoice Organizer App", "description": "Store bills & warranties digitally. Never lose proof of purchase again.",
     "advertiser": "BillBox", "categories": ["Billing", "Product"], "keywords": ["invoice", "receipt", "evidence", "billing"],
     "cities": [], "locations": [], "personas": [], "roles": [],
     "placement": "inline", "link_url": "#", "priority": 7},
    {"title": "AC Installation Experts", "description": "Same-day AC installation in Pune, Mumbai & Bengaluru.",
     "advertiser": "CoolInstall Pro", "categories": ["Installation"], "keywords": ["installation", "AC", "appliance", "delay"],
     "cities": ["Pune", "Mumbai", "Bengaluru"], "locations": ["Koregaon Park", "Viman Nagar", "Andheri"],
     "personas": ["Frustrated Home Buyer"], "roles": ["consumer"],
     "placement": "sidebar", "link_url": "#", "priority": 10},
    {"title": "Refund Tracker Tool", "description": "Track your refund status across e-commerce platforms in one place.",
     "advertiser": "RefundWatch", "categories": ["Refund", "Delivery"], "keywords": ["refund", "delivery", "ecommerce"],
     "cities": ["Mumbai", "Pune"], "locations": [], "personas": ["Budget-Conscious Shopper"], "roles": ["consumer"],
     "placement": "inline", "link_url": "#", "priority": 6},
    {"title": "Legal Aid for Consumer Disputes", "description": "Connect with consumer law advocates for unresolved cases.",
     "advertiser": "NyaySetu", "categories": ["Safety", "Other"], "keywords": ["legal", "dispute", "unresolved", "reopened"],
     "cities": [], "locations": [], "personas": [], "roles": [],
     "placement": "footer", "link_url": "#", "priority": 4},
]


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        users = {}
        for p in PERSONAS:
            user = User(
                username=p["username"],
                email=p["email"],
                password_hash=hash_password("demo123"),
                display_name=p["display_name"],
                role=p["role"],
                city=p["city"],
                persona_tag=p["persona_tag"],
                bio=p["bio"],
                credibility_score=p["credibility_score"],
                verified=p["verified"],
                badges=p["badges"],
                avatar_url=p["avatar_url"],
                weight_multiplier=1.3 if p["verified"] else 1.0,
            )
            db.add(user)
            db.flush()
            users[p["username"]] = user

        brands = {}
        for i, b in enumerate(BRANDS):
            brand = Brand(**b, average_rating=3.5 + (i % 3) * 0.5,
                          complaint_count=0, resolved_count=0,
                          response_rate=75 + i * 3, avg_response_hours=8 + i * 2)
            if b["slug"] == "coolbreeze":
                brand.claimed_by_user_id = users["vikram_singh"].id
            elif b["slug"] == "quickcart":
                brand.claimed_by_user_id = users["sneha_kulkarni"].id
            db.add(brand)
            db.flush()
            brands[b["slug"]] = brand

        locations = [
            Location(brand_id=brands["megamart"].id, name="MegaMart Viman Nagar",
                     area="Viman Nagar", city="Pune", state="Maharashtra", pincode="411014"),
            Location(brand_id=brands["coolbreeze"].id, name="CoolBreeze Service Center Pune",
                     area="Koregaon Park", city="Pune", state="Maharashtra"),
            Location(brand_id=brands["autodrive"].id, name="AutoDrive Hitech City",
                     area="Hitech City", city="Hyderabad", state="Telangana"),
        ]
        for loc in locations:
            db.add(loc)
        db.flush()

        complaints_data = [
            {
                "author": "priya_sharma", "brand": "coolbreeze", "title": "AC installation delayed for 4 days after purchase",
                "description": "Purchased a 1.5 ton split AC from CoolBreeze on 10 Aug. Sales team promised installation within 24 hours. Nobody came for 4 days despite multiple calls to customer care. Had to take leave from office waiting for technicians.",
                "category": "Installation", "rating": 2, "status": ComplaintStatus.RESOLUTION_PROPOSED,
                "city": "Pune", "area": "Koregaon Park", "product_name": "CoolBreeze 1.5T Split AC",
                "amount": 38990, "weight_score": 1.5, "me_too_count": 23, "comment_count": 8,
                "ai_summary": "Consumer claims AC installation was delayed 4 days despite 24-hour promise.",
                "ai_topics": ["installation", "delay", "customer care"],
            },
            {
                "author": "rahul_mehta", "brand": "quickcart", "title": "Refund pending for 3 weeks after return pickup",
                "description": "Returned defective headphones on 5 Aug. Pickup was done on 7 Aug but refund of Rs 2,499 is still not credited. Customer support gives different timelines every time I call.",
                "category": "Refund", "rating": 1, "status": ComplaintStatus.BUSINESS_RESPONDED,
                "city": "Mumbai", "area": "Andheri", "product_name": "SoundMax Pro Headphones",
                "amount": 2499, "weight_score": 1.3, "me_too_count": 45, "comment_count": 12,
                "ai_summary": "Consumer awaiting refund for 3 weeks after successful return pickup.",
                "ai_topics": ["refund", "delay", "ecommerce"],
            },
            {
                "author": "anjali_reddy", "brand": "autodrive", "title": "Free service coupon not honored at service center",
                "description": "Bought a new sedan in June with 3 free services. First free service appointment was cancelled twice. When I finally visited, they said the coupon is not in their system.",
                "category": "Service", "rating": 2, "status": ComplaintStatus.AWAITING_RESPONSE,
                "city": "Hyderabad", "area": "Hitech City", "product_name": "AutoDrive Sedan 2025",
                "amount": 850000, "weight_score": 1.1, "me_too_count": 7, "comment_count": 3,
                "ai_summary": "Free service coupon not recognized at authorized service center.",
                "ai_topics": ["warranty", "service", "coupon"],
            },
            {
                "author": "meera_patel", "brand": "megamart", "title": "Overcharged for extended warranty at Viman Nagar store",
                "description": "Staff at MegaMart Viman Nagar charged Rs 4,500 for extended warranty on a TV that was supposed to be Rs 2,999 as per website. When I showed the website price, manager was rude and refused to adjust.",
                "category": "Billing", "rating": 2, "status": ComplaintStatus.RESOLVED,
                "city": "Pune", "area": "Viman Nagar", "product_name": "SmartTV 55 inch",
                "amount": 4500, "weight_score": 1.5, "me_too_count": 15, "comment_count": 6,
                "resolution_rating": 4, "resolution_feedback": "Manager apologized and refunded the difference after escalation here.",
                "ai_summary": "Billing overcharge resolved after consumer escalation on platform.",
                "ai_topics": ["billing", "overcharge", "warranty"],
            },
            {
                "author": "priya_sharma", "brand": "freshfoods", "title": "Expired products delivered twice in one week",
                "description": "Ordered groceries twice this week. Both times received items past expiry date — milk and yogurt. Very concerning for health.",
                "category": "Safety", "rating": 1, "status": ComplaintStatus.REOPENED,
                "city": "Pune", "area": "Baner", "product_name": "Dairy products",
                "amount": 890, "weight_score": 1.4, "me_too_count": 31, "comment_count": 9,
                "ai_summary": "Repeated delivery of expired dairy products reported.",
                "ai_topics": ["safety", "expiry", "grocery"],
            },
        ]

        for i, cd in enumerate(complaints_data):
            days_ago = 10 - i * 2
            complaint = Complaint(
                case_number=f"CP-2026-{i+1:06d}",
                author_id=users[cd["author"]].id,
                brand_id=brands[cd["brand"]].id,
                title=cd["title"],
                description=cd["description"],
                category=cd["category"],
                rating=cd["rating"],
                status=cd["status"],
                city=cd["city"],
                area=cd["area"],
                product_name=cd["product_name"],
                amount=cd["amount"],
                weight_score=cd["weight_score"],
                me_too_count=cd["me_too_count"],
                comment_count=cd["comment_count"],
                ai_summary=cd["ai_summary"],
                ai_topics=cd["ai_topics"],
                evidence_level=2,
                evidence_urls=["/uploads/sample-invoice.jpg"],
                resolution_rating=cd.get("resolution_rating"),
                resolution_feedback=cd.get("resolution_feedback"),
                created_at=datetime.utcnow() - timedelta(days=days_ago),
                resolved_at=datetime.utcnow() - timedelta(days=1) if cd["status"] == ComplaintStatus.RESOLVED else None,
            )
            db.add(complaint)
            db.flush()

            brands[cd["brand"]].complaint_count += 1
            if cd["status"] == ComplaintStatus.RESOLVED:
                brands[cd["brand"]].resolved_count += 1

            db.add(TimelineEvent(complaint_id=complaint.id, event_type="created",
                                 title="Complaint published", actor_name=users[cd["author"]].display_name,
                                 created_at=complaint.created_at))
            if cd["status"] in (ComplaintStatus.BUSINESS_RESPONDED, ComplaintStatus.RESOLUTION_PROPOSED, ComplaintStatus.RESOLVED):
                db.add(TimelineEvent(complaint_id=complaint.id, event_type="brand_response",
                                     title="Official brand response", actor_name="Brand Support",
                                     created_at=complaint.created_at + timedelta(hours=6)))
            if cd["status"] == ComplaintStatus.RESOLUTION_PROPOSED:
                res = Resolution(complaint_id=complaint.id, proposed_by_user_id=users["vikram_singh"].id,
                                 resolution_type="Installation", status=ResolutionStatus.PROPOSED,
                                 description="Installation scheduled for tomorrow. Dedicated technician assigned. Apology for delay.")
                db.add(res)
                db.add(TimelineEvent(complaint_id=complaint.id, event_type="resolution_proposed",
                                     title="Resolution proposed: Installation",
                                     created_at=complaint.created_at + timedelta(days=1)))
            if cd["status"] == ComplaintStatus.RESOLVED:
                db.add(TimelineEvent(complaint_id=complaint.id, event_type="resolved",
                                     title="Consumer confirmed resolution",
                                     actor_name=users[cd["author"]].display_name,
                                     created_at=complaint.created_at + timedelta(days=5)))

        # Sample comments
        c1 = db.query(Complaint).filter(Complaint.case_number == "CP-2026-000001").first()
        if c1:
            db.add(Comment(complaint_id=c1.id, author_id=users["meera_patel"].id,
                           body="Same thing happened to me in Ahmedabad! Took 5 days for installation.", upvote_count=12))
            db.add(Comment(complaint_id=c1.id, author_id=users["vikram_singh"].id,
                           body="We sincerely apologize. A dedicated team has been assigned to your case. Installation is scheduled for tomorrow.",
                           is_official_brand_reply=True, upvote_count=5))

        for ad in SAMPLE_ADS:
            db.add(Ad(**ad, active=True))

        db.commit()
        print("Database seeded successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
