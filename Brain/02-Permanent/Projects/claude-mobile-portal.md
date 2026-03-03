---
created: '2026-01-17'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreihmtvpihtnpnmoymc2zqfjlvnldl6ciydcou5quan7zhgsoqnizjy
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
status: In Progress
---
# Claude Mobile Portal   
# Claude Portal   
iOS app that connects to a Mac over Tailscale via SSH to run Claude CLI, with native UI enhancements.   
## Status   
Active development - Phase 1 (MVP) complete   
## Tech Stack   
- Swift 6.0 / SwiftUI   
- TCA (The Composable Architecture)   
- Citadel (SSH)   
- SwiftTerm (Terminal emulation)   
   
## Features Implemented   
- Multi-session terminal management   
- SSH connectivity with password/key auth   
- Claude command bar with quick actions   
- Extended keyboard row   
- Skills launcher   
- Host configuration UI   
- Settings with appearance preferences   
   
## Local Path   
`/Users/jlb/Documents/Projects/Personal/claude-portal`   
## Next Steps   
- Phase 2: Connection reliability, session persistence   
- Phase 3: Claude-specific integrations   
- Phase 4: iPad optimization, Tailscale device picker   
   
   
## Claude code mobile    
Here's a vision for Claude Code Mobile — reimagined for touch-first, on-the-go development:   
 --- 
The Core Concept: Conversation Cards   
Instead of a scrolling terminal, the interface is a stack of swipeable cards. Each card represents a discrete unit: a question, a file diff, a task, a terminal   
output.   
Swipe right → approve/apply   
Swipe left → reject/skip + start command input   
Swipe up → expand for details and give new context   
Swipe up and hold → see ongoing sessions   
Hold → fork into a new conversation thread → new agent/session with that ported context   
 --- 
Key Interface Elements   
1. The Orb   
   
A floating, ambient circle in the corner. Its color and motion reflect Claude's state:   
- Pulsing blue = thinking   
- Steady green = ready and needs your attention   
- Swirling orange = running tools   
- Tap to speak a command via voice   
1. Ghost Keyboard   
   
When you tap to type, the keyboard shows contextual autocomplete based on your codebase: function names, file paths, recent commands. Feels like coding, not texting.   
2. Pocket Repo   
Your project lives in a compressed local mirror. Claude can read and propose changes, but edits queue up as pending patches until you're back at your desk — or you can apply them directly if you're brave.   
   
Bonus features:   
1. Branch Timeline   
   
A horizontal timeline at the bottom shows your git history as dots. Drag to scrub through commits. Tap any dot to see what Claude did at that point. Time travel
for your project.   
 --- 
A Scenario   
You're on the train. A Slack message says the auth flow is broken.   
1. Open Claude Code Mobile   
2. Say: "What changed in auth this week?"   
3. Claude shows 3 commit cards — swipe through them   
4. Tap the suspicious one → see the diff in file review mode   
5. Say: "Revert this and add a null check for the token"   
6. Claude generates a patch card from context on screen at that moment — swipe right to queue it   
7. When you get home, your terminal shows: 3 patches pending from mobile session   
 --- 
   
The Philosophy   
Keep claude coding on mobile, in a new interface that doesn't have to be like a terminal anymore.   
