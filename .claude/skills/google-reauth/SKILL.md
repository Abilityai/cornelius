---
name: google-reauth
description: Handle Google OAuth token expiration and re-authentication. Use when Google Workspace operations fail with authentication errors, expired tokens, 401 Unauthorized, or authorization URL is returned. Provides streamlined re-authentication workflow.
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Google Workspace Re-Authentication

When Google OAuth tokens expire, use this streamlined re-authentication process.

## When to Trigger

This skill auto-activates when:
- Google authentication error received
- Authorization URL returned in error message
- 401 Unauthorized from Google APIs
- Token expired errors
- "Please visit this URL to authorize" messages

## Re-Authentication Workflow

### Step 1: Detect the Authorization URL
Look for the authorization URL in the error message. It typically starts with:
`https://accounts.google.com/o/oauth2/auth?...`

### Step 2: Update the HTML Template
Update the authorization URL in the HTML template:

```bash
# Update the href in the template
sed -i '' 's|href="https://accounts.google.com/o/oauth2/auth[^"]*"|href="NEW_AUTHORIZATION_URL"|' .claude/skills/google-reauth/templates/google_auth.html
```

### Step 3: Open in Browser
```bash
open .claude/skills/google-reauth/templates/google_auth.html
```

### Step 4: User Completes Authorization
- User is auto-redirected after 2 seconds (or clicks button)
- Signs in with Google account (cornelius@beingluminous.com)
- Accepts permissions
- Redirects to localhost:8890 (MCP server)

### Step 5: Retry Original Command
After authorization completes, retry the original Google Workspace command.

## Quick Commands

**Update auth URL and open:**
```bash
cd /Users/eugene/Dropbox/Agents/cornelius_luminous
sed -i '' 's|href="https://accounts.google.com/o/oauth2/auth[^"]*"|href="NEW_URL_HERE"|' .claude/skills/google-reauth/templates/google_auth.html && open .claude/skills/google-reauth/templates/google_auth.html
```

## Template Features

- Clean, user-friendly interface
- Auto-redirect after 2 seconds
- Professional styling
- Clear instructions for user
- Works with localhost:8890 MCP server redirect

## Scopes Included

The authorization includes all Google Workspace scopes:
- Gmail (read, compose, send, modify, labels)
- Calendar (events, readonly)
- Drive (files, readonly)
- Docs, Sheets, Slides
- Tasks
- Forms
- Chat

## Troubleshooting

**Auth loop / keeps asking:**
- Clear browser cookies for accounts.google.com
- Ensure MCP server is running on localhost:8890

**Token not refreshing:**
- Delete token cache and re-authenticate
- Check MCP server logs for errors

**Wrong account:**
- Sign out of Google in browser first
- Clear cookies and try again
