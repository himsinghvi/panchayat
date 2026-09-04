from app.models import User, Complaint


# Weight multipliers — logged-in users get more visibility & faster resolution priority
GUEST_WEIGHT = 0.4
ANONYMOUS_WEIGHT = 0.5
REGISTERED_WEIGHT = 1.0
VERIFIED_WEIGHT = 1.3
HIGH_CREDIBILITY_WEIGHT = 1.5
EVIDENCE_BONUS = 0.2  # per evidence item, max 0.6


def calculate_complaint_weight(
    user: User | None,
    is_anonymous: bool = False,
    evidence_count: int = 0,
    guest: bool = False,
) -> float:
    if guest or user is None:
        base = GUEST_WEIGHT
    elif is_anonymous:
        base = ANONYMOUS_WEIGHT
    else:
        base = REGISTERED_WEIGHT * (user.weight_multiplier or 1.0)
        if user.verified:
            base *= VERIFIED_WEIGHT / REGISTERED_WEIGHT
        if user.credibility_score and user.credibility_score >= 70:
            base *= HIGH_CREDIBILITY_WEIGHT / REGISTERED_WEIGHT

    evidence_bonus = min(evidence_count * EVIDENCE_BONUS, 0.6)
    return round(base + evidence_bonus, 2)


def get_priority_label(weight: float) -> str:
    if weight >= 1.3:
        return "High Priority"
    if weight >= 0.8:
        return "Standard"
    return "Guest — Login for faster resolution"


def get_weight_explanation(user: User | None, guest: bool) -> str:
    if guest or user is None:
        return "Guest posts are visible but weighted lower. Login to be heard better and resolved faster."
    if user.verified:
        return "Verified account — your complaint carries higher trust and priority."
    return "Registered user — your voice matters. Add evidence to increase weight."
