# Event Tech Live CSV Data - Structure and Statistics

**Source Files**:
- `event_tech_live_20251020_152709_summary.csv` (383 bytes)
- `event_tech_live_20251020_152709_companies.csv` (8,100 bytes)
- `event_tech_live_20251020_152709_products.csv` (68,466 bytes)

**Export Date**: October 20, 2025
**Event Date**: November 12-13, 2025

---

## Summary CSV Structure

**Event Information**:
```
Event Name: Event Tech Live
Event URL: https://eventtechlive.com/
Event Date: 12-13 November 2025
Event Location: London, UK
Event Type: conference
```

**Statistics**:
```
Total Companies: 28
Total Products: 214
Companies with Products: 20
Companies without Products: 8
```

**Company Roles**:
```
attendee: 1
partner: 25
speaker: 1
sponsor: 1
```

---

## Companies CSV Structure

**Columns** (12 total):
1. Company Name
2. Website
3. Description
4. Industry
5. Role (attendee, partner, speaker, sponsor)
6. Tier (e.g., "headline" for sponsor)
7. Booth Number (mostly empty)
8. LinkedIn
9. Twitter
10. Logo URL
11. Enriched by Apollo (Yes/No)
12. Enrichment Source (apollo, event_page)

**Data Quality**:
- 28 companies total (rows 2-29)
- All companies have names and roles
- 24 companies have websites (86%)
- 27 companies have descriptions (96%)
- 17 companies have identified industries (61%)
- 22 companies have LinkedIn URLs (79%)
- 18 companies have Twitter handles (64%)
- 24 companies have logo URLs (86%)
- 22 companies enriched by Apollo (79%)
- Booth numbers: All empty (event layout not included)

**Industries Represented**:
- events services (5)
- information technology & services (7)
- translation & localization (1)
- entertainment (1)
- media production (1)
- publishing (1)
- Not specified (12)

**Companies without Products** (8 total):
1. Eventpack
2. Fenix Event Tech
3. FFAIR
4. enviricard
5. Silent Seminars
6. BeCause
7. Event Tech Live
8. Event Technology Awards

---

## Products CSV Structure

**Columns** (9 total):
1. Company Name
2. Company Website
3. Product Name
4. Description
5. Category
6. Pricing
7. Product URL
8. Features (pipe-separated list)
9. Source (multi_strategy, no_products_found, none)

**Data Quality**:
- 214 product entries total (rows 2-224)
- 20 companies with products
- 8 "no products found" entries

**Product Distribution by Company**:
1. Choose 2 Rent: 39 products (18%)
2. One World Rental: 39 products (18%)
3. TransPerfect Live: 9 products
4. IMEX Group: 3 products
5. ExpoPlatform: 6 products
6. Cvent: 8 products
7. 4Wall: 11 products
8. Braindate: 4 products
9. Erleah: 10 products
10. Eventbase: 3 products
11. First Sight Media: 3 products
12. Interprefy: 5 products
13. Komo: 13 products
14. Lineup Ninja: 5 products
15. Memento: 3 products
16. Novum Live: 10 products
17. One Tribe: 14 products
18. Pigeonhole: 10 products
19. PreMagic: 8 products
20. Event Industry News: 4 products

**Product Categories**:
- Service: 84 products (39%)
- Hardware: 59 products (28%)
- Platform: 20 products (9%)
- Feature: 8 products (4%)
- Accessories: 7 products (3%)
- Tool: 4 products (2%)
- Event: 3 products (1%)
- API: 3 products (1%)
- SaaS: 2 products (1%)
- Mobile Application: 1 product (<1%)

**Pricing Models**:
- "Paid": 75 products (35%)
- "Not mentioned": 64 products (30%)
- "Contact for pricing": 26 products (12%)
- "Request a quote" / "Get a quote": 36 products (17%)
- "Free" / "Try for free": 5 products (2%)
- "Tailored pricing": 4 products (2%)
- Various specific plans: 4 products (2%)

**Product URLs**:
- 195 products without URLs (91%)
- 19 products with URLs (9%)
- Note: Most products are services/features within company platforms

**Features**:
- All products have features listed (pipe-separated format)
- Average: 4-6 features per product
- Features are descriptive and benefit-focused

---

## Notable Patterns

### 1. Equipment Rental Dominance
**Choose 2 Rent** and **One World Rental** account for 36% of all products (78 out of 214). This reflects:
- B2B event focus on technology infrastructure
- Importance of hardware in event operations
- Rental model popularity for event equipment

### 2. Category Breakdown Insights

**Services (39%)** dominate because:
- Event production requires many service providers
- Integration, support, and consulting are key
- Many "products" are actually service offerings

**Hardware (28%)** is strong because:
- Physical event tech is essential (badges, kiosks, AV)
- Rental companies list individual hardware items
- B2B events showcase tangible equipment

**Platforms (9%)** represent:
- Core event management solutions
- SaaS offerings for event organizers
- All-in-one solutions

### 3. Pricing Transparency

**65% of products** don't show public pricing:
- "Paid" without specific pricing
- "Contact for pricing"
- "Request a quote"
- "Not mentioned"

This is typical for **B2B enterprise software** where:
- Pricing is customized per customer
- Quotes depend on event size and needs
- Sales process involves demos and consultation

### 4. Feature-Rich Products

All products include detailed feature lists:
- Average 4-6 features per product
- Benefits-focused descriptions
- Clear value propositions
- Technical specifications included

### 5. Data Enrichment

**79% of companies** enriched by Apollo:
- LinkedIn URLs
- Twitter handles
- Logo URLs
- Industry classifications
- Enhanced descriptions

**21% from event page only**:
- Basic information
- No social media links
- Limited industry data

---

## Industry Insights

### Event Technology Ecosystem Represented:

1. **Registration & Onsite** (Choose 2 Rent, Eventpack, Fenix)
2. **Event Platforms** (ExpoPlatform, Cvent, Eventbase)
3. **Engagement** (Komo, Pigeonhole, Braindate)
4. **Accessibility** (TransPerfect, Interprefy)
5. **AV & Production** (4Wall, Novum Live, First Sight Media)
6. **Content & Programme** (Lineup Ninja, Memento, PreMagic)
7. **Sustainability** (One Tribe, enviricard, BeCause)
8. **AI & Innovation** (Erleah)
9. **Rentals & Infrastructure** (One World Rental, Silent Seminars)
10. **Media & Publishing** (Event Industry News)

### Technology Trends Visible:

1. **AI Integration** (Erleah, ExpoPlatform, Interprefy, PreMagic)
2. **Sustainability Focus** (One Tribe, enviricard, BeCause)
3. **Hybrid Events** (Cvent, Eventbase, First Sight Media)
4. **Accessibility** (Interprefy, TransPerfect Live)
5. **Networking Innovation** (Braindate, ExpoPlatform, PreMagic)
6. **Data & Analytics** (ExpoPlatform, Komo, Lineup Ninja)

---

## Data Completeness Assessment

### Excellent Coverage:
- ✅ Company names (100%)
- ✅ Company descriptions (96%)
- ✅ Product descriptions (100%)
- ✅ Product features (100%)
- ✅ Product categories (100%)
- ✅ Company roles (100%)

### Good Coverage:
- ⚠ Company websites (86%)
- ⚠ Company logos (86%)
- ⚠ LinkedIn URLs (79%)
- ⚠ Product pricing info (35% specific)

### Limited Coverage:
- ❌ Booth numbers (0%)
- ❌ Tier information (only sponsor has tier)
- ❌ Product URLs (9%)
- ❌ Industry classifications (61%)

### Missing Data (Would Need to Mock):
- ❌ Speaker names and bios
- ❌ Session schedules and tracks
- ❌ Attendee data
- ❌ Actual connections made
- ❌ Booth layout/floor plan
- ❌ Sponsor packages and benefits
- ❌ Ticket types and pricing
- ❌ Event agenda details

---

## Recommendations for Mock Data

### Use Directly from CSV:
1. ✅ Company names
2. ✅ Product names and descriptions
3. ✅ Product features
4. ✅ Company descriptions
5. ✅ Industry classifications
6. ✅ Company roles

### Infer from CSV:
1. 🔄 Session topics (from company specialties)
2. 🔄 Speaker names (from company representatives)
3. 🔄 Connection names (from company roles)
4. 🔄 Product categories (simplify from detailed categories)

### Create from Scratch:
1. ❌ Attendee personas
2. ❌ Individual attendee stats
3. ❌ Session schedule/timing
4. ❌ Specific achievements
5. ❌ Engagement metrics
6. ❌ Booth visit patterns

---

## File Locations

**Analysis Documents**:
- `/Users/carlos.cubas/Projects/personal-event-summary/analysis/event-tech-live-data-insights.md`
- `/Users/carlos.cubas/Projects/personal-event-summary/analysis/event-tech-live-quick-reference.md`
- `/Users/carlos.cubas/Projects/personal-event-summary/analysis/event-tech-live-csv-summary.md`

**Source CSV Files**:
- `/Users/carlos.cubas/Projects/personal-event-summary/examples/event_live_conf_data/event_tech_live_20251020_152709_summary.csv`
- `/Users/carlos.cubas/Projects/personal-event-summary/examples/event_live_conf_data/event_tech_live_20251020_152709_companies.csv`
- `/Users/carlos.cubas/Projects/personal-event-summary/examples/event_live_conf_data/event_tech_live_20251020_152709_products.csv`

---

## Summary Statistics

**Event**: Event Tech Live 2025 (Nov 12-13, London, UK)

**Scale**:
- 28 Companies
- 214 Products
- 1 Headline Sponsor
- 25 Partners
- 1 Speaker
- 1 Attendee (IMEX Group)

**Data Quality**: 8/10
- Excellent product and company coverage
- Rich descriptions and features
- Good social media links
- Missing: booth layout, detailed schedule, attendee data

**Usability for Mock Data**: 9/10
- Perfect for company names and products
- Excellent for CTAs and connections
- Great for session topic inference
- Requires persona/attendee creation

**Realism Factor**: 10/10
- Real B2B tech conference
- Authentic companies and products
- Actual event (upcoming)
- Representative of event tech industry

---

**Last Updated**: 2025-11-06
**Analysis Completed**: Comprehensive extraction complete
**Ready for**: Mock attendee data generation
