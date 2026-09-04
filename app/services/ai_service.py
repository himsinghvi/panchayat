import json
import re
from typing import Optional
from openai import AzureOpenAI
from app.config import get_settings

settings = get_settings()


def _get_client() -> Optional[AzureOpenAI]:
    if not settings.azure_openai_api_key or not settings.azure_openai_endpoint:
        return None
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
    )


def _call_ai(system: str, user: str) -> Optional[str]:
    client = _get_client()
    if not client:
        return None
    try:
        response = client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception:
        return None


def smart_draft_complaint(raw_text: str) -> dict:
    """Agentic AI: structure messy complaint text into fields."""
    system = """You are Panchaayat AI assistant for a consumer grievance platform in India.
Convert the user's raw complaint into structured JSON. Never invent facts.
Return ONLY valid JSON with keys: title, description, category, brand_name, product_name, 
city, area, amount (number or null), desired_resolution, quality_warnings (array of strings).
Categories: Product, Service, Billing, Warranty, Safety, Delivery, Installation, Refund, Other."""
    
    result = _call_ai(system, raw_text)
    if result:
        try:
            clean = re.sub(r"```json\s*|\s*```", "", result).strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            pass

    return _fallback_draft(raw_text)


def _fallback_draft(raw_text: str) -> dict:
    """Rule-based fallback when Azure OpenAI is not configured."""
    text = raw_text.strip()
    category = "Other"
    keywords = {
        "installation": "Installation", "refund": "Refund", "delivery": "Delivery",
        "warranty": "Warranty", "billing": "Billing", "service": "Service",
        "defect": "Product", "broken": "Product", "fraud": "Safety",
    }
    lower = text.lower()
    for kw, cat in keywords.items():
        if kw in lower:
            category = cat
            break

    brand_match = re.search(r"(?:from|at|with)\s+([A-Z][A-Za-z0-9\s&]+?)(?:\s+shop|\s+store|\.|,|$)", text)
    brand_name = brand_match.group(1).strip() if brand_match else None

    city_match = re.search(r"(Pune|Mumbai|Delhi|Bengaluru|Bangalore|Hyderabad|Chennai|Kolkata|Nagpur|Jaipur)", text, re.I)
    city = city_match.group(1) if city_match else None

    amount_match = re.search(r"(?:Rs\.?|₹|INR)\s*([\d,]+)", text)
    amount = float(amount_match.group(1).replace(",", "")) if amount_match else None

    title = text[:80] + ("..." if len(text) > 80 else "")
    if len(title) < 20:
        title = f"{category} issue reported by consumer"

    warnings = []
    if amount is None:
        warnings.append("Consider adding the amount paid for stronger credibility.")
    if not brand_name:
        warnings.append("Tag a specific brand or shop name.")
    warnings.append("Upload invoice or photos as evidence to increase trust.")

    return {
        "title": title,
        "description": text,
        "category": category,
        "brand_name": brand_name,
        "product_name": None,
        "city": city,
        "area": None,
        "amount": amount,
        "desired_resolution": "Resolution of the reported issue",
        "quality_warnings": warnings,
    }


def quality_check(text: str, title: str = "") -> dict:
    """AI quality check before publishing."""
    system = """Analyze consumer complaint text for a grievance platform.
Return ONLY JSON: {"warnings":[], "suggestions":[], "pii_detected":bool, "toxicity_score":0-1, "duplicate_hints":[]}
Check for: missing info, abusive language, defamation risk, PII (phone, email, Aadhaar)."""
    
    result = _call_ai(system, f"Title: {title}\n\n{text}")
    if result:
        try:
            clean = re.sub(r"```json\s*|\s*```", "", result).strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            pass

    return _fallback_quality_check(text)


def _fallback_quality_check(text: str) -> dict:
    warnings, suggestions = [], []
    lower = text.lower()

    if len(text) < 50:
        warnings.append("Description is quite short — add more details about what happened.")
    if not re.search(r"\d", text):
        suggestions.append("Include dates or amounts if relevant.")
    
    pii_patterns = [
        (r"\b\d{10}\b", "phone number"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "email address"),
        (r"\b\d{4}\s?\d{4}\s?\d{4}\b", "Aadhaar-like number"),
    ]
    pii_detected = False
    for pattern, label in pii_patterns:
        if re.search(pattern, text):
            pii_detected = True
            warnings.append(f"Possible {label} detected — consider removing personal info.")

    toxic_words = ["idiot", "fraudster", "scammer", "thief", "cheat"]
    toxicity = sum(1 for w in toxic_words if w in lower) * 0.2

    if toxicity > 0:
        warnings.append("Language may be aggressive — consider neutral wording for better visibility.")

    return {
        "warnings": warnings,
        "suggestions": suggestions,
        "pii_detected": pii_detected,
        "toxicity_score": min(toxicity, 1.0),
        "duplicate_hints": [],
    }


def summarize_complaint(title: str, description: str, status: str, brand_response: str = "") -> str:
    system = "Summarize this consumer complaint case in 2-3 neutral sentences. Label as AI-generated."
    user = f"Title: {title}\nDescription: {description}\nStatus: {status}\nBrand response: {brand_response or 'None yet'}"
    result = _call_ai(system, user)
    if result:
        return result
    return f"Consumer reports: {title}. Status: {status.replace('_', ' ').title()}."


def suggest_resolution(complaint_text: str, category: str) -> str:
    system = """You are a customer service advisor. Suggest a resolution approach for the brand.
Be practical, empathetic. Do NOT make legal determinations. Keep under 100 words."""
    result = _call_ai(system, f"Category: {category}\nComplaint: {complaint_text}")
    if result:
        return result
    suggestions = {
        "Refund": "Consider offering a full or partial refund with a clear timeline.",
        "Delivery": "Provide tracking update and expedited delivery or compensation for delay.",
        "Installation": "Schedule installation within 24-48 hours and assign a dedicated technician.",
        "Warranty": "Initiate warranty claim process and provide service center details.",
    }
    return suggestions.get(category, "Acknowledge the issue publicly, investigate internally, and propose a concrete resolution with timeline.")


def suggest_ad_targeting(title: str, description: str = "") -> dict:
    """AI recommends categories, keywords, and targeting for an ad."""
    system = """You are an ad targeting expert for a consumer grievance platform in India.

Given ad title and description, suggest targeting for showing relevant ads to consumers with complaints.

Return ONLY valid JSON:
{
  "categories": ["Product", "Refund"],
  "keywords": ["iPhone", "smartphone", "Apple", "budget", "electronics"],
  "cities": [],
  "locations": [],
  "personas": [],
  "roles": ["consumer"],
  "reasoning": "brief explanation"
}

RULES for keywords:
- NEVER include stop words: and, the, or, best, least, priced, good, very, etc.
- Include: product names (iPhone 17), brands (Apple), categories (electronics), consumer intent (budget, warranty, deals)
- Use 4-10 specific, actionable keywords that match consumer complaint topics
- Keywords should help match ads to relevant complaints (e.g. iPhone ad → smartphone, mobile, Apple, electronics)

Categories (pick 1-3): Product, Service, Billing, Warranty, Safety, Delivery, Installation, Refund, Other."""

    result = _call_ai(system, f"Title: {title}\nDescription: {description}")
    if result:
        try:
            clean = re.sub(r"```json\s*|\s*```", "", result).strip()
            parsed = json.loads(clean)
            return _sanitize_ad_targeting(parsed, title, description)
        except json.JSONDecodeError:
            pass

    return _fallback_ad_targeting(title, description)


def _sanitize_ad_targeting(parsed: dict, title: str, description: str) -> dict:
    """Clean AI output and merge with rule-based extraction."""
    from app.services.text_utils import extract_categories_and_keywords, STOP_WORDS, GENERIC_ADJECTIVES

    fallback = extract_categories_and_keywords(title, description)

    def clean_kw_list(items):
        out = []
        for kw in (items or []):
            k = str(kw).strip()
            if not k or k.lower() in STOP_WORDS or k.lower() in GENERIC_ADJECTIVES:
                continue
            if len(k) <= 2 and not re.match(r"\d", k):
                continue
            out.append(k)
        return out

    ai_keywords = clean_kw_list(parsed.get("keywords", []))
    ai_categories = clean_kw_list(parsed.get("categories", []))

    merged_keywords = list(dict.fromkeys(ai_keywords + fallback["keywords"]))[:10]
    merged_categories = list(dict.fromkeys(ai_categories + fallback["categories"]))[:4]

    return {
        "categories": merged_categories or fallback["categories"],
        "keywords": merged_keywords or fallback["keywords"],
        "cities": parsed.get("cities") or fallback["cities"],
        "locations": parsed.get("locations") or fallback["locations"],
        "personas": parsed.get("personas") or fallback["personas"],
        "roles": parsed.get("roles") or fallback["roles"],
        "reasoning": parsed.get("reasoning") or fallback["reasoning"],
    }


def _fallback_ad_targeting(title: str, description: str) -> dict:
    from app.services.text_utils import extract_categories_and_keywords
    return extract_categories_and_keywords(title, description)


def _tokenize_simple(text: str) -> list[str]:
    from app.services.text_utils import extract_meaningful_tokens
    return extract_meaningful_tokens(text)
