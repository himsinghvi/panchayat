from fastapi import APIRouter

from app.schemas import SocialApiSourceStatus
from app.services.social_mentions_service import get_social_api_status

router = APIRouter(prefix="/api/social-mentions", tags=["social"])


@router.get("/config", response_model=list[SocialApiSourceStatus])
def social_mentions_config():
    """Return which social API integrations are configured (keys are never exposed)."""
    return get_social_api_status()
