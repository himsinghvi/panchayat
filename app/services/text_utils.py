"""Shared text intelligence: stop-word filtering, entity extraction, keyword generation."""

import re
from typing import Optional

# Common English stop words + generic adjectives that aren't useful as targeting keywords
STOP_WORDS = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "shall",
    "this", "that", "these", "those", "it", "its", "as", "if", "so", "than", "too", "very",
    "just", "also", "only", "both", "each", "all", "any", "some", "no", "not", "can", "about",
    "into", "through", "during", "before", "after", "above", "below", "between", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
    "what", "which", "who", "whom", "whose", "while", "because", "until", "although",
    "your", "our", "their", "my", "his", "her", "its", "you", "they", "them", "his",
    "get", "got", "make", "made", "use", "used", "using", "want", "need", "like",
    "well", "much", "many", "such", "own", "same", "other", "another", "every",
    "and", "or", "nor", "yet", "both", "either", "neither",
})

# Generic adjectives — map to intent keywords instead of using raw
GENERIC_ADJECTIVES = frozenset({
    "best", "good", "great", "nice", "bad", "worst", "better", "worse", "least", "most",
    "more", "less", "top", "new", "old", "big", "small", "high", "low", "free",
    "priced", "price", "pricing", "cost", "costs", "cheap", "expensive", "affordable",
})

# Phrase → semantic keywords (checked before single-word tokenization)
INTENT_PHRASES: list[tuple[str, list[str]]] = [
    ("least priced", ["budget", "affordable", "value for money", "low cost"]),
    ("low cost", ["budget", "affordable", "value for money"]),
    ("low price", ["budget", "affordable", "discount"]),
    ("best price", ["deals", "comparison", "value for money"]),
    ("money back", ["refund", "return policy"]),
    ("customer care", ["support", "service", "helpline"]),
    ("air conditioner", ["AC", "cooling", "appliance"]),
    ("air conditioning", ["AC", "cooling", "appliance"]),
    ("service center", ["warranty", "repair", "support"]),
    ("extended warranty", ["warranty", "protection plan", "electronics"]),
    ("consumer rights", ["legal aid", "complaint", "helpline"]),
    ("not working", ["defect", "repair", "replacement"]),
    ("delayed delivery", ["delivery", "shipping delay", "logistics"]),
    ("installation delay", ["installation", "setup", "technician"]),
]

# Product / brand patterns (preserve casing in output)
PRODUCT_PATTERNS: list[tuple[str, str, list[str]]] = [
    (r"\biphone\s*(\d+\s*(?:pro|max|plus|mini)?)\b", "iPhone {}", ["smartphone", "mobile", "Apple", "electronics"]),
    (r"\bipad\s*(\w*)\b", "iPad {}", ["tablet", "Apple", "electronics"]),
    (r"\bmacbook\s*(\w*)\b", "MacBook {}", ["laptop", "Apple", "computer"]),
    (r"\bgalaxy\s*(\w+)\b", "Galaxy {}", ["smartphone", "Samsung", "mobile"]),
    (r"\bpixel\s*(\d+)\b", "Pixel {}", ["smartphone", "Google", "mobile"]),
    (r"\boneplus\s*(\w+)\b", "OnePlus {}", ["smartphone", "mobile"]),
    (r"\b(\d+(?:\.\d+)?)\s*(?:ton|t)\s*(?:split\s*)?ac\b", "{} Ton AC", ["AC", "air conditioner", "appliance", "cooling"]),
    (r"\bsplit\s*ac\b", "Split AC", ["AC", "appliance", "installation"]),
    (r"\bwashing\s*machine\b", "Washing Machine", ["appliance", "home", "electronics"]),
    (r"\brefrigerator\b|\bfridge\b", "Refrigerator", ["appliance", "home", "electronics"]),
    (r"\bLED\s*TV\b|\bsmart\s*tv\b", "Smart TV", ["television", "electronics", "entertainment"]),
    (r"\bcar\b|\bsedan\b|\bSUV\b", "Automobile", ["automotive", "vehicle", "service"]),
    (r"\btwo\s*wheeler\b|\bbike\b|\bscooter\b", "Two Wheeler", ["automotive", "vehicle"]),
]

BRAND_ALIASES: dict[str, list[str]] = {
    "iphone": ["Apple", "smartphone", "mobile"],
    "ipad": ["Apple", "tablet"],
    "macbook": ["Apple", "laptop"],
    "apple": ["Apple", "electronics", "smartphone"],
    "samsung": ["Samsung", "electronics", "smartphone"],
    "google": ["Google", "Pixel", "technology"],
    "amazon": ["Amazon", "e-commerce", "marketplace"],
    "flipkart": ["Flipkart", "e-commerce", "online shopping"],
    "quickcart": ["e-commerce", "online shopping"],
    "lg": ["LG", "appliance", "electronics"],
    "sony": ["Sony", "electronics"],
    "whirlpool": ["Whirlpool", "appliance"],
    "voltas": ["Voltas", "AC", "appliance"],
    "daikin": ["Daikin", "AC", "cooling"],
    "maruti": ["Maruti", "automotive", "car"],
    "hyundai": ["Hyundai", "automotive", "car"],
    "tata": ["Tata", "automotive"],
}

CATEGORY_SIGNALS: list[tuple[list[str], str, list[str]]] = [
    (["iphone", "ipad", "macbook", "smartphone", "mobile", "phone", "laptop", "tablet", "electronics", "tv", "gadget"], "Product", ["electronics", "consumer tech"]),
    (["ac", "air conditioner", "refrigerator", "washing", "appliance", "fridge"], "Product", ["home appliance", "electronics"]),
    (["installation", "install", "setup", "technician", "fitting"], "Installation", ["home service"]),
    (["refund", "return", "money back", "cashback", "reimburse"], "Refund", ["payment", "e-commerce"]),
    (["delivery", "shipping", "courier", "dispatch", "logistics"], "Delivery", ["e-commerce"]),
    (["warranty", "guarantee", "service center", "repair"], "Warranty", ["after-sales"]),
    (["billing", "invoice", "overcharge", "bill", "charged"], "Billing", ["payment"]),
    (["fraud", "scam", "fake", "counterfeit"], "Safety", ["consumer protection"]),
    (["car", "vehicle", "automotive", "sedan", "service center"], "Service", ["automotive"]),
    (["legal", "rights", "helpline", "court", "consumer commission"], "Other", ["legal aid"]),
    (["budget", "affordable", "cheap", "deal", "discount", "offer"], "Product", ["value shopping", "deals"]),
]

INDIAN_CITIES = [
    "pune", "mumbai", "delhi", "bengaluru", "bangalore", "hyderabad", "chennai",
    "kolkata", "ahmedabad", "jaipur", "nagpur", "lucknow", "kochi", "indore",
]

SEARCH_SYNONYMS = {
    "refund": ["refund", "money back", "return", "reimburse", "cashback"],
    "installation": ["installation", "install", "setup", "fitting", "technician"],
    "delivery": ["delivery", "shipping", "courier", "dispatch", "late", "logistics"],
    "warranty": ["warranty", "guarantee", "service center", "claim", "repair"],
    "billing": ["billing", "overcharge", "invoice", "bill", "charged"],
    "defect": ["defect", "defective", "broken", "faulty", "damaged"],
    "service": ["service", "support", "customer care", "helpline"],
    "fraud": ["fraud", "scam", "cheat", "fake", "suspicious"],
    "delay": ["delay", "delayed", "late", "waiting", "pending"],
    "ac": ["ac", "air conditioner", "air conditioning", "cooling", "appliance"],
    "phone": ["phone", "mobile", "smartphone", "handset", "iphone", "android"],
    "iphone": ["iphone", "apple", "smartphone", "mobile", "ios"],
    "electronics": ["electronics", "gadget", "device", "appliance"],
    "complaint": ["complaint", "grievance", "issue", "problem", "experience"],
    "resolved": ["resolved", "fixed", "closed", "completed"],
    "unresolved": ["unresolved", "open", "pending", "awaiting"],
    "budget": ["budget", "affordable", "cheap", "value", "deal", "discount"],
    "automotive": ["car", "vehicle", "automotive", "sedan", "service"],
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def extract_entities(text: str) -> dict:
    """Extract products, brands, cities from text."""
    lower = text.lower()
    products: list[str] = []
    brands: list[str] = []
    extra_keywords: list[str] = []

    for pattern, label_fmt, kws in PRODUCT_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            if "{}" in label_fmt and m.lastindex:
                products.append(label_fmt.format(m.group(1).strip()).strip())
            else:
                products.append(label_fmt)
            extra_keywords.extend(kws)

    for brand_key, kws in BRAND_ALIASES.items():
        if re.search(rf"\b{re.escape(brand_key)}\b", lower):
            brands.extend(kws)

    cities = [c.title() for c in INDIAN_CITIES if c in lower]

    return {
        "products": list(dict.fromkeys(products)),
        "brands": list(dict.fromkeys(brands)),
        "cities": cities,
        "extra_keywords": list(dict.fromkeys(extra_keywords)),
    }


def extract_intent_keywords(text: str) -> list[str]:
    """Map phrases and intent words to useful targeting keywords."""
    lower = text.lower()
    found: list[str] = []

    for phrase, kws in INTENT_PHRASES:
        if phrase in lower:
            found.extend(kws)

    if re.search(r"\b(?:best|top|leading)\b", lower) and "comparison" not in found:
        found.append("comparison")
        found.append("reviews")
    if re.search(r"\b(?:cheap|affordable|budget|least|lowest)\b", lower):
        found.extend(["budget", "affordable", "value for money"])
    if re.search(r"\b(?:premium|luxury|expensive|high[- ]end)\b", lower):
        found.extend(["premium", "high-end"])
    if re.search(r"\b(?:deal|offer|discount|sale)\b", lower):
        found.extend(["deals", "offers", "discount"])

    return list(dict.fromkeys(found))


def extract_meaningful_tokens(text: str) -> list[str]:
    """Tokenize and keep only meaningful words (no stop words, no bare generics)."""
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9]*|\d+(?:\.\d+)?", text)
    meaningful = []
    for t in tokens:
        low = t.lower()
        if low in STOP_WORDS:
            continue
        if low in GENERIC_ADJECTIVES:
            continue
        if len(low) <= 2 and not low.isdigit():
            continue
        meaningful.append(t if t[0].isupper() else low)
    return meaningful


def extract_categories_and_keywords(title: str, description: str = "") -> dict:
    """
    Intelligent category & keyword extraction for ads and search.
    Returns categories, keywords, cities, personas, reasoning.
    """
    text = _normalize(f"{title} {description}")
    lower = text.lower()

    entities = extract_entities(text)
    intent_kws = extract_intent_keywords(text)
    tokens = extract_meaningful_tokens(text)

    categories: list[str] = []
    keyword_set: list[str] = []

    # Priority: products, brands, entity keywords
    keyword_set.extend(entities["products"])
    keyword_set.extend(entities["brands"])
    keyword_set.extend(entities["extra_keywords"])
    keyword_set.extend(intent_kws)

    # Meaningful tokens (e.g. iPhone stays, "and" dropped)
    for t in tokens:
        if t not in keyword_set and t.lower() not in STOP_WORDS:
            keyword_set.append(t)

    # Category inference from combined signals
    signal_text = " ".join(keyword_set + [lower])
    for signals, category, cat_kws in CATEGORY_SIGNALS:
        if any(s in signal_text for s in signals):
            if category not in categories:
                categories.append(category)
            keyword_set.extend(cat_kws)

    # Deduplicate preserving order, title-case multi-word where appropriate
    seen = set()
    final_keywords: list[str] = []
    for kw in keyword_set:
        key = kw.lower()
        if key in seen or key in STOP_WORDS or key in GENERIC_ADJECTIVES:
            continue
        if len(key) <= 2 and not re.match(r"\d", key):
            continue
        seen.add(key)
        final_keywords.append(kw)

    if not categories:
        categories = ["Product"] if any(
            s in signal_text for s in ["iphone", "phone", "electronics", "appliance", "gadget", "laptop"]
        ) else ["Other"]

    personas = []
    if any(s in signal_text for s in ["appliance", "ac", "installation", "home", "fridge"]):
        personas.append("Frustrated Home Buyer")
    if any(s in signal_text for s in ["budget", "affordable", "refund", "ecommerce", "deal"]):
        personas.append("Budget-Conscious Shopper")
    if any(s in signal_text for s in ["car", "automotive", "vehicle"]):
        personas.append("First-Time Car Owner")

    reasoning_parts = []
    if entities["products"]:
        reasoning_parts.append(f"Detected products: {', '.join(entities['products'])}")
    if entities["brands"]:
        reasoning_parts.append(f"Related brands: {', '.join(entities['brands'])}")
    if intent_kws:
        reasoning_parts.append(f"Intent: {', '.join(intent_kws[:3])}")
    if not reasoning_parts:
        reasoning_parts.append("Extracted meaningful terms from ad copy, filtering filler words.")

    return {
        "categories": categories[:4],
        "keywords": final_keywords[:10],
        "cities": entities["cities"],
        "locations": [],
        "personas": personas[:2],
        "roles": ["consumer"],
        "reasoning": ". ".join(reasoning_parts) + ".",
    }


def search_tokens(query: str) -> list[str]:
    """Build search term list: entities, intent, meaningful tokens, synonyms."""
    text = _normalize(query)
    lower = text.lower()
    terms: list[str] = [lower]

    entities = extract_entities(text)
    for p in entities["products"]:
        terms.append(p.lower())
    for b in entities["brands"]:
        terms.append(b.lower())
    terms.extend(k.lower() for k in extract_intent_keywords(text))
    terms.extend(t.lower() for t in extract_meaningful_tokens(text))

    expanded = set(terms)
    for term in list(terms):
        for key, syns in SEARCH_SYNONYMS.items():
            if term == key or term in syns or key in term:
                expanded.update(s.lower() for s in syns)

    return [t for t in expanded if t and t not in STOP_WORDS and len(t) > 1]
