from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Auth
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    display_name: str
    city: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    display_name: str
    role: str
    city: Optional[str] = None
    avatar_url: Optional[str] = None
    credibility_score: float = 50.0
    weight_multiplier: float = 1.0
    verified: bool = False
    persona_tag: Optional[str] = None
    bio: Optional[str] = None
    badges: List[str] = []

    @classmethod
    def from_user(cls, user):
        return cls(
            id=user.id, username=user.username, email=user.email,
            display_name=user.display_name, role=user.role.value if hasattr(user.role, 'value') else user.role,
            city=user.city, avatar_url=user.avatar_url,
            credibility_score=user.credibility_score or 50.0,
            weight_multiplier=user.weight_multiplier or 1.0,
            verified=user.verified or False,
            persona_tag=user.persona_tag, bio=user.bio,
            badges=user.badges or [],
        )

    class Config:
        from_attributes = True


# Complaints
class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: str
    complaint_type: str = "complaint"
    rating: int = Field(ge=1, le=5, default=3)
    brand_id: Optional[int] = None
    brand_name_free: Optional[str] = None
    location_id: Optional[int] = None
    product_name: Optional[str] = None
    purchase_date: Optional[str] = None
    incident_date: Optional[str] = None
    amount: Optional[float] = None
    desired_resolution: Optional[str] = None
    visibility: str = "public"
    is_anonymous: bool = False
    city: Optional[str] = None
    area: Optional[str] = None
    evidence_urls: List[str] = []
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None


class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    resolution_rating: Optional[int] = None
    resolution_feedback: Optional[str] = None


class TimelineEventOut(BaseModel):
    id: int
    event_type: str
    title: str
    description: Optional[str] = None
    actor_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResolutionOut(BaseModel):
    id: int
    resolution_type: str
    description: str
    status: str
    consumer_response: Optional[str] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    confirmed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentOut(BaseModel):
    id: int
    body: str
    author_name: str
    is_official_brand_reply: bool = False
    upvote_count: int = 0
    created_at: datetime
    replies: List["CommentOut"] = []

    class Config:
        from_attributes = True


class ComplaintOut(BaseModel):
    id: int
    case_number: str
    title: str
    description: str
    category: str
    complaint_type: str
    severity: str
    rating: int
    status: str
    visibility: str
    evidence_level: int
    evidence_urls: List[str] = []
    weight_score: float
    me_too_count: int = 0
    upvote_count: int = 0
    comment_count: int = 0
    ai_summary: Optional[str] = None
    ai_sentiment: Optional[str] = None
    ai_topics: List[str] = []
    product_name: Optional[str] = None
    purchase_date: Optional[str] = None
    amount: Optional[float] = None
    desired_resolution: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    resolution_rating: Optional[int] = None
    resolution_feedback: Optional[str] = None
    is_anonymous: bool = False
    author_name: str
    author_credibility: float = 50.0
    author_verified: bool = False
    brand_name: Optional[str] = None
    brand_id: Optional[int] = None
    brand_verified: bool = False
    location_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    timeline: List[TimelineEventOut] = []
    resolutions: List[ResolutionOut] = []
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True


class ComplaintListItem(BaseModel):
    id: int
    case_number: str
    title: str
    description: str
    category: str
    status: str
    rating: int
    weight_score: float
    me_too_count: int = 0
    comment_count: int = 0
    recent_comments: List["RecentCommentPreview"] = []
    ai_summary: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    author_name: str
    brand_name: Optional[str] = None
    brand_id: Optional[int] = None
    created_at: datetime
    has_brand_response: bool = False
    evidence_count: int = 0
    match_reasons: List[str] = []

    class Config:
        from_attributes = True


class RecentCommentPreview(BaseModel):
    author_name: str
    body: str
    is_official_brand_reply: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class AdSuggestRequest(BaseModel):
    title: str
    description: str = ""


class AdTargetingSuggestion(BaseModel):
    categories: List[str] = []
    keywords: List[str] = []
    cities: List[str] = []
    locations: List[str] = []
    personas: List[str] = []
    roles: List[str] = []
    reasoning: str = ""


# Comments
class CommentCreate(BaseModel):
    body: str
    parent_id: Optional[int] = None
    guest_name: Optional[str] = None


# Resolutions
class ResolutionCreate(BaseModel):
    resolution_type: str
    description: str
    evidence_urls: List[str] = []


class ResolutionRespond(BaseModel):
    action: str  # accept, reject, partial
    response: Optional[str] = None
    rejection_reason: Optional[str] = None
    resolution_rating: Optional[int] = None


# Brand
class BrandOut(BaseModel):
    id: int
    name: str
    slug: str
    category: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    verification_status: str
    average_rating: float
    complaint_count: int
    resolved_count: int
    resolution_rate: float = 0.0
    response_rate: float
    avg_response_hours: float

    class Config:
        from_attributes = True


class BrandSearchResult(BrandOut):
    match_reasons: List[str] = []


# AI
class AIDraftRequest(BaseModel):
    raw_text: str


class AIDraftResponse(BaseModel):
    title: str
    description: str
    category: str
    brand_name: Optional[str] = None
    product_name: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    amount: Optional[float] = None
    desired_resolution: Optional[str] = None
    quality_warnings: List[str] = []
    suggested_entities: dict = {}


class AIQualityCheck(BaseModel):
    warnings: List[str]
    suggestions: List[str]
    pii_detected: bool = False
    toxicity_score: float = 0.0
    duplicate_hints: List[str] = []


# Ads
class AdOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    advertiser: Optional[str] = None
    categories: List[str] = []
    keywords: List[str] = []
    cities: List[str] = []
    locations: List[str] = []
    personas: List[str] = []
    roles: List[str] = []
    placement: str
    active: bool = True
    priority: int = 0

    class Config:
        from_attributes = True


class AdCreate(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    advertiser: Optional[str] = None
    categories: List[str] = []
    keywords: List[str] = []
    cities: List[str] = []
    locations: List[str] = []
    personas: List[str] = []
    roles: List[str] = []
    placement: str = "sidebar"
    active: bool = True
    priority: int = 0


class AdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    advertiser: Optional[str] = None
    categories: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    cities: Optional[List[str]] = None
    locations: Optional[List[str]] = None
    personas: Optional[List[str]] = None
    roles: Optional[List[str]] = None
    placement: Optional[str] = None
    active: Optional[bool] = None
    priority: Optional[int] = None


# Search
class SearchResults(BaseModel):
    complaints: List[ComplaintListItem] = []
    brands: List[BrandSearchResult] = []
    query: str
    expanded_terms: List[str] = []
    total: int = 0
    search_mode: str = "smart"


# Dashboard stats
class DashboardStats(BaseModel):
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    resolution_rate: float
    avg_response_hours: float
    trending_categories: List[dict] = []


CommentOut.model_rebuild()
ComplaintListItem.model_rebuild()
