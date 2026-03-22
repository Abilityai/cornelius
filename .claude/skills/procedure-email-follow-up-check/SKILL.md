---
description: Review sent emails from past month to identify those needing follow-up responses
triggers:
  - check for follow ups
  - emails needing follow up
  - follow up check
  - what emails need follow up
  - review sent emails
automation: manual
metadata:
  version: "1.0"
  category: procedure
---

# Email Follow-Up Check Procedure

Review sent emails from the past 30 days to identify messages that may need follow-up.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Sent Emails | Gmail (via google-workspace) | Yes | | Last 30 days of sent messages |
| Inbox | Gmail (via google-workspace) | Yes | | Check for replies received |

## Workflow

### Step 1: Search Sent Emails

Use the google-workspace subagent to search sent emails:

```
Search query: "in:sent after:YYYY/MM/DD" (30 days ago)
```

### Step 2: Analyze for Follow-Up Indicators

Review each email for these patterns:

**High Priority:**
- Questions asked that likely haven't been answered
- Meeting requests awaiting confirmation (Calendly links sent)
- Investor/business discussions with open concerns
- Proposals or pitches awaiting response

**Medium Priority:**
- Podcast/interview invitations sent
- Introduction emails made
- Action items promised to others
- Scheduling discussions in progress

**Low Priority:**
- Mass updates (monitor for interested responses)
- Informational emails that may warrant check-in

### Step 3: Exclusions

Filter out these email types:
- Quarterly updates (unless flagged for specific follow-up)
- Newsletters and broadcast emails
- Auto-replies and confirmations
- Simple thank-you notes not requiring response
- Threads with recent replies (conversation is active)

### Step 4: Categorize and Present

Output format for each email needing follow-up:

```
**[Recipient Name]** (Date)
- Subject: [subject line]
- Reason: [why follow-up may be needed]
- Action: [suggested next step]
```

Group by priority: HIGH / MEDIUM / LOW

### Step 5: Offer Next Steps

After presenting the list, offer:
- Draft follow-up emails for specific items
- Check if meetings were actually scheduled
- Mark items as resolved if user confirms no action needed

## Completion Checklist

- [ ] Sent emails from last 30 days retrieved
- [ ] Emails categorized by priority (HIGH/MEDIUM/LOW)
- [ ] Exclusions applied (newsletters, auto-replies, active threads)
- [ ] Follow-up list presented to user
- [ ] Next steps offered (draft emails, check meetings, mark resolved)
