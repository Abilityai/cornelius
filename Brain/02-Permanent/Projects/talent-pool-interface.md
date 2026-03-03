---
created: '2026-01-14'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreig5mt5vpk7tmuh5frxnnwvwvfvdmexdkfda4bqcaukglr5qysroii
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
status: To Do
---
# Talent pool interface   
## Description   
*[Written by Claude]*   
A client-facing web interface that allows clients to search and discover talent from Big Matter's professional networks, with data sourced from Airtable.   
## What is it for   
Enabling clients to self-serve when looking for talent, reducing manual matchmaking work and speeding up the talent discovery process.   
## Goals   
- Provide intuitive search and filtering across talent pools   
- Surface relevant candidates based on skills, experience, and availability   
- Reduce time-to-match for client requests   
- Maintain data sync with Airtable as source of truth   
   
## Measure of success   
- Client adoption rate and repeat usage   
- Time reduction in talent discovery (vs. manual process)   
- Quality of matches (client satisfaction with surfaced candidates)   
   
## Potential blockers   
- Airtable API rate limits for real-time sync   
- Data privacy/consent for displaying talent profiles   
- Search relevance tuning may require iteration   
   
## Alternative implementation paths   
- Static export from Airtable vs. live API integration   
- Embed within existing client portal vs. standalone app   
- Start with simple text search, evolve to semantic/AI-powered search   
