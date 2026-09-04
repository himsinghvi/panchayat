# Consumer Experience, Review & Grievance Platform — Product & Engineering Blueprint

## 1. Product Vision

Build a consumer-first public platform where people can:

- Share product/service experiences.
- Publish reviews, complaints, grievances, warnings, and appreciation.
- Tag shops, brands, products, services, people, locations, categories, and relevant organizations.
- Discuss complaints publicly.
- Allow brands/retailers/service providers to claim profiles and respond.
- Allow brands to propose a resolution and mark a complaint as resolved.
- Require the original consumer to confirm whether the issue is actually resolved.
- Preserve the complete history of the complaint, including updated feedback.
- Help other consumers discover recurring issues and trustworthy experiences.
- Create a transparent reputation layer for brands, sellers, products, and locations.
- Aggregate complaints into trends without unfairly declaring guilt.
- Provide a structured escalation path to official consumer-protection channels where appropriate.

The product should be positioned as a **consumer experience and resolution network**, not as a platform that automatically determines that a business is guilty.

Suggested working names:
- GrahakVoice
- ConsumerVoice
- ResolveNow
- GrahakConnect
- ConsumerPulse
- ReviewResolve
- GrahakSetu
- Voice of Consumer

---

# 2. Core Product Principle

The platform should separate:

1. **What the consumer says**
2. **What evidence exists**
3. **What the business says**
4. **What resolution was proposed**
5. **Whether the consumer accepted the resolution**
6. **What happened afterward**

Every complaint should therefore behave like a transparent case/ticket with a public conversation and immutable activity history.

Example:

Consumer:
> Purchased washing machine on 10 Aug. Installation was promised within 48 hours but did not happen.

Brand:
> We apologize. Installation has been scheduled for 14 Aug.

Consumer:
> Technician visited on 14 Aug and installation completed.

System:
> Resolution proposed → Consumer confirmed resolved.

Consumer follow-up:
> Issue resolved. Installation was delayed by 2 days, but support team eventually helped.

This creates a much more useful record than a simple 1–5 star review.

---

# 3. Target Users

## 3.1 Consumers

People who purchased or used a product/service.

Goals:
- Share experience.
- Get help.
- Warn others.
- Praise good service.
- Track complaint progress.
- Communicate with brands.
- Maintain evidence.
- Discover other consumer experiences.

## 3.2 Brands

Manufacturers, service providers, retailers, marketplaces, banks, telecom companies, restaurants, hospitals, travel companies, etc.

Goals:
- Monitor complaints.
- Respond publicly.
- Resolve issues.
- Improve reputation.
- Identify recurring problems.
- Manage official brand presence.

## 3.3 Retailers / Local Businesses

Especially useful for India where consumers often purchase from local stores.

Goals:
- Claim shop profile.
- Respond to complaints.
- Handle customer conversations.
- Build reputation.

## 3.4 Community Members

People who did not create the original complaint but have relevant experience.

They can:
- Comment.
- Share similar experiences.
- Upvote useful information.
- Confirm recurring patterns.
- Add factual information.

## 3.5 Moderators

Review content, handle abuse, fraud, impersonation, privacy issues, disputes and legal requests.

## 3.6 Platform Administrators

Manage:
- Users
- Brands
- Locations
- Categories
- Complaints
- Moderation
- Reports
- Analytics
- Verification
- Trust & safety

---

# 4. Core Objects / Domain Model

The platform should be designed around these primary entities:

## User

Fields:
- id
- name
- username
- email
- phone
- profile_photo
- city
- country
- account_type
- verification_status
- created_at
- updated_at
- privacy_settings
- reputation_score

## Brand

Fields:
- id
- name
- logo
- description
- website
- categories
- official_social_links
- headquarters
- verification_status
- claimed_by
- average_rating
- complaint_count
- resolved_count
- resolution_rate
- response_rate
- response_time
- profile_status

## Retailer / Business

Fields:
- id
- name
- address
- latitude
- longitude
- city
- state
- pincode
- phone
- website
- categories
- owner_user_id
- verification_status

## Product

Fields:
- id
- brand_id
- product_name
- model_number
- category
- description
- specifications
- average_rating
- complaint_count

## Complaint

Fields:
- id
- public_case_number
- author_id
- title
- description
- complaint_type
- category
- severity
- brand_id
- retailer_id
- product_id
- location_id
- purchase_date
- incident_date
- amount
- desired_resolution
- status
- visibility
- evidence_level
- created_at
- updated_at
- resolved_at
- resolution_confirmed_at
- resolution_confirmed_by
- sentiment
- moderation_status

## Complaint Status

Recommended lifecycle:

DRAFT
→ PUBLISHED
→ AWAITING_RESPONSE
→ BUSINESS_RESPONDED
→ RESOLUTION_PROPOSED
→ CONSUMER_REVIEWING
→ RESOLVED_PENDING_CONFIRMATION
→ RESOLVED
→ PARTIALLY_RESOLVED
→ NOT_RESOLVED
→ REOPENED
→ ESCALATED
→ CLOSED

Important:
A brand should NOT be able to unilaterally mark a consumer complaint as permanently resolved.

## Complaint Update

A timeline event attached to a complaint.

Examples:
- Consumer added evidence.
- Brand responded.
- Brand proposed replacement.
- Consumer rejected proposed resolution.
- Appointment scheduled.
- Product replaced.
- Consumer confirmed resolution.
- Complaint reopened.

## Evidence

Types:
- Invoice
- Receipt
- Warranty
- Photo
- Video
- Email
- Chat screenshot
- Service report
- Delivery proof
- Payment proof
- Other document

Each evidence item should have:
- id
- complaint_id
- uploader_id
- type
- file_url
- metadata
- visibility
- uploaded_at
- moderation_status

Sensitive information should be automatically detected/redacted where possible.

## Discussion / Comment

Fields:
- id
- complaint_id
- author_id
- parent_comment_id
- content
- attachments
- created_at
- edited_at
- moderation_status

## Resolution

Fields:
- id
- complaint_id
- proposed_by
- resolution_type
- description
- promised_date
- completed_date
- status
- consumer_response
- created_at

Resolution types:
- Refund
- Replacement
- Repair
- Exchange
- Installation
- Delivery
- Cancellation
- Warranty service
- Compensation
- Apology
- Information provided
- Other

## Review

A review can exist independently or be generated after a complaint.

Fields:
- overall_rating
- product_rating
- service_rating
- value_rating
- review_text
- would_recommend
- verified_purchase
- linked_complaint_id
- created_at

## Location

Support:
- Country
- State
- City
- Area
- Pincode
- Exact business location

Use geospatial indexing.

---

# 5. Complaint Creation Experience

The complaint creation flow should be extremely easy.

## Step 1 — What happened?

Options:

- Bad product
- Defective product
- Poor service
- Refund issue
- Replacement issue
- Warranty issue
- Delivery issue
- Installation issue
- Overcharging
- Misleading advertisement
- Staff behavior
- Fraud/suspicious activity
- Billing issue
- Cancellation issue
- Subscription issue
- Other

## Step 2 — Who is involved?

Search/select:
- Brand
- Shop
- Retailer
- Product
- Service provider

Allow creation if the entity does not exist.

## Step 3 — Where?

Location:
- Store
- Service location
- Delivery location
- City
- Area

Exact location should be optional.

## Step 4 — Tell your story

Use guided fields:
- What did you purchase?
- When?
- How much did you pay?
- What happened?
- What was promised?
- What went wrong?
- What have you tried?
- What resolution do you want?

Also allow free-form description.

## Step 5 — Evidence

Upload:
- Invoice
- Photos
- Videos
- Screenshots
- Warranty documents

## Step 6 — Publish settings

Options:
- Public
- Public but hide my identity
- Private to brand and platform
- Anonymous public complaint

The platform should explain that anonymous/public claims may receive less trust unless evidence exists.

## Step 7 — Preview

Show:

> This is how your complaint will appear publicly.

Require user confirmation before publishing.

---

# 6. AI-Assisted Complaint Creation

AI should help structure the complaint but should never invent facts.

Capabilities:

## Smart Draft

User enters:

> Bought AC from XYZ shop. They promised installation next day. Nobody came for 4 days.

AI converts it into:

Title:
> AC installation delayed for 4 days after purchase

Structured fields:
- Category: Installation
- Retailer: XYZ
- Issue: Delayed installation
- Promised timeline: 1 day
- Actual delay: 4 days

## AI Quality Check

Before publishing:

- Detect missing important information.
- Suggest adding invoice.
- Detect aggressive/abusive language.
- Flag potentially defamatory statements.
- Detect personal information.
- Identify duplicate complaints.
- Suggest neutral wording.

Important:
AI must not change the factual meaning.

## AI Entity Detection

Automatically detect:
- Brand
- Shop
- Product
- Model
- Location
- People
- Dates
- Amounts

User must approve detected entities.

---

# 7. Brand / Business Response

Verified brands get a dashboard.

Dashboard:

### Overview
- Open complaints
- New complaints
- Response rate
- Average response time
- Resolution rate
- Reopened cases
- Sentiment
- Trending issues

### Complaint Inbox

Filters:
- New
- Awaiting response
- High priority
- Unresolved
- Escalated
- Resolved
- Reopened

Each complaint shows:

Consumer complaint
→ Evidence
→ Discussion
→ Brand response
→ Resolution proposal
→ Consumer confirmation

---

# 8. Brand Verification

Brand accounts should have different verification levels.

## Level 1 — Unverified

Can:
- Request profile
- Submit ownership claim

## Level 2 — Business Verified

Verify using:
- Official email domain
- Business registration
- Website
- GSTIN
- Other business documents

## Level 3 — Official Brand

Strong verification.

Badge:
> Official Brand

Important:
Verification means the account represents the business. It does NOT mean the platform endorses the business.

---

# 9. Resolution Workflow

This is the most important differentiator.

## Brand proposes resolution

Example:

> We have approved a replacement unit. Delivery is scheduled for 12 September.

Status:
`RESOLUTION_PROPOSED`

Consumer options:

### Accept Resolution

Then:
`RESOLVED_PENDING_CONFIRMATION`

### Reject Resolution

Reason required:
- Not sufficient
- Not completed
- Different from promised
- Still experiencing issue
- Other

### Request Update

Consumer can ask the brand for additional action.

---

# 10. Consumer Confirmation

Brand cannot permanently close a complaint by itself.

Consumer sees:

> Has your issue actually been resolved?

Options:

### Yes, resolved

Complaint:
`RESOLVED`

Consumer can update review.

### Partially resolved

Complaint:
`PARTIALLY_RESOLVED`

### No, still unresolved

Complaint:
`NOT_RESOLVED`

### Reopen

If the issue returns later:
`REOPENED`

---

# 11. Post-Resolution Feedback

After resolution:

Ask:

- Was your issue resolved?
- How satisfied are you?
- How did the brand handle the complaint?
- How quickly was it resolved?
- Would you buy from them again?

Generate:

> Original rating: 1/5  
> Resolution rating: 4/5

This is valuable because a bad initial experience does not necessarily mean bad customer support.

---

# 12. Complaint Timeline

Every complaint should have a highly visual timeline.

Example:

10 Aug — Product purchased
11 Aug — Complaint created
11 Aug — Brand notified
12 Aug — Brand responded
13 Aug — Replacement approved
15 Aug — Replacement delivered
15 Aug — Consumer confirmed resolution
16 Aug — Consumer updated feedback

Timeline events should be immutable once published, except where corrections are explicitly recorded.

---

# 13. Public Complaint Page

URL concept:

`/complaint/CP-2026-001234`

Page layout:

## Header

Complaint title

Status badge:
- Open
- Awaiting Brand
- Resolution Proposed
- Resolved
- Reopened

Entity tags:
- Brand
- Product
- Retailer
- Location

## Consumer Story

Full description.

## Evidence

Evidence gallery.

## Brand Response

Official response highlighted.

## Discussion

Community conversation.

## Resolution

Promised resolution and actual outcome.

## Consumer Confirmation

> Confirmed resolved by the consumer on 15 Sep 2026.

## Updated Feedback

Latest consumer review.

## Related Complaints

Show similar complaints.

---

# 14. Reviews

Reviews should support more than stars.

Rating dimensions:

- Product quality
- Service quality
- Support
- Value for money
- Delivery
- Staff behavior
- Overall experience

Add:
- Verified purchase
- Complaint linked
- Resolved after complaint
- Recommended

Avoid allowing anonymous 1-star spam to dominate reputation scores.

---

# 15. Brand Reputation Score

Do NOT simply calculate:

`average(stars)`

Create a composite score.

Potential inputs:

- Verified reviews
- Complaint volume
- Complaint rate relative to business scale if available
- Response rate
- Average response time
- Resolution rate
- Consumer-confirmed resolution
- Reopened complaint rate
- Recency
- Evidence strength
- Review authenticity

Display multiple metrics rather than one opaque score.

Example:

### Brand Experience

4.2 / 5

Response Rate: 91%
Consumer-confirmed Resolution: 78%
Average Response Time: 11 hours

Use clear methodology documentation.

---

# 16. Location Intelligence

Allow users to browse:

`Pune → Viman Nagar → Electronics Shops`

Location page:

- Top businesses
- Complaints
- Reviews
- Trending issues
- Recently resolved complaints
- Consumer sentiment
- Category breakdown

Map view:

Markers can represent:
- Business
- Complaint
- Service center
- Product location

Privacy:
Do not expose exact consumer home addresses or sensitive locations.

---

# 17. Brand Pages

Example:

`/brand/brand-name`

Sections:

- Overview
- Products
- Reviews
- Complaints
- Resolutions
- Discussions
- Locations
- Statistics
- Official response
- Contact/support links

Example statistics:

- 2,431 reviews
- 318 complaints
- 84% consumer-confirmed resolution
- 89% response rate
- 7h average first response

---

# 18. Product Pages

Example:

`/product/brand/model`

Sections:
- Product overview
- Reviews
- Complaints
- Common problems
- Resolved issues
- Related products
- Community discussions

AI can identify recurring themes.

Example:

> Common issues reported by consumers:
> 1. Installation delays
> 2. Remote-control failures
> 3. Warranty communication

Clearly label these as platform/community-reported patterns, not verified product defects unless independently established.

---

# 19. Discussion System

Users can participate in discussions around a complaint.

Features:
- Comments
- Replies
- Mentions
- Upvotes
- Helpful
- Share
- Report
- Sort by newest/helpful
- Pin official response

Community users can say:

> I faced the same issue.

This can be converted into a linked experience rather than duplicating the complaint.

---

# 20. Similar Complaint Detection

Use semantic search to detect:

- Duplicate complaints
- Same product issue
- Same retailer
- Same location
- Same incident type

Example:

100 consumers report:

> "Installation team never came."

AI clusters them under:

**Installation delays**

But do NOT automatically merge complaints.

---

# 21. Trending Problems

Dashboard:

### Trending Today

- Brand X — Refund complaints
- Store Y — Delivery complaints
- Product Z — Warranty complaints

Metrics should account for:
- Complaint volume
- Unique consumers
- Time period
- Business size where available

Avoid ranking based purely on raw complaint count.

---

# 22. Search

Global search should support:

- Brand
- Product
- Shop
- Complaint
- City
- Pincode
- Category
- Person/business representative
- Keywords

Example searches:

`Samsung AC Pune`

`Viman Nagar electronics shop`

`refund issue Amazon`

`XYZ Model installation`

---

# 23. Advanced Filters

- Location
- Brand
- Product
- Category
- Complaint type
- Status
- Date
- Resolved/unresolved
- Verified purchase
- Evidence available
- Rating
- Business response available

---

# 24. Consumer Dashboard

Sections:

### My Experiences
All reviews.

### My Complaints
Status and timeline.

### Awaiting Brand
Cases requiring business response.

### Resolutions
Resolved and partially resolved cases.

### Follow-ups
Cases requiring consumer confirmation.

### Saved
Saved complaints/brands/products.

### Notifications

---

# 25. Brand Dashboard

### KPI cards

- Open cases
- New today
- Awaiting response
- Resolution rate
- Response rate
- Average response time
- Reopened cases

### Analytics

Charts:
- Complaints over time
- Categories
- Locations
- Products
- Sentiment
- Resolution performance

### Team management

Roles:
- Admin
- Customer Support
- Manager
- Analyst
- Viewer

---

# 26. Notifications

Channels:

- In-app
- Email
- Push
- Optional WhatsApp integration

Events:

Consumer:
- Brand responded
- Resolution proposed
- Brand mentioned you
- Complaint updated
- Community reply
- Resolution confirmation reminder

Brand:
- New complaint
- Consumer replied
- Complaint reopened
- Negative experience trending
- Mention
- Escalation

Allow notification preferences.

---

# 27. Escalation

The platform should provide guidance, not pretend to be a government authority.

Possible options:

> Still unresolved?

Show:
- Contact brand escalation team
- Warranty escalation
- Marketplace grievance officer
- National Consumer Helpline
- Appropriate government authority
- Consumer Commission / e-Jagriti
- Payment dispute route where applicable

Provide contextual information and links to official channels.

---

# 28. Moderation & Trust

This platform will be vulnerable to abuse, so Trust & Safety must be a first-class subsystem.

Detect:

- Spam
- Fake reviews
- Review bombing
- Harassment
- Threats
- Hate speech
- Doxxing
- Personal information
- Extortion
- Impersonation
- Fake brand accounts
- Manipulated evidence
- Coordinated attacks
- Defamation risk

Actions:

- Warning
- Hide temporarily
- Require verification
- Human review
- Remove
- Suspend account
- Ban

Maintain moderation audit logs.

---

# 29. Legal / Defamation Safety

This is extremely important.

The platform should distinguish:

### User allegation

> "I believe the shop overcharged me."

from:

### Platform assertion

> "This shop is fraudulent."

The platform should generally publish the former as a user's experience, with appropriate policies and moderation.

Do not automatically label a company/person as:
- Fraud
- Criminal
- Scammer
- Cheater
- Thief

unless there is an appropriate verified/legal basis and the product's legal policy permits it.

Provide:
- Right of reply
- Content reporting
- Dispute process
- Correction mechanism
- Takedown/legal request workflow
- Privacy controls

Have qualified Indian legal counsel review Terms of Service, Privacy Policy, Content Policy and grievance mechanisms before launch.

---

# 30. Privacy

Never expose:

- Phone numbers
- Email addresses
- Home addresses
- Government IDs
- Payment details
- Bank details
- Card numbers
- Private conversations

Automatically detect sensitive data in uploads.

Potential features:
- PII redaction
- Blur faces
- Blur documents
- Hide invoice numbers
- Hide phone numbers

---

# 31. Evidence Trust Model

Evidence levels:

### Level 0
No evidence.

### Level 1
Consumer-provided description.

### Level 2
Purchase evidence.

### Level 3
Communication evidence.

### Level 4
Service/document evidence.

### Level 5
Business acknowledgement.

Do not call evidence "proof" unless verified appropriately.

---

# 32. Verified Purchase

Possible verification methods:

- Invoice upload
- Order ID
- Marketplace integration
- Email confirmation
- Brand verification
- Receipt

Badge:

> Verified Purchase

Verification should never expose the underlying sensitive information.

---

# 33. AI Features

AI should be an assistant, not the judge.

## AI Complaint Assistant

Convert messy text into structured complaint.

## AI Summarization

Generate:

> Consumer claims...
> Brand response...
> Current status...
> Resolution proposed...

Clearly label as AI-generated summary.

## AI Sentiment

Analyze:
- Consumer sentiment
- Brand response sentiment
- Conversation trajectory

## AI Topic Extraction

Identify:
- Refund
- Delivery
- Installation
- Warranty
- Quality
- Support

## AI Similar Cases

Retrieve related complaints.

## AI Resolution Suggestions

For brands:

> Similar complaints were resolved through replacement.

Do not make legal determinations.

## AI Toxicity / Abuse Detection

Flag content for moderation.

## AI PII Detection

Detect sensitive information.

## AI Duplicate Detection

Identify probable duplicates.

---

# 34. Search Architecture

Use hybrid search.

### Keyword search

Elasticsearch/OpenSearch.

### Semantic search

Vector database or OpenSearch vector search.

### Hybrid ranking

Combine:

`BM25 + semantic similarity + recency + entity match`

Potential stack:
- OpenSearch
- PostgreSQL
- pgvector
- Redis

---

# 35. Recommended Technical Architecture

## Frontend

Recommended:
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Mapbox/Google Maps

Alternative:
- React + Vite

## Backend

Recommended:
- Python FastAPI
- PostgreSQL
- Redis
- Celery/RQ for background jobs

Alternative:
- Node.js/NestJS

## Search

- OpenSearch

## Storage

- S3-compatible object storage

## Authentication

- Email/password
- Google
- Apple
- Phone OTP

For India:
- Optional mobile OTP.

## AI

Provider abstraction supporting:
- OpenAI
- Azure OpenAI
- Anthropic
- Local models

Do not hard-code the product to one model provider.

---

# 36. High-Level Architecture

```text
                    ┌──────────────────┐
                    │     Web / PWA    │
                    │ React / Next.js  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │    API Gateway   │
                    └────────┬─────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
┌──────▼──────┐      ┌───────▼───────┐     ┌──────▼──────┐
│ User Service│      │ Complaint      │     │ Brand       │
│             │      │ Service        │     │ Service     │
└──────┬──────┘      └───────┬───────┘     └──────┬──────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                 ┌───────────▼───────────┐
                 │      PostgreSQL       │
                 └───────────────────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
      ┌──────▼─────┐  ┌──────▼─────┐  ┌──────▼──────┐
      │ OpenSearch │  │ Redis       │  │ Object      │
      │             │  │             │  │ Storage     │
      └─────────────┘  └─────────────┘  └─────────────┘
                             │
                    ┌────────▼────────┐
                    │ AI / ML Services │
                    └─────────────────┘
```

---

# 37. API Design

Use REST initially.

Examples:

## Authentication

`POST /api/v1/auth/register`

`POST /api/v1/auth/login`

`POST /api/v1/auth/verify-otp`

## Complaints

`POST /api/v1/complaints`

`GET /api/v1/complaints/{id}`

`PATCH /api/v1/complaints/{id}`

`POST /api/v1/complaints/{id}/updates`

`POST /api/v1/complaints/{id}/resolve`

`POST /api/v1/complaints/{id}/reopen`

## Brand

`GET /api/v1/brands/{id}`

`POST /api/v1/brands/{id}/claim`

`POST /api/v1/brands/{id}/responses`

## Discussions

`POST /api/v1/complaints/{id}/comments`

`POST /api/v1/comments/{id}/reply`

## Reviews

`POST /api/v1/reviews`

`GET /api/v1/brands/{id}/reviews`

## Search

`GET /api/v1/search?q=...`

---

# 38. Database Design

Use PostgreSQL.

Core tables:

```text
users
user_profiles
user_verifications

brands
brand_users
brand_verifications

retailers
retailer_users
retailer_locations

products
product_models

locations

complaints
complaint_entities
complaint_updates
complaint_status_history

resolutions
resolution_events

reviews

comments
comment_votes

evidence
evidence_access_logs

notifications

reports
moderation_actions

audit_logs

tags
complaint_tags
brand_tags
product_tags

follows
bookmarks

reputation_snapshots
analytics_events
```

Every important state transition should have a history table.

---

# 39. Status State Machine

Implement status transitions centrally.

Example:

```text
DRAFT
  ↓
PUBLISHED
  ↓
AWAITING_RESPONSE
  ↓
BUSINESS_RESPONDED
  ↓
RESOLUTION_PROPOSED
  ↓
RESOLVED_PENDING_CONFIRMATION
  ├──→ RESOLVED
  ├──→ PARTIALLY_RESOLVED
  └──→ NOT_RESOLVED
             ↓
          REOPENED
```

Prevent arbitrary status changes from the frontend.

The backend must validate every transition.

---

# 40. Gamification

Consumer reputation can encourage useful participation.

Badges:

- Helpful Reviewer
- Verified Buyer
- Resolution Champion
- Community Helper
- Local Expert
- Early Contributor

Avoid rewarding users simply for posting more complaints.

Reward:
- Useful evidence
- Accurate information
- Helpful replies
- Confirmed experiences
- Constructive discussions

---

# 41. Community Reputation

Possible score:

```text
Community Score =
  helpful votes
+ verified experiences
+ accepted answers
+ accurate reports
- moderation violations
- spam
```

Do not allow reputation to become a popularity contest.

---

# 42. Business Reputation

Create separate metrics:

### Customer Experience

Rating.

### Responsiveness

Response rate + response time.

### Resolution

Consumer-confirmed resolution.

### Transparency

Rate of cases with public responses.

This prevents one star rating from hiding poor complaint handling.

---

# 43. Monetization

Keep basic consumer functionality free.

Potential revenue:

## Brand SaaS

Paid dashboard:
- Complaint management
- Analytics
- Team inbox
- AI summaries
- Trend detection
- Export
- Integrations

## Premium Analytics

Brands can subscribe to:
- Competitor benchmarking
- Category intelligence
- Location intelligence
- Product issue intelligence

## API

Offer anonymized aggregate data to:
- Research companies
- Enterprises
- Consumer organizations

Strict privacy controls required.

## Advertising

Avoid ads that compromise complaint independence.

Never allow brands to pay to:
- Delete complaints
- Hide complaints
- Improve scores
- Suppress negative reviews

This should be a core trust principle.

---

# 44. Business Model Trust Rule

Create a public policy:

> Businesses can pay for tools, analytics and workflow management. Businesses cannot pay to remove legitimate consumer experiences or alter consumer-confirmed outcomes.

This can become a major differentiator.

---

# 45. Admin Console

Sections:

- Dashboard
- Users
- Brands
- Retailers
- Products
- Complaints
- Reviews
- Reports
- Moderation queue
- Verification queue
- Disputes
- Legal requests
- AI moderation
- Analytics
- Configuration
- Audit logs

---

# 46. Moderation Queue

Each flagged item:

```text
Content
↓
Why flagged
↓
AI confidence
↓
Previous violations
↓
Evidence
↓
Moderator action
```

Actions:
- Approve
- Hide
- Remove
- Request edit
- Escalate
- Suspend user

All actions logged.

---

# 47. Anti-Fraud

Prevent:

- Multiple accounts
- Fake reviews
- Automated posting
- Review manipulation
- Brand-created fake consumer accounts
- Competitor attacks
- Coordinated campaigns

Signals:
- Device fingerprint
- IP reputation
- Posting patterns
- Account age
- Verified purchase
- Similar text
- Velocity
- Behavioral patterns

Use these signals for risk scoring, not automatic guilt.

---

# 48. Notification / SLA Engine

For brands:

Example:

```text
Complaint created
        ↓
Notify brand
        ↓
Response SLA timer
        ↓
No response
        ↓
Reminder
        ↓
Escalation
```

Configurable SLAs by plan/category.

---

# 49. Consumer Journey

```text
Discover problem
      ↓
Search brand/product/shop
      ↓
See existing experiences
      ↓
Create complaint
      ↓
Add evidence
      ↓
Publish
      ↓
Brand notified
      ↓
Brand responds
      ↓
Discussion
      ↓
Resolution proposed
      ↓
Consumer validates
      ↓
Resolved / Partially resolved / Not resolved
      ↓
Updated feedback
```

---

# 50. Brand Journey

```text
Brand claims profile
      ↓
Verification
      ↓
Dashboard
      ↓
New complaint
      ↓
Review evidence
      ↓
Respond
      ↓
Propose resolution
      ↓
Complete action
      ↓
Consumer confirmation
      ↓
Resolution analytics
```

---

# 51. Important UX Screens

Build these screens:

1. Landing page
2. Login
3. Registration
4. Home feed
5. Search
6. Search results
7. Brand profile
8. Product profile
9. Retailer profile
10. Location page
11. Complaint creation
12. Complaint preview
13. Complaint details
14. Complaint timeline
15. Discussion
16. Resolution flow
17. Consumer dashboard
18. Brand dashboard
19. Brand complaint inbox
20. Brand analytics
21. Create review
22. Notifications
23. Saved items
24. User profile
25. Verification
26. Report content
27. Moderation console
28. Admin dashboard
29. Settings
30. Help / policies

---

# 52. Homepage

Recommended structure:

### Hero

> Had a bad experience?  
> Don't just complain. **Make it visible. Get it resolved.**

CTA:
- Share an Experience
- Search a Brand

### Search

> Search brands, products, shops or complaints

### Trending Experiences

Cards showing:
- Complaint
- Brand
- Location
- Status
- Rating

### Recently Resolved

Highlight successful consumer-brand resolutions.

### Trending Brands

Based on activity, not paid ranking.

### Popular Locations

Example:
- Pune
- Mumbai
- Bengaluru
- Delhi
- Hyderabad

### How it works

1. Share
2. Discuss
3. Brand responds
4. Resolve
5. Consumer confirms

---

# 53. Feed

Feed types:

- Trending
- Nearby
- Following
- Recent
- Resolved
- Unresolved
- Discussions

Each card:

```text
[Brand]
Complaint title

Consumer story preview

📍 Viman Nagar, Pune
🏷 Installation
⚠ Open

Brand response: Yes
Evidence: 3 files
Discussion: 18

[View Complaint]
```

---

# 54. Mobile-First Design

Most consumer traffic is likely mobile.

Prioritize:
- Fast complaint creation
- Camera upload
- Location tagging
- Voice-to-text
- Share
- WhatsApp notification
- Push notifications

Use PWA capabilities.

---

# 55. Accessibility

Target WCAG 2.2 AA.

Include:
- Keyboard navigation
- Screen reader support
- Proper labels
- Color-independent statuses
- Focus states
- Large touch targets
- Alt text
- Reduced motion

---

# 56. SEO

Public pages should be indexable.

SEO targets:

`Brand + complaint`

`Product + review`

`Shop + reviews`

`Brand + customer complaints`

`Product + common issues`

Generate structured metadata where appropriate.

Important:
Do not generate thousands of thin AI pages.

---

# 57. Sharing

Every public complaint should have:

- Copy link
- WhatsApp
- LinkedIn
- X
- Facebook
- QR code

Sharing preview:

```text
Consumer complaint against XYZ
Status: Resolution Proposed
Location: Pune
```

Avoid sensationalized previews.

---

# 58. Data Export

Consumer can download:

- Complaint PDF
- Timeline
- Evidence list
- Conversation
- Resolution history

Useful if escalating to an official consumer forum.

---

# 59. Complaint PDF

Generate a formal case summary:

```text
Consumer Experience Report

Case ID
Consumer
Brand
Retailer
Product
Purchase date
Issue
Amount
Description
Evidence
Timeline
Brand response
Resolution
Consumer confirmation
Final feedback
```

Include a disclaimer that the platform is not itself a judicial authority.

---

# 60. API / Integration Opportunities

Future integrations:

- E-commerce marketplaces
- Brand CRM
- Zendesk
- Salesforce
- Freshdesk
- ServiceNow
- WhatsApp
- Email
- Payment providers
- Maps
- GST/business verification
- Official consumer grievance systems where APIs/permissions exist

For integrations, never scrape or access private data without authorization.

---

# 61. Analytics

Consumer analytics:

- Complaint categories
- Resolution time
- Brands
- Locations
- Products
- Trends

Brand analytics:

- Complaint volume
- Response SLA
- Resolution rate
- Reopen rate
- Sentiment
- Product issue clusters
- Location clusters

Platform analytics:

- DAU/MAU
- Complaints/day
- Reviews/day
- Verified purchases
- Brand response rate
- Resolution rate
- Average resolution time
- Community engagement
- Abuse rate

---

# 62. Event Tracking

Track events such as:

```text
user_registered
complaint_started
complaint_published
evidence_uploaded
brand_viewed_complaint
brand_responded
resolution_proposed
consumer_accepted_resolution
consumer_rejected_resolution
complaint_reopened
review_created
comment_created
complaint_shared
search_performed
brand_claimed
```

Use an analytics abstraction so vendors can be swapped.

---

# 63. Security

Implement:

- HTTPS
- JWT/session security
- Password hashing
- MFA for brands/admins
- RBAC
- Rate limiting
- CSRF protection
- Input validation
- SQL injection protection
- XSS protection
- File scanning
- Malware scanning
- Secure object URLs
- Encryption at rest
- Encryption in transit
- Audit logging
- Secret management

---

# 64. File Upload Security

For uploaded evidence:

```text
Upload
 ↓
Virus scan
 ↓
File type validation
 ↓
Metadata sanitization
 ↓
PII detection
 ↓
Optional redaction
 ↓
Object storage
 ↓
Signed URL
```

Never trust MIME type supplied by client.

---

# 65. Observability

Implement:

- Structured logs
- Error tracking
- Metrics
- Distributed tracing
- API latency monitoring
- Background job monitoring

Suggested:
- OpenTelemetry
- Prometheus
- Grafana
- Sentry or equivalent

---

# 66. Testing Strategy

## Unit tests

Services, validators, state transitions.

## Integration tests

Database/API.

## E2E tests

Critical flows:

1. Register
2. Create complaint
3. Upload evidence
4. Brand responds
5. Resolution proposed
6. Consumer confirms
7. Consumer reopens

## Security tests

- Authorization
- File uploads
- Rate limits
- IDOR
- XSS
- SQL injection

## AI tests

- Hallucination
- PII detection
- Toxicity
- Entity extraction
- Duplicate detection
- Summary fidelity

---

# 67. MVP Scope

Do NOT build everything initially.

## MVP Consumer

- Authentication
- User profile
- Search
- Brand/business profiles
- Complaint creation
- Location tagging
- Evidence upload
- Public complaint page
- Comments
- Reviews
- Notifications
- Brand response
- Resolution proposal
- Consumer confirmation
- Reopen complaint
- Basic moderation
- Reporting

## MVP Brand

- Claim profile
- Verification
- Dashboard
- Complaint inbox
- Respond
- Propose resolution
- Mark action completed
- Basic analytics

## MVP Admin

- User management
- Complaint moderation
- Brand verification
- Reports
- Audit logs

---

# 68. Phase 2

- AI complaint assistant
- Similar complaint detection
- Product pages
- Advanced location intelligence
- Reputation analytics
- WhatsApp notifications
- PDF exports
- Advanced search
- PWA
- Community reputation
- Better anti-fraud

---

# 69. Phase 3

- Brand SaaS
- CRM integrations
- Consumer organization partnerships
- Advanced AI analytics
- Voice complaint creation
- Multilingual India support
- Regional language moderation
- API platform

---

# 70. India-First Strategy

Start with:

- Pune
- Mumbai
- Bengaluru
- Delhi NCR
- Hyderabad
- Chennai

Support languages progressively:

1. English
2. Hindi
3. Marathi
4. Tamil
5. Telugu
6. Kannada
7. Bengali
8. Gujarati
9. Malayalam

Use Unicode throughout.

AI translation should preserve the original complaint and clearly distinguish translated content.

---

# 71. Differentiating Features

The product should not become another generic review website.

The strongest differentiators are:

## 1. Complaint → Resolution

Not just reviews.

## 2. Consumer-verified resolution

Brand cannot simply declare victory.

## 3. Full public timeline

Show what happened.

## 4. Brand right of reply

Fairness for businesses.

## 5. Evidence-aware reviews

Separate unsupported opinions from documented experiences.

## 6. Community corroboration

Find people with similar experiences.

## 7. Location intelligence

Understand local businesses and recurring local problems.

## 8. Resolution quality

Measure how companies handle problems, not just how many stars they receive.

---

# 72. Trust Score Philosophy

The platform should communicate:

> A complaint is an allegation/experience reported by a consumer. A response is the business's position. A resolution is confirmed only when the consumer confirms it.

This philosophy should appear in:
- UX
- Help center
- Terms
- Complaint pages
- Brand dashboards

---

# 73. Recommended Product Metrics

North Star Metric:

**Consumer-confirmed successful resolutions**

Supporting metrics:

- New complaints
- Brand response rate
- Median response time
- Resolution rate
- Consumer confirmation rate
- Reopen rate
- Verified complaint percentage
- Repeat complainants
- Community helpfulness
- Complaint-to-resolution conversion

Avoid optimizing only for:
- Number of complaints
- Time spent
- Engagement

Those could incentivize negativity.

---

# 74. Development Strategy for Coding Agents

Give coding agents the following development rules:

## Rule 1

Build in vertical slices, not isolated UI screens.

Example:

```text
Complaint Creation
+ API
+ Database
+ Validation
+ Evidence
+ Notification
+ Public page
```

## Rule 2

Use TypeScript strict mode.

## Rule 3

Use API versioning.

## Rule 4

Keep business logic out of React components.

## Rule 5

Use service/repository architecture in backend.

## Rule 6

All authorization must be server-side.

## Rule 7

All state transitions must be validated server-side.

## Rule 8

Every destructive action requires confirmation.

## Rule 9

Every important action generates an audit event.

## Rule 10

Never let AI invent facts.

## Rule 11

Never expose private evidence accidentally.

## Rule 12

Write tests for every critical workflow.

---

# 75. Suggested Repository Structure

```text
consumer-platform/
│
├── apps/
│   ├── web/
│   ├── api/
│   ├── worker/
│   └── admin/
│
├── packages/
│   ├── ui/
│   ├── types/
│   ├── validation/
│   ├── config/
│   └── ai/
│
├── infrastructure/
│   ├── docker/
│   ├── terraform/
│   └── kubernetes/
│
├── docs/
│
├── tests/
│
└── README.md
```

---

# 76. Coding Agent Instructions

The coding agent should follow this order:

### Step 1

Read this document completely.

### Step 2

Create:
- Architecture
- Database schema
- API contracts
- UX routes
- State machines

### Step 3

Implement authentication.

### Step 4

Implement entities:
- Users
- Brands
- Retailers
- Products
- Locations

### Step 5

Implement complaint lifecycle.

### Step 6

Implement evidence.

### Step 7

Implement public complaint page.

### Step 8

Implement comments/discussions.

### Step 9

Implement brand dashboard.

### Step 10

Implement resolution workflow.

### Step 11

Implement consumer confirmation.

### Step 12

Implement reviews.

### Step 13

Implement moderation.

### Step 14

Implement search.

### Step 15

Implement AI features.

### Step 16

Implement analytics.

### Step 17

Security hardening.

### Step 18

Performance optimization.

### Step 19

E2E testing.

### Step 20

Production deployment.

---

# 77. Acceptance Criteria for MVP

A consumer must be able to:

- Register.
- Search for a brand/shop.
- Create an experience.
- Tag a brand.
- Tag a location.
- Upload evidence.
- Publish complaint.
- Receive brand response.
- Participate in discussion.
- Receive a resolution proposal.
- Accept/reject it.
- Confirm resolution.
- Reopen the case.
- Update feedback.
- Share the complaint.

A brand must be able to:

- Claim its profile.
- Verify identity.
- View complaints.
- Respond.
- Ask questions.
- Propose resolutions.
- Update resolution progress.
- See analytics.

An admin must be able to:

- Moderate.
- Verify brands.
- Review reports.
- Suspend accounts.
- Audit activity.
- Handle disputes.

---

# 78. Example End-to-End Scenario

## Consumer

Himanshu purchases a refrigerator from a local shop in Viman Nagar, Pune.

The refrigerator develops a problem.

He searches:

`Shop Name + Pune`

He discovers 3 existing experiences.

He creates:

> Refrigerator stopped cooling after 12 days.

Uploads:
- Invoice
- Product photo
- Service request screenshot

Tags:
- Brand
- Shop
- Product
- Viman Nagar

Complaint becomes public.

## Brand

The brand receives notification.

Support agent responds:

> We have scheduled a technician tomorrow.

Technician visits.

Brand updates:

> Compressor issue identified. Replacement approved.

Brand proposes:

> Replace compressor within 3 days.

## Consumer

After completion:

> Compressor replaced and refrigerator is working.

Consumer selects:

`Yes — Resolved`

Adds:

> Initial service was frustrating, but the brand eventually resolved it satisfactorily.

Final state:

**Resolved by brand — confirmed by consumer**

This entire journey becomes a useful public record.

---

# 79. Future "Consumer Intelligence" Layer

Once sufficient data exists, build a consumer intelligence engine.

Example:

> Consumers in Pune reported 1,240 appliance service complaints in the last 90 days.

Breakdown:

- 34% installation
- 26% warranty
- 18% delayed service
- 12% refunds
- 10% other

Then:

> 72% received a brand response.

> 61% were consumer-confirmed resolved.

This turns the platform from a review site into a **Consumer Experience Intelligence Network**.

---

# 80. Long-Term Vision

The ultimate product can become:

**"LinkedIn + Reddit + Google Reviews + Consumer Complaint Tracker"**

but focused specifically on consumer experiences and resolution.

The long-term ecosystem can connect:

```text
Consumers
   ↕
Community
   ↕
Brands
   ↕
Retailers
   ↕
Products
   ↕
Locations
   ↕
Consumer Intelligence
```

The platform's most valuable asset will not be the number of reviews.

It will be the structured history of:

**Problem → Evidence → Brand Response → Action → Resolution → Consumer Confirmation → Long-Term Feedback**

That is the core product moat.
