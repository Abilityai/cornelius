---
name: send-email
description: Send emails via Google Workspace with duplicate prevention. Use when composing or sending emails. Checks Sent folder before sending to prevent duplicates.
argument-hint: [recipient] [subject] [body]
automation: gated
---

# Send Email with Duplicate Prevention

Send emails safely through the google-workspace subagent with built-in duplicate detection.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Sent Folder | Gmail (via google-workspace) | Yes | | Check for recent duplicates |
| Outbox | Gmail (via google-workspace) | | Yes | Send new email |

## Workflow

**ALWAYS delegate to the google-workspace subagent** for email operations. The subagent has direct MCP tool access and handles duplicate detection.

### Step 1: Check for Duplicates

Before sending ANY email, search the Sent folder for recent emails to the same recipient:
- Query: Emails sent to RECIPIENT in the last 2 hours
- If similar email found: STOP and inform user, ask if they want to proceed anyway
- If no duplicates: Proceed to Step 2

### Step 2: Send the Email

Send the email using the google-workspace subagent's MCP tools:
- Recipient: The target email address
- Subject: The email subject line
- Body: Plain text content (NO markdown formatting)

### Step 3: Confirm

After successful send, confirm:
- Recipient
- Subject
- Summary of body (first line or key points)

## Email Formatting Rules

- Do NOT use markdown formatting (bold, italics, links) in email body
- Gmail does not render markdown - it displays as raw characters
- Use plain text only
- Apply Eugene's voice from the email-tone skill

## Arguments

- `$ARGUMENTS[0]`: Recipient email address
- `$ARGUMENTS[1]`: Subject line
- `$ARGUMENTS[2]`: Email body

If arguments are not provided, extract them from conversation context.

## Error Handling

- **Authentication error**: Direct user to `/google-reauth` skill
- **Rate limit**: Wait and inform user
- **Invalid recipient**: Report error clearly

## Completion Checklist

- [ ] Sent folder checked for duplicates (last 2 hours)
- [ ] Email formatted as plain text (no markdown)
- [ ] Eugene's voice applied (email-tone skill)
- [ ] Email sent successfully
- [ ] Confirmation provided to user
