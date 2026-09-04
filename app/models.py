import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, Enum, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(str, enum.Enum):
    CONSUMER = "consumer"
    BRAND_REP = "brand_rep"
    MODERATOR = "moderator"
    ADMIN = "admin"


class ComplaintStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    AWAITING_RESPONSE = "awaiting_response"
    BUSINESS_RESPONDED = "business_responded"
    RESOLUTION_PROPOSED = "resolution_proposed"
    CONSUMER_REVIEWING = "consumer_reviewing"
    RESOLVED = "resolved"
    PARTIALLY_RESOLVED = "partially_resolved"
    NOT_RESOLVED = "not_resolved"
    REOPENED = "reopened"
    ESCALATED = "escalated"
    CLOSED = "closed"


class ResolutionStatus(str, enum.Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    display_name = Column(String(120), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CONSUMER)
    city = Column(String(80), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    credibility_score = Column(Float, default=50.0)
    weight_multiplier = Column(Float, default=1.0)
    verified = Column(Boolean, default=False)
    persona_tag = Column(String(80), nullable=True)
    bio = Column(Text, nullable=True)
    badges = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="author", foreign_keys="Complaint.author_id")
    comments = relationship("Comment", back_populates="author")
    notifications = relationship("Notification", back_populates="user")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(300), nullable=True)
    headquarters = Column(String(200), nullable=True)
    claimed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    verification_status = Column(String(50), default="unclaimed")
    average_rating = Column(Float, default=0.0)
    complaint_count = Column(Integer, default=0)
    resolved_count = Column(Integer, default=0)
    response_rate = Column(Float, default=0.0)
    avg_response_hours = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="brand")
    locations = relationship("Location", back_populates="brand")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    name = Column(String(200), nullable=True)
    address = Column(String(500), nullable=True)
    area = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(20), nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    brand = relationship("Brand", back_populates="locations")
    complaints = relationship("Complaint", back_populates="location")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(30), unique=True, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    guest_name = Column(String(120), nullable=True)
    guest_email = Column(String(120), nullable=True)
    is_anonymous = Column(Boolean, default=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(80), nullable=False)
    complaint_type = Column(String(80), default="complaint")
    severity = Column(String(30), default="medium")
    rating = Column(Integer, default=3)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    brand_name_free = Column(String(200), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    product_name = Column(String(200), nullable=True)
    purchase_date = Column(String(50), nullable=True)
    incident_date = Column(String(50), nullable=True)
    amount = Column(Float, nullable=True)
    desired_resolution = Column(Text, nullable=True)
    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.PUBLISHED)
    visibility = Column(String(30), default="public")
    evidence_level = Column(Integer, default=0)
    evidence_urls = Column(JSON, default=list)
    weight_score = Column(Float, default=1.0)
    me_too_count = Column(Integer, default=0)
    upvote_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    ai_summary = Column(Text, nullable=True)
    ai_sentiment = Column(String(30), nullable=True)
    ai_topics = Column(JSON, default=list)
    city = Column(String(100), nullable=True)
    area = Column(String(100), nullable=True)
    resolution_rating = Column(Integer, nullable=True)
    resolution_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    author = relationship("User", back_populates="complaints", foreign_keys=[author_id])
    brand = relationship("Brand", back_populates="complaints")
    location = relationship("Location", back_populates="complaints")
    comments = relationship("Comment", back_populates="complaint", order_by="Comment.created_at")
    timeline = relationship("TimelineEvent", back_populates="complaint", order_by="TimelineEvent.created_at")
    resolutions = relationship("Resolution", back_populates="complaint", order_by="Resolution.created_at")
    votes = relationship("Vote", back_populates="complaint")


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    event_type = Column(String(80), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    actor_name = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("Complaint", back_populates="timeline")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    guest_name = Column(String(120), nullable=True)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    body = Column(Text, nullable=False)
    is_official_brand_reply = Column(Boolean, default=False)
    upvote_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("Complaint", back_populates="comments")
    author = relationship("User", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])


class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    proposed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolution_type = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(ResolutionStatus), default=ResolutionStatus.PROPOSED)
    consumer_response = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    evidence_urls = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)

    complaint = relationship("Complaint", back_populates="resolutions")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), nullable=True)
    vote_type = Column(String(20), default="me_too")
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("Complaint", back_populates="votes")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    link = Column(String(300), nullable=True)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    link_url = Column(String(500), nullable=True)
    advertiser = Column(String(150), nullable=True)
    categories = Column(JSON, default=list)
    keywords = Column(JSON, default=list)
    cities = Column(JSON, default=list)
    locations = Column(JSON, default=list)
    personas = Column(JSON, default=list)
    roles = Column(JSON, default=list)
    placement = Column(String(50), default="sidebar")
    active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    target_type = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    reported_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reason = Column(String(200), nullable=False)
    status = Column(String(30), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
