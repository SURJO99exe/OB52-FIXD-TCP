# GAME UPDATE MAINTENANCE GUIDE
# OB52-FIXD-TCP Bot
# What to change when Free Fire updates

================================================================================
                         🔧 GAME UPDATE CHECKLIST
================================================================================

When Free Fire updates (OB52 → OB53, etc.), check and update these files:

================================================================================
                    1️⃣ PACKET HEADERS (main.py)
================================================================================

Location: Lines 2523-2540 in bundle_packet_async, Emote_k, etc.

What to check:
- Region packet types may change
- Current: "0514" (IND), "0515" (Default), "0519" (BD)

Update needed if:
- Game server rejects packets
- "Invalid packet" errors in console
- Commands stop working after update

How to find new headers:
1. Capture packets from official game client
2. Look for first 4 bytes of encrypted packets
3. Update packet_type variables

================================================================================
                    2️⃣ BUNDLE IDS (main.py)
================================================================================

Location: Line 21-32 (BUNDLE dictionary)

Current Bundle IDs:
```python
BUNDLE = {
    "midnight": 914000002,
    "aurora": 914000002,
    "naruto": 914000002,
    ...
}
```

Update needed if:
- /bundle commands stop working
- Bundles show as "expired" or "invalid"

How to find new IDs:
1. Check game files (bundles.json or similar)
2. Capture from official client
3. Check community forums/Telegram groups

================================================================================
                    3️⃣ EMOTE IDS (main.py)
================================================================================

Location: Lines 37-162 (Multiple emote dictionaries)

Categories to update:
- DANCE_EMOTES (909000001-909000008)
- RARE_EMOTES (909052001-909052012)
- LEGEND_EMOTES (909053001-909053010)
- VIP_EMOTES (909054001-909054008)
- WEAPON_EMOTES (909000063-909046012)
- VICTORY_EMOTES (909000200-909000207)
- PET_EMOTES (909055001-909055008)
- VEHICLE_EMOTES (909056001-909056006)
- GRAFFITI_SPRAYS (909057001-909057006)

Update needed if:
- Emotes show as "expired"
- New emotes added to game
- Emote codes stop working

How to find new IDs:
1. Game asset files (emotes.json)
2. Packet capture
3. Community databases

================================================================================
                    4️⃣ PROTOBUF IDs (xC4.py)
================================================================================

Location: All protobuf creation functions

Check functions:
- CrEaTe_ProTo()
- GeneRaTePk()
- DeCode_PackEt()

Update needed if:
- Packets fail to decode
- "Invalid protobuf" errors
- Protocol version changes

How to update:
1. Reverse engineer new protobuf specs
2. Check field numbering changes
3. Update field mappings

================================================================================
                    5️⃣ API ENDPOINTS (APIS.py / xHeaders.py)
================================================================================

Location: xHeaders.py - login and API functions

Check:
- Login URLs
- API base URLs
- Authentication endpoints

Update needed if:
- Login fails
- "Connection refused" errors
- API returns 404/503

Common changes:
- api.garena.com → api2.garena.com
- New authentication tokens
- Updated headers

================================================================================
                    6️⃣ REGION/ SERVER CODES
================================================================================

Location: Throughout main.py and xC4.py

Check:
- Region codes: "ind", "bd", "br", "sg", "tw"
- Server IPs and ports
- Connection strings

Update needed if:
- "Cannot connect to server"
- Region-specific commands fail
- New regions added

================================================================================
                    7️⃣ CHARACTER SKILLS (main.py)
================================================================================

Location: Lines 178-256 (Strategy info)

Check:
- New characters added
- Skill changes
- Character reworks

Update needed if:
- /char command shows wrong info
- New characters in game

================================================================================
                    8️⃣ WEAPON STATS (main.py)
================================================================================

Location: Lines 196-223 (WEAPON_STATS dictionary)

Check:
- New weapons added
- Weapon balance changes
- Stats modifications

Update needed if:
- /weaponstats shows outdated info
- New weapons not recognized

================================================================================
                    9️⃣ DROP LOCATIONS (main.py)
================================================================================

Location: Lines 215-224 (DROP_LOCATIONS)

Check:
- New maps added
- Location name changes
- Map rotations

Update needed if:
- /drop command shows wrong info
- New maps in game

================================================================================
                    🔟 SECURITY TOKENS
================================================================================

Location: token.txt, main.py (BYPASS_TOKEN)

Check:
- New authentication method
- Token format changes
- Security updates

Update needed if:
- "Invalid token" errors
- Cannot login
- Account banned quickly

================================================================================
                         📋 UPDATE WORKFLOW
================================================================================

Step 1: IDENTIFY
- Note which commands stopped working
- Check console for error messages
- Identify specific error patterns

Step 2: RESEARCH
- Check community forums
- Look for updated packet captures
- Join Telegram/WhatsApp groups for updates

Step 3: TEST
- Make one change at a time
- Test immediately after each change
- Document what works

Step 4: UPDATE
- Apply fixes to all affected areas
- Test all commands
- Verify functionality

Step 5: DOCUMENT
- Update this file with new IDs/values
- Note what changed in the update
- Share with community

================================================================================
                    🛠️ QUICK FIX LOCATIONS
================================================================================

File: main.py
- Line 21-32: BUNDLE IDs
- Line 37-162: EMOTE IDs
- Line 178-256: Character info
- Line 196-223: Weapon stats
- Line 215-224: Drop locations
- Line 2523-2540: Packet headers

File: xC4.py
- All protobuf functions
- Encryption/decryption
- Packet generation

File: xHeaders.py
- API endpoints
- Login functions
- Authentication

File: token.txt
- Login credentials
- Security tokens

================================================================================
                    ⚠️ COMMON UPDATE ISSUES
================================================================================

Issue: All commands stopped working
→ Check: Packet headers, protobuf IDs

Issue: Login fails
→ Check: token.txt, xHeaders.py API endpoints

Issue: Emotes not working
→ Check: Emote IDs in main.py

Issue: Bundle not sending
→ Check: Bundle IDs, packet headers

Issue: Cannot connect
→ Check: Server IPs, region codes

================================================================================
                    📞 WHERE TO FIND UPDATES
================================================================================

Community Sources:
- Telegram: t.me/+NNjmL2bYZIk2ZTJl
- WhatsApp: chat.whatsapp.com/DcDHGuTCGFQAXUnOR84Ah0
- GitHub: Check issues and pull requests

Official Sources:
- Free Fire patch notes
- Garena developer docs (if available)

Tools:
- Packet capture software
- Hex editors
- Protobuf decoders

================================================================================
                         ✅ POST-UPDATE CHECKLIST
================================================================================

After updating, test these commands:
□ /bundle [uid] [name]
□ /bundleall [name]
□ /evo [1-18]
□ /dance [1-8]
□ /weapon ak
□ /char dj
□ /kick [uid]
□ /start
□ /help

If all work → Update successful!
If any fail → Check corresponding section above

================================================================================
                    📝 VERSION TRACKING
================================================================================

Current Version: OB52
Last Updated: March 9, 2026
Next Expected Update: OB53 (TBA)

Update this file after each game update!

================================================================================
                              END OF GUIDE
================================================================================
