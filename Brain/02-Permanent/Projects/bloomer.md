---
created: '2026-01-10'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreiba6bwkvpvbd2fzg62x2h7z7iaezjqgt4ww7mebhud6wdekdlgxgu
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
local_path: /Users/jlb/Documents/Projects/BigMatter/Bloomer
status: In Progress
---
# Bloomer   
   
# Hackathon Platform   
A multi-event hackathon management platform with REST API. Supports user authentication, event management, team formation, challenges, and submissions.   
## Features   
- **Multi-event support** - Run multiple hackathons with data isolation   
- **Role-based access** - Global admin, event owner, organizer, participant roles   
- **Team management** - Create/join teams, invites, team locking   
- **Challenges & submissions** - Sponsor challenges with prizes, team submissions   
- **Event-driven architecture** - Audit logging, webhook dispatch   
- **Session-based auth** - Password login + magic link (passwordless)   
   
   
     
     
   
## Quick Start   
```
# Install dependencies
pnpm install

# Set up environment
cp .env.example .env
# Edit .env with your values

# Start database (if using Docker)
docker run -d --name hackathon-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=hackathon \
  -p 5432:5432 \
  postgres:16

# Push schema to database
pnpm db:push

# Start development server
pnpm dev

```
## API Documentation   
Full OpenAPI specification available at `openapi.yaml`.   
### Authentication   
| Method |           Endpoint |                Description |
|:-------|:-------------------|:---------------------------|
|   POST |   `/auth/register` |             Create account |
|   POST |      `/auth/login` |        Login with password |
|   POST | `/auth/magic-link` | Request passwordless login |
|    GET |     `/auth/verify` |    Verify magic link token |
|    GET |         `/auth/me` |           Get current user |
|   POST |     `/auth/logout` |                End session |

### Events   
| Method |             Endpoint |          Description |
|:-------|:---------------------|:---------------------|
|    GET |            `/events` |   List public events |
|   POST |            `/events` | Create event (admin) |
|    GET |        `/events/:id` |    Get event details |
|  PATCH |        `/events/:id` |         Update event |
| DELETE |        `/events/:id` |   Delete draft event |
|   POST | `/events/:id/status` |  Change event status |

### Event-Scoped Routes (/events/:eventId/...)   
**Registrations**   
- `POST /registrations` - Register for event   
- `GET /registrations/me` - Current user's registration   
- `PATCH /registrations/:id/checkin` - Check in user   
   
**Teams**   
- `GET /teams` - List teams   
- `POST /teams` - Create team   
- `POST /teams/:id/join` - Join team   
- `POST /teams/:id/leave` - Leave team   
- `POST /teams/:id/invite` - Create invite   
- `POST /teams/:id/lock` - Lock for submission   
- `POST /invites/:code/accept` - Accept invite   
   
**Challenges**   
- `GET /challenges` - List challenges   
- `POST /challenges` - Create challenge (organizer)   
- `PATCH /challenges/:id` - Update challenge   
- `DELETE /challenges/:id` - Delete challenge   
   
**Submissions**   
- `GET /submissions` - List submissions   
- `POST /submissions` - Create submission   
- `PATCH /submissions/:id` - Update draft   
- `POST /submissions/:id/finalize` - Submit   
   
**Webhooks**   
- `GET /webhooks` - List webhooks   
- `POST /webhooks` - Register webhook   
- `DELETE /webhooks/:id` - Remove webhook   
   
### Admin Routes (/admin/...)   
- `GET /registrations` - All registrations   
- `GET /teams` - All teams   
- `GET /submissions` - All submissions   
- `POST /announcements` - Send announcement   
- `GET /export/:entity` - CSV export   
   
## Project Structure   
```
src/
├── db/
│   ├── schema.ts          # Drizzle schema (PostgreSQL)
│   └── index.ts           # Database connection
├── lib/
│   ├── env.ts             # Environment validation
│   ├── errors.ts          # Error handling
│   ├── schemas.ts         # Zod validation schemas
│   ├── password.ts        # Password hashing
│   └── anonymize.ts       # Public view transformers
├── middleware/
│   ├── auth.ts            # Session middleware
│   ├── event-context.ts   # Event loading + role detection
│   └── authorization.ts   # Permission checking
├── routes/
│   ├── auth.ts
│   ├── users.ts
│   ├── admin.ts
│   ├── events/
│   │   ├── index.ts       # Event CRUD
│   │   ├── organizers.ts
│   │   ├── registrations.ts
│   │   ├── teams.ts
│   │   ├── challenges.ts
│   │   ├── submissions.ts
│   │   └── webhooks.ts
│   └── webhooks/
│       └── stripe.ts      # Payment webhooks
├── services/
│   └── events.ts          # Domain event bus
└── index.ts               # Entry point

```
## Development   
```
# Run tests
pnpm test

# Type check
pnpm typecheck

# Generate migrations
pnpm db:generate

# Open Drizzle Studio
pnpm db:studio

```
## Authorization Model   
|            Role |        Scope |                        Permissions |
|:----------------|:-------------|:-----------------------------------|
|    Global Admin |   All events |                        Full access |
|     Event Owner | Single event | Manage event, organizers, webhooks |
| Event Organizer | Single event |   Manage registrations, challenges |
|     Participant | Single event |          Create/join teams, submit |
|          Public |              |              View events, register |

## Event System   
All state changes emit domain events:   
```
user.created, user.updated
event.created, event.updated, event.status_changed
registration.created, registration.paid, registration.checked_in
team.created, team.member_joined, team.member_left, team.locked
challenge.created, challenge.updated, challenge.deleted
submission.created, submission.updated, submission.finalized
announcement.sent

```
Events are:   
1. Logged to `event\_logs` table (audit trail)   
2. Dispatched to registered webhooks   
3. Available for internal handlers   
   
## Tech Stack   
- **Runtime**: Node.js 20+   
- **Framework**: Hono   
- **Database**: PostgreSQL + Drizzle ORM   
- **Validation**: Zod   
- **Testing**: Vitest   
