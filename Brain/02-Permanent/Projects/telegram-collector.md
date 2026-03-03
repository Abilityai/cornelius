---
created: '2026-02-10'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreicjh73anofay6exogmfjklw3ai7obyyaudbxtj37otyo37oklpoxe
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
local_path: /Users/jlb/Documents/Projects/BigMatter/telegram-collector
---
# Telegram Collector   
OSINT data collection pipeline for Telegram channels focused on the Russo-Ukrainian war. Monitors channels, downloads images, translates RU/UK military text, and analyzes images for military hardware identification using Claude Vision + EasyOCR.   
## Stack   
- Python 3.11+   
- Telethon (Telegram MTProto client)   
- aiosqlite (async SQLite)   
- boto3 (S3-compatible storage — Cloudflare R2)   
- DeepL API (translation)   
- Claude Vision API (image analysis)   
- EasyOCR (OCR for RU/UK/EN)   
   
## Status   
Phase 1-3 complete. Phase 4 (CLI polish, Docker) pending.   
## CLI Commands   
- `tg-collect collect` — real-time channel monitoring   
- `tg-collect backfill --channel @name` — historical message fetch   
- `tg-collect analyze --pending` — analyze unprocessed images   
- `tg-collect export --format csv` — export data   
