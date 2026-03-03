---
created: '2026-01-12'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreid4xqzffdrmamnqnzmeouqnbuqkcdtero2gr7bqdl42qrlefthlza
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
---
# to done   
## Description   
*[Written by Claude]*   
A todo app where AI doesn't just help you manage tasks - it actually executes them. "to done" turns your todo list into a done list by having AI agents complete tasks on your behalf.   
## What is it for   
Moving beyond task management to task execution. Instead of just reminding you to send an email, book a flight, or schedule a meeting - the AI does it for you.   
## Goals   
- Transform passive task tracking into active task completion   
- Reduce cognitive load by delegating executable tasks to AI   
- Maintain human oversight with approval workflows for important actions   
- Learn user preferences over time to improve execution quality   
   
## Example use cases   
- "Send a follow-up email to John about the proposal" → AI drafts and sends   
- "Book a dinner reservation for Friday at 7pm" → AI finds restaurant and books   
- "Schedule a meeting with the team next week" → AI coordinates calendars and sends invites   
- "Research competitors in the AI space" → AI compiles a report   
   
## Measure of success   
- Tasks completed per user per week   
- User trust/approval rate for AI-executed tasks   
- Time saved vs. manual execution   
- Retention and repeat usage   
   
## Potential blockers   
- API access to external services (email, calendar, booking platforms)   
- User trust in AI taking actions on their behalf   
- Handling failures and edge cases gracefully   
- Security and authentication for third-party services   
   
## MVP Scope   
1. Email sending integration (Gmail/Outlook)   
2. Calendar scheduling (Google Calendar)   
3. Simple approval workflow (confirm before executing)   
4. Basic task parsing and categorization   
   
## Technical approach   
- LLM for task understanding and execution planning   
- MCP/tool integrations for service access   
- Approval queue for human-in-the-loop review   
- Learning system to remember user preferences   
