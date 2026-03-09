import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, random
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from APIS import insta
from flask import Flask, jsonify, request
import asyncio
import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# Enhanced Configuration Variables
ADMIN_UID = "8804135237"
server2 = "BD"
key2 = "mg24"
BYPASS_TOKEN = "your_bypass_token_here"


# Auto-accept invitation settings
auto_accept_invite = True  # Auto-accept squad invitations
auto_accept_delay = 1.0  # seconds to wait before accepting

# Animation settings
rainbow_running = False
rainbow_task = None
flash_running = False
flash_task = None

# New emote collections
DANCE_EMOTES = {
    "1": "909000001",   # Dance 1
    "2": "909000002",   # Dance 2
    "3": "909000003",   # Dance 3
    "4": "909000004",   # Dance 4
    "5": "909000005",   # Dance 5
    "6": "909000006",   # Dance 6
}

RAINBOW_COLORS = ["FF0000", "FF7F00", "FFFF00", "00FF00", "0000FF", "4B0082", "9400D3"]

# RARE EMOTES COLLECTION
RARE_EMOTES = {
    "1": "909052001",   # Rare AK
    "2": "909052002",   # Rare SCAR
    "3": "909052003",   # Rare MP40
    "4": "909052004",   # Rare M1014
    "5": "909052005",   # Rare XM8
    "6": "909052006",   # Rare UMP
    "7": "909052007",   # Rare M1887
    "8": "909052008",   # Rare Groza
    "9": "909052009",   # Rare M4A1
    "10": "909052010",  # Rare Thompson
    "11": "909052011",  # Rare P90
    "12": "909052012",  # Rare Woodpecker
}

# LEGENDARY EMOTES COLLECTION
LEGEND_EMOTES = {
    "1": "909053001",   # Legend AK
    "2": "909053002",   # Legend SCAR
    "3": "909053003",   # Legend MP40
    "4": "909053004",   # Legend M1887
    "5": "909053005",   # Legend Groza
    "6": "909053006",   # Legend M4A1
    "7": "909053007",   # Legend P90
    "8": "909053008",   # Legend AWM
    "9": "909053009",   # Legend Desert Eagle
    "10": "909053010",  # Legend AN94
}

# EXCLUSIVE/VIP EMOTES
VIP_EMOTES = {
    "1": "909054001",   # VIP Exclusive 1
    "2": "909054002",   # VIP Exclusive 2
    "3": "909054003",   # VIP Exclusive 3
    "4": "909054004",   # VIP Exclusive 4
    "5": "909054005",   # VIP Exclusive 5
    "6": "909054006",   # VIP Exclusive 6
    "7": "909054007",   # VIP Exclusive 7
    "8": "909054008",   # VIP Exclusive 8
}

# WEAPON SHOWCASE EMOTES
WEAPON_EMOTES = {
    "ak": "909000063",
    "scar": "909000068",
    "mp40": "909000075",
    "mp40_2": "909040010",
    "m1014": "909000081",
    "m1014_2": "909039011",
    "xm8": "909000085",
    "famas": "909000090",
    "ump": "909000098",
    "m1887": "909035007",
    "woodpecker": "909042008",
    "groza": "909041005",
    "m4a1": "909033001",
    "thompson": "909038010",
    "g18": "909038012",
    "parafal": "909045001",
    "p90": "909049010",
    "m60": "909051003",
    "awm": "909036008",
    "desert_eagle": "909037012",
    "an94": "909048008",
    "mp5": "909039004",
    "vector": "909040008",
    "sks": "909044012",
    "m14": "909045012",
    "sniper": "909046012",
}

# VICTORY/DANCE EMOTES
VICTORY_EMOTES = {
    "1": "909000200",   # Victory Dance 1
    "2": "909000201",   # Victory Dance 2
    "3": "909000202",   # Victory Dance 3
    "4": "909000203",   # Victory Dance 4
    "5": "909000204",   # Victory Dance 5
    "6": "909000205",   # Victory Dance 6
    "7": "909000206",   # Victory Dance 7
    "8": "909000207",   # Victory Dance 8
}

# PET SHOWCASE EMOTES
PET_EMOTES = {
    "1": "909055001",   # Pet 1 - Kitty
    "2": "909055002",   # Pet 2 - Puppy
    "3": "909055003",   # Pet 3 - Panda
    "4": "909055004",   # Pet 4 - Robot
    "5": "909055005",   # Pet 5 - Dragon
    "6": "909055006",   # Pet 6 - Eagle
    "7": "909055007",   # Pet 7 - Tiger
    "8": "909055008",   # Pet 8 - Fox
}

# VEHICLE EMOTES
VEHICLE_EMOTES = {
    "1": "909056001",   # SUV
    "2": "909056002",   # Sports Car
    "3": "909056003",   # Monster Truck
    "4": "909056004",   # Motorcycle
    "5": "909056005",   # Jeep
    "6": "909056006",   # Tuk-Tuk
}

# GRAFFITI/SPRAY COLLECTION
GRAFFITI_SPRAYS = {
    "1": "909057001",   # Crown
    "2": "909057002",   # Skull
    "3": "909057003",   # Fire
    "4": "909057004",   # Heart
    "5": "909057005",   # GG
    "6": "909057006",   # Boss
}

# QUICK GAME CALLOUTS
GAME_CALLOUTS = {
    "enemy": "[B][C][FF0000]⚠️ ENEMY SPOTTED! ⚠️",
    "backup": "[B][C][0000FF]🆘 NEED BACKUP! 🆘",
    "help": "[B][C][00FF00]📢 NEED HELP! 📢",
    "rush": "[B][C][FF8C00]⚡ RUSH! RUSH! RUSH! ⚡",
    "camp": "[B][C][9400D3]🎯 CAMP HERE! 🎯",
    "loot": "[B][C][FFD700]💰 LOOT HERE! 💰",
    "medic": "[B][C][FF69B4]🏥 NEED MEDIC! 🏥",
    "ammo": "[B][C][1E90FF]🔫 NEED AMMO! 🔫",
    "thanks": "[B][C][32CD32]🙏 THANKS! 🙏",
    "gg": "[B][C][FFD700]🏆 GG! WELL PLAYED! 🏆",
}

# TEAM LOADOUTS
LOADOUTS = {
    "sniper": "[B][C][00FFFF]🎯 SNIPER LOADOUT\n[FFFFFF]AWM + MP40 + Level 3 Vest",
    "rusher": "[B][C][FF4500]⚡ RUSHER LOADOUT\n[FFFFFF]MP40 + M1887 + Level 3 Helmet",
    "support": "[B][C][32CD32]🛡️ SUPPORT LOADOUT\n[FFFFFF]M4A1 + Thompson + Med Kits",
    "assault": "[B][C][FF0000]🔫 ASSAULT LOADOUT\n[FFFFFF]AK + SCAR + Grenades",
}

# TOURNAMENT/SCRIM SYSTEM
TOURNAMENT_MODES = {
    "1v1": "1v1 Duel",
    "2v2": "2v2 Team",
    "4v4": "4v4 Squad",
    "solo": "Solo Battle",
    "duo": "Duo Battle",
    "squad": "Full Squad",
}

# RANK PUSH TIPS
RANK_TIPS = {
    "bronze": "[B][C][CD7F32]🥉 BRONZE TIPS\n[FFFFFF]• Land in safe zones\n• Collect basic loot\n• Avoid early fights",
    "silver": "[B][C][C0C0C0]🥈 SILVER TIPS\n[FFFFFF]• Practice close combat\n• Use cover wisely\n• Stay in zone",
    "gold": "[B][C][FFD700]🥇 GOLD TIPS\n[FFFFFF]• Improve aim training\n• Use grenades\n• Team coordination",
    "platinum": "[B][C][00FF00]💎 PLATINUM TIPS\n[FFFFFF]• Rush with strategy\n• Headshot practice\n• Quick looting",
    "diamond": "[B][C][00BFFF]💠 DIAMOND TIPS\n[FFFFFF]• Advanced movement\n• Squad leadership\n• Map awareness",
    "heroic": "[B][C][FF0000]🔥 HEROIC TIPS\n[FFFFFF]• Pro level tactics\n• Character skills\n• Tournament prep",
    "grandmaster": "[B][C][9400D3]👑 GRANDMASTER TIPS\n[FFFFFF]• Elite strategies\n• Perfect aim\n• Champion mindset",
}

# GAME MODES
GAME_MODES = {
    "br": "[B][C][FF0000]🔥 BATTLE ROYALE\n[FFFFFF]Classic BR mode - Be the last one standing!",
    "cs": "[B][C][0000FF]⚔️ CLASH SQUAD\n[FFFFFF]4v4 Team battle - First to 5 rounds wins!",
    "lone": "[B][C][9400D3]🐺 LONE WOLF\n[FFFFFF]Solo vs Squad - Test your skills!",
    "rush": "[B][C][FF8C00]⚡ RUSH HOUR\n[FFFFFF]Fast paced action - Quick matches!",
    "gun": "[B][C][FFD700]🔫 GUN KING\n[FFFFFF]Weapon progression mode!",
}

# DROP LOCATIONS
DROP_LOCATIONS = {
    "peaks": "[B][C][FF0000]🏔️ BERMUDA - PEAKS\n[FFFFFF]High loot | High risk | Great for snipers",
    "mill": "[B][C][FF8C00]🏭 BERMUDA - MILL\n[FFFFFF]Medium loot | Medium risk | Good loot spread",
    "dock": "[B][C][1E90FF]⚓ BERMUDA - DOCK\n[FFFFFF]High loot | Medium risk | Close combat",
    "clock": "[B][C][9400D3]🕐 KALAHARI - CLOCK TOWER\n[FFFFFF]High loot | High risk | Central location",
    "refinery": "[B][C][FF4500]🏭 KALAHARI - REFINERY\n[FFFFFF]Medium loot | Good cover | Squad fights",
    "alpine": "[B][C][00FF00]🏔️ ALPINE - MAIN TOWN\n[FFFFFF]High loot | Multiple buildings | Strategy",
}

# CHARACTER SKILLS INFO
CHARACTER_SKILLS = {
    "dj": "[B][C][FF8C00]🎧 DJ ALOK\n[FFFFFF]Skill: Drop the Beat\n[FFFFFF]Creates a 5m aura that increases ally movement speed",
    "chrono": "[B][C][1E90FF]🛡️ CHRONO\n[FFFFFF]Skill: Time Turner\n[FFFFFF]Creates a force field that blocks damage",
    "k": "[B][C][FF0000]🔥 K\n[FFFFFF]Skill: Master of All\n[FFFFFF]Increases max EP and EP conversion",
    "joseph": "[B][C][9400D3]⚡ JOSEPH\n[FFFFFF]Skill: Nutty Movement\n[FFFFFF]Increases movement speed after taking damage",
    "moco": "[B][C][00FF00]🔍 MOCO\n[FFFFFF]Skill: Hacker's Eye\n[FFFFFF]Tags enemies that you damage",
    "clu": "[B][C][FF69B4]🎯 CLU\n[FFFFFF]Skill: Detect enemies\n[FFFFFF]Reveals enemy positions",
    "wolfrahh": "[B][C][FFD700]🐺 WOLFRAHH\n[FFFFFF]Skill: Limelight\n[FFFFFF]Reduces headshot damage",
    "dasha": "[B][C][FF4500]💃 DASHA\n[FFFFFF]Skill: Partying On\n[FFFFFF]Reduces fall damage and recovery time",
}

# WEAPON STATS
WEAPON_STATS = {
    "ak": "[B][C][FF0000]🔫 AK47\n[FFFFFF]Damage: HIGH | Range: MEDIUM\n[FFFFFF]Best for: Close-Mid range fights",
    "mp40": "[B][C][FF8C00]🔫 MP40\n[FFFFFF]Damage: MEDIUM | Fire Rate: VERY HIGH\n[FFFFFF]Best for: Close range rush",
    "awm": "[B][C][1E90FF]🎯 AWM\n[FFFFFF]Damage: EXTREME | Range: LONG\n[FFFFFF]Best for: Long range sniping",
    "m1887": "[B][C][9400D3]🔫 M1887\n[FFFFFF]Damage: VERY HIGH | Fire Rate: SLOW\n[FFFFFF]Best for: One-shot kills close range",
    "scar": "[B][C][00FF00]🔫 SCAR\n[FFFFFF]Damage: MEDIUM | Stability: HIGH\n[FFFFFF]Best for: Beginners, stable fire",
    "m4a1": "[B][C][32CD32]🔫 M4A1\n[FFFFFF]Damage: MEDIUM | Range: GOOD\n[FFFFFF]Best for: All-round performance",
    "groza": "[B][C][FF0000]🔫 GROZA\n[FFFFFF]Damage: HIGH | Fire Rate: HIGH\n[FFFFFF]Best for: Aggressive gameplay",
    "ump": "[B][C][FFD700]🔫 UMP\n[FFFFFF]Damage: MEDIUM | Stability: GOOD\n[FFFFFF]Best for: Mid-range fights",
}

# QUICK STRATEGIES
STRATEGIES = {
    "rush": "[B][C][FF0000]⚡ RUSH STRATEGY\n[FFFFFF]• Land hot zone\n[FFFFFF]• Get SMG/Shotgun\n[FFFFFF]• Push immediately\n[FFFFFF]• Keep pressure on",
    "camp": "[B][C][9400D3]🎯 CAMP STRATEGY\n[FFFFFF]• Land edge of zone\n[FFFFFF]• Get Sniper/AR\n[FFFFFF]• Hold high ground\n[FFFFFF]• Move with zone",
    "balance": "[B][C][00FF00]⚖️ BALANCED STRATEGY\n[FFFFFF]• Land medium zone\n[FFFFFF]• Get AR/SMG combo\n[FFFFFF]• Play edge fights\n[FFFFFF]• Rotate smart",
    "sniper": "[B][C][1E90FF]🎯 SNIPER STRATEGY\n[FFFFFF]• Land high ground\n[FFFFFF]• Get AWM/Marksman\n[FFFFFF]• Support team\n[FFFFFF]• Headshot focus",
}

# EMOTE CATEGORIES HELP
EMOTE_CATEGORIES = """
[B][C][00FF00]🎭 EMOTE CATEGORIES 🎭
[FFFFFF]
[00FFFF]/evo [1-18] [FFFFFF]- Standard Evo emotes
[00FFFF]/emote [1-363] [FFFFFF]- All emotes list
[00FFFF]/dance [1-8] [FFFFFF]- Dance emotes
[00FFFF]/rare [1-12] [FFFFFF]- Rare collection emotes
[00FFFF]/legend [1-10] [FFFFFF]- Legendary emotes
[00FFFF]/vip [1-8] [FFFFFF]- VIP exclusive emotes
[00FFFF]/weapon [name] [FFFFFF]- Weapon showcase emotes
[00FFFF]/victory [1-8] [FFFFFF]- Victory celebration emotes
[00FFFF]/pet [1-8] [FFFFFF]- Pet showcase emotes
[00FFFF]/vehicle [1-6] [FFFFFF]- Vehicle emotes
[00FFFF]/graffiti [1-6] [FFFFFF]- Spray graffiti emotes
[00FFFF]/callout [type] [FFFFFF]- Quick game callouts
[00FFFF]/loadout [type] [FFFFFF]- Team loadout suggestions
[00FFFF]/rank [tier] [FFFFFF]- Rank push tips
[00FFFF]/mode [type] [FFFFFF]- Game mode info
[00FFFF]/drop [location] [FFFFFF]- Drop location guide
[00FFFF]/scrim [mode] [FFFFFF]- Tournament/scrim setup
[00FFFF]/char [name] [FFFFFF]- Character skills info
[00FFFF]/weaponstats [name] [FFFFFF]- Weapon stats guide
[00FFFF]/strategy [type] [FFFFFF]- Game strategies
[00FFFF]/super [id] [count] [FFFFFF]- Spam any emote
[00FFFF]/rainbow [FFFFFF]- Rainbow animation
[00FFFF]/flash [FFFFFF]- Flash animation
"""

# VariabLes dyli 
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
reject_spam_running = False
insquad = None 
joining_team = False 
reject_spam_task = None
lag_running = False
lag_task = None
evo_cycle_running = False
evo_cycle_task = None
auto_start_running = False
auto_start_teamcode = None
stop_auto = False
auto_start_task = None
auto_join_enabled = True  # Auto-join teams when invited
start_spam_duration = 18  # seconds to spam start
wait_after_match = 20  # seconds to wait after match
start_spam_delay = 0.2  # delay between start packets
evo_emotes = {
    "1": "909000063",   # AK
    "2": "909000068",   # SCAR
    "3": "909000075",   # 1st MP40
    "4": "909040010",   # 2nd MP40
    "5": "909000081",   # 1st M1014
    "6": "909039011",   # 2nd M1014
    "7": "909000085",   # XM8
    "8": "909000090",   # Famas
    "9": "909000098",   # UMP
    "10": "909035007",  # M1887
    "11": "909042008",  # Woodpecker
    "12": "909041005",  # Groza
    "13": "909033001",  # M4A1
    "14": "909038010",  # Thompson
    "15": "909038012",  # G18
    "16": "909045001",  # Parafal
    "17": "909049010",  # P90
    "18": "909051003"   # m60
}
#------------------------------------------#

# Emote mapping for evo commands
EMOTE_MAP = {
    1: 909000063,
    2: 909000081,
    3: 909000075,
    4: 909000085,
    5: 909000134,
    6: 909000098,
    7: 909035007,
    8: 909051012,
    9: 909000141,
    10: 909034008,
    11: 909051015,
    12: 909041002,
    13: 909039004,
    14: 909042008,
    15: 909051014,
    16: 909039012,
    17: 909040010,
    18: 909035010,
    19: 909041005,
    20: 909051003,
    21: 909034001
}

# RARE LOOK CHANGER BUNDLE ID
BUNDLE = {
    "rampage": 914000002,
    "cannibal": 914000003,
    "devil": 914038001,
    "scorpio": 914039001,
    "frostfire": 914042001,
    "paradox": 914044001,
    "naruto": 914047001,
    "aurora": 914047002,
    "midnight": 914048001,
    "itachi": 914050001,
    "dreamspace": 914051001
}
# Emote mapping for all emote commands
ALL_EMOTE = {
    1: 909000001,
    2: 909000002,
    3: 909000003,
    4: 909000004,
    5: 909000005,
    6: 909000006,
    7: 909000007,
    8: 909000008,
    9: 909000009,
    10: 909000010,
    11: 909000011,
    12: 909000012,
    13: 909000013,
    14: 909000014,
    15: 909000015,
    16: 909000016,
    17: 909000017,
    18: 909000018,
    19: 909000019,
    20: 909000020,
    21: 909000021,
    22: 909000022,
    23: 909000023,
    24: 909000024,
    25: 909000025,
    26: 909000026,
    27: 909000027,
    28: 909000028,
    29: 909000029,
    30: 909000031,
    31: 909000032,
    32: 909000033,
    33: 909000034,
    34: 909000035,
    35: 909000036,
    36: 909000037,
    37: 909000038,
    38: 909000039,
    39: 909000040,
    40: 909000041,
    41: 909000042,
    42: 909000043,
    43: 909000044,
    44: 909000045,
    45: 909000046,
    46: 909000047,
    47: 909000048,
    48: 909000049,
    49: 909000051,
    50: 909000052,
    51: 909000053,
    52: 909000054,
    53: 909000055,
    54: 909000056,
    55: 909000057,
    56: 909000058,
    57: 909000059,
    58: 909000060,
    59: 909000061,
    60: 909000062,
    61: 909000063,
    62: 909000064,
    63: 909000065,
    64: 909000066,
    65: 909000067,
    66: 909000068,
    67: 909000069,
    68: 909000070,
    69: 909000071,
    70: 909000072,
    71: 909000073,
    72: 909000074,
    73: 909000075,
    74: 909000076,
    75: 909000077,
    76: 909000078,
    77: 909000079,
    78: 909000080,
    79: 909000081,
    80: 909000082,
    81: 909000083,
    82: 909000084,
    83: 909000085,
    84: 909000086,
    85: 909000087,
    86: 909000088,
    87: 909000089,
    88: 909000090,
    89: 909000091,
    90: 909000092,
    91: 909000093,
    92: 909000094,
    93: 909000095,
    94: 909000096,
    95: 909000097,
    96: 909000098,
    97: 909000099,
    98: 909000100,
    99: 909000101,
    100: 909000102,
    101: 909000103,
    102: 909000104,
    103: 909000105,
    104: 909000106,
    105: 909000107,
    106: 909000108,
    107: 909000109,
    108: 909000110,
    109: 909000111,
    110: 909000112,
    111: 909000113,
    112: 909000114,
    113: 909000115,
    114: 909000116,
    115: 909000117,
    116: 909000118,
    117: 909000119,
    118: 909000120,
    119: 909000121,
    120: 909000122,
    121: 909000123,
    122: 909000124,
    123: 909000125,
    124: 909000126,
    125: 909000127,
    126: 909000128,
    127: 909000129,
    128: 909000130,
    129: 909000131,
    130: 909000132,
    131: 909000133,
    132: 909000134,
    133: 909000135,
    134: 909000136,
    135: 909000137,
    136: 909000138,
    137: 909000139,
    138: 909000140,
    139: 909000141,
    140: 909000142,
    141: 909000143,
    142: 909000144,
    143: 909000145,
    144: 909000150,
    145: 909033001,
    146: 909033002,
    147: 909033003,
    148: 909033004,
    149: 909033005,
    150: 909033006,
    151: 909033007,
    152: 909033008,
    153: 909033009,
    154: 909033010,
    155: 909034001,
    156: 909034002,
    157: 909034003,
    158: 909034004,
    159: 909034005,
    160: 909034006,
    161: 909034007,
    162: 909034008,
    163: 909034009,
    164: 909034010,
    165: 909034011,
    166: 909034012,
    167: 909034013,
    168: 909034014,
    169: 909035001,
    170: 909035002,
    171: 909035003,
    172: 909035004,
    173: 909035005,
    174: 909035006,
    175: 909035007,
    176: 909035008,
    177: 909035009,
    178: 909035010,
    179: 909035011,
    180: 909035012,
    181: 909035013,
    182: 909035014,
    183: 909035015,
    184: 909036001,
    185: 909036002,
    186: 909036003,
    187: 909036004,
    188: 909036005,
    189: 909036006,
    190: 909036008,
    191: 909036009,
    192: 909036010,
    193: 909036011,
    194: 909036012,
    195: 909036014,
    196: 909037001,
    197: 909037002,
    198: 909037003,
    199: 909037004,
    200: 909037005,
    201: 909037006,
    202: 909037007,
    203: 909037008,
    204: 909037009,
    205: 909037010,
    206: 909037011,
    207: 909037012,
    208: 909038001,
    209: 909038002,
    210: 909038003,
    211: 909038004,
    212: 909038005,
    213: 909038006,
    214: 909038008,
    215: 909038009,
    216: 909038010,
    217: 909038011,
    218: 909038012,
    219: 909038013,
    220: 909039001,
    221: 909039002,
    222: 909039003,
    223: 909039004,
    224: 909039005,
    225: 909039006,
    226: 909039007,
    227: 909039008,
    228: 909039009,
    229: 909039010,
    230: 909039011,
    231: 909039012,
    232: 909039013,
    233: 909039014,
    234: 909040001,
    235: 909040002,
    236: 909040003,
    237: 909040004,
    238: 909040005,
    239: 909040006,
    240: 909040008,
    241: 909040009,
    242: 909040010,
    243: 909040011,
    244: 909040012,
    245: 909040013,
    246: 909040014,
    247: 909041001,
    248: 909041002,
    249: 909041003,
    250: 909041004,
    251: 909041005,
    252: 909041006,
    253: 909041007,
    254: 909041008,
    255: 909041009,
    256: 909041010,
    257: 909041011,
    258: 909041012,
    259: 909041013,
    260: 909041014,
    261: 909041015,
    262: 909042001,
    263: 909042002,
    264: 909042003,
    265: 909042004,
    266: 909042005,
    267: 909042006,
    268: 909042007,
    269: 909042008,
    270: 909042009,
    271: 909042011,
    272: 909042012,
    273: 909042013,
    274: 909042016,
    275: 909042017,
    276: 909042018,
    277: 909043001,
    278: 909043002,
    279: 909043003,
    280: 909043004,
    281: 909043005,
    282: 909043006,
    283: 909043007,
    284: 909043008,
    285: 909043009,
    286: 909043010,
    287: 909043013,
    288: 909044001,
    289: 909044002,
    290: 909044003,
    291: 909044004,
    292: 909044005,
    293: 909044006,
    294: 909044007,
    295: 909044008,
    296: 909044009,
    297: 909044010,
    298: 909044011,
    299: 909044012,
    300: 909044015,
    301: 909044016,
    302: 909045001,
    303: 909045002,
    304: 909045003,
    305: 909045004,
    306: 909045005,
    307: 909045006,
    308: 909045007,
    309: 909045008,
    310: 909045009,
    311: 909045010,
    312: 909045011,
    313: 909045012,
    314: 909045015,
    315: 909045016,
    316: 909045017,
    317: 909046001,
    318: 909046002,
    319: 909046003,
    320: 909046004,
    321: 909046005,
    322: 909046006,
    323: 909046007,
    324: 909046008,
    325: 909046009,
    326: 909046010,
    327: 909046011,
    328: 909046012,
    329: 909046013,
    330: 909046014,
    331: 909046015,
    332: 909046016,
    333: 909046017,
    334: 909047001,
    335: 909047002,
    336: 909047003,
    337: 909047004,
    338: 909047005,
    339: 909047006,
    340: 909047007,
    341: 909047008,
    342: 909047009,
    343: 909047010,
    344: 909047011,
    345: 909047012,
    346: 909047013,
    347: 909047015,
    348: 909047016,
    349: 909047017,
    350: 909047018,
    351: 909047019,
    352: 909048001,
    353: 909048002,
    354: 909048003,
    355: 909048004,
    356: 909048005,
    357: 909048006,
    358: 909048007,
    359: 909048008,
    360: 909048009,
    361: 909048010,
    362: 909048011,
    363: 909048012,
    364: 909048013,
    365: 909048014,
    366: 909048015,
    367: 909048016,
    368: 909048017,
    369: 909048018,
    370: 909049001,
    371: 909049002,
    372: 909049003,
    373: 909049004,
    374: 909049005,
    375: 909049006,
    376: 909049007,
    377: 909049008,
    378: 909049009,
    379: 909049010,
    380: 909049011,
    381: 909049012,
    382: 909049013,
    383: 909049014,
    384: 909049015,
    385: 909049016,
    386: 909049017,
    387: 909049018,
    388: 909049019,
    389: 909049020,
    390: 909049021,
    391: 909050002,
    392: 909050003,
    393: 909050004,
    394: 909050005,
    395: 909050006,
    396: 909050008,
    397: 909050009,
    398: 909050010,
    399: 909050011,
    400: 909050012,
    401: 909050013,
    402: 909050014,
    403: 909050015,
    404: 909050016,
    405: 909050017,
    406: 909050018,
    407: 909050019,
    408: 909050020,
    409: 909050021,
    410: 909050026,
    411: 909050027,
    412: 909050028,
    413: 909547001,
    414: 909550001
}

# Badge values for s1 to s5 commands - using your exact values
BADGE_VALUES = {
    "s1": 1048576,    # Your first badge
    "s2": 32768,      # Your second badge  
    "s3": 2048,       # Your third badge
    "s4": 64,         # Your fourth badge
    "s5": 262144     # Your seventh badge
}

# ------------------- Insta API Thread -------------------
def start_insta_api():
    port = insta.find_free_port()
    print(f"🚀 Starting Insta API on port {port}")
    insta.app.run(host="0.0.0.0", port=port, debug=False)
# ------------------- End Insta API Thread -------------------
def uid_generator():
    # ৮ ডিজিটের সর্বনিম্ন সংখ্যা ১০০০০০০০ (10,000,000)
    # আপনার দেওয়া সর্বোচ্চ সীমা ৯৯৯৯৯৯৯৯৯৯৯ (99,999,999,999)
    start = 10000000
    end = 99999999999
    
    for i in range(start, end + 1):
        yield i

def cleanup_cache():
    """Clean old cached data to maintain performance"""
    current_time = time.time()
    # Clean last_request_time
    to_remove = [k for k, v in last_request_time.items() 
                 if current_time - v > CLEANUP_INTERVAL]
    for k in to_remove:
        last_request_time.pop(k, None)
    
    # Clean command_cache if too large
    if len(command_cache) > MAX_CACHE_SIZE:
        oldest_keys = sorted(command_cache.keys())[:len(command_cache)//2]
        for key in oldest_keys:
            command_cache.pop(key, None)

def get_rate_limited_response(user_id):
    """Implement rate limiting to reduce server load"""
    user_key = str(user_id)
    current_time = time.time()
    
    if user_key in last_request_time:
        time_since_last = current_time - last_request_time[user_key]
        if time_since_last < RATE_LIMIT_DELAY:
            return False
    
    last_request_time[user_key] = current_time
    return True

# Helper Functions
def is_admin(uid):
    return str(uid) == ADMIN_UID

# Helper functions for ghost join
def dec_to_hex(decimal):
    """Convert decimal to hex string"""
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def encrypt_packet(packet_hex, key, iv):
    """Encrypt packet using AES CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    """Wrapper for encrypt_packet"""
    return await encrypt_packet(packet_hex, key, iv)
    



def get_idroom_by_idplayer(packet_hex):
    """Extract room ID from packet - converted from your other TCP"""
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        print(f"Error extracting room ID: {e}")
        return None

async def check_player_in_room(target_uid, key, iv):
    """Check if player is in a room by sending status request"""
    try:
        # Send status request packet
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT('OnLine', status_packet)
        
        # You'll need to capture the response packet and parse it
        # For now, return True and we'll handle room detection in the main loop
        return True
    except Exception as e:
        print(f"Error checking player room status: {e}")
        return False
        
        
        
async def handle_alll_titles_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    """Handle /alltitles command to send all titles sequentially"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) == 1:
        target_uid = uid
        target_name = "Yourself"
    elif len(parts) == 2 and parts[1].isdigit():
        target_uid = parts[1]
        target_name = f"UID {target_uid}"
    else:
        error_msg = f"""[B][C][FF0000]❌ Usage: /alltitles [uid]
        
📝 Examples:
/alltitles - Send all titles to yourself
/alltitles 123456789 - Send all titles to specific UID

🎯 What it does:
1. Sends all 4 titles one by one
2. 2-second delay between each title
3. Sends in background (non-blocking)
4. Shows progress updates
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Start the title sequence in the background
    asyncio.create_task(
        send_all_titles_sequentiallly(target_uid, chat_id, key, iv, region, chat_type)
    )
    

async def send_all_titles_sequentiallly(uid, chat_id, key, iv, region, chat_type):
    """Send all titles one by one with 2-second delay"""
    
    # Get all titles
    all_titles = [
        904090014, 904090015, 904090024, 904090025, 904090026, 904090027, 904990070, 904990071, 904990072
    ]
    
    total_titles = len(all_titles)
    
    # Send initial message
    start_msg = f"""[B][C][00FF00] Noobde Black666 ya meku agar tu noob bolra toh tu gay hai


"""
    await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
    
    try:
        for index, title_id in enumerate(all_titles):
            title_number = index + 1
            

            
            # Send the actual title using your existing method
            # You'll need to use your existing title sending logic here
            # For example:
            title_packet = await noob(uid, chat_id, key, iv, nickname="MG24", title_id=title_id)
            
            if title_packet and whisper_writer:
                whisper_writer.write(title_packet)
                await whisper_writer.drain()
                print(f"✅ Sent title {title_number}/{total_titles}: {title_id}")
            
            # Wait 2 seconds before next title (unless it's the last one)
            if title_number < total_titles:
                await asyncio.sleep(2)
        
        # Completion message
        completion_msg = f"""[B][C][00FF00]Noobde ab tu bta ye titles aur bol kon noob hai
"""
        await safe_send_message(chat_type, completion_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error sending titles: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def noob(target_uid, chat_id, key, iv, nickname="MG24", title_id=None):
    """EXACT conversion with customizable title ID"""
    try:
        # Use provided title_id or get random one
        if title_id is None:
            # Get a random title from the list
            available_titles = [904090014, 904090015, 904090024, 904090025, 904090026, 904090027, 904990070, 904990071, 904990072]
            title_id = random.choice(available_titles)
        
        # Create fields dictionary with specific title_id
        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(await xBunnEr()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 1,
                    13: {
                        1: 2
                    },
                    14: {
                        1: 8804135237,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {
                    2: 2,
                    3: 1
                },
                14: {}
            }
        }
        
        # ... rest of your existing function
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        
        print(f"✅ Created packet with Title ID: {title_id}")
        return final_packet
        
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return None
        

async def send_title_packet_direct(target_uid, chat_id, key, iv, region="ind"):
    """Send title packet directly without chat context - for auto-join"""
    try:
        print(f"🎖️ Sending title to {target_uid} in chat {chat_id}")
        
        # Method 1: Using your existing function
        title_packet = await convert_kyro_to_your_system(target_uid, chat_id, key, iv)
        
        if title_packet and whisper_writer:
            # Send via Whisper connection
            whisper_writer.write(title_packet)
            await whisper_writer.drain()
            print(f"✅ Title sent via Whisper to {target_uid}")
            return True
            
    except Exception as e:
        print(f"❌ Error sending title directly: {e}")
        import traceback
        traceback.print_exc()
    
    return False

def titles():
    """Return all titles instead of just one random"""
    titles_list = [
        905090075, 904990072, 904990069, 905190079
    ]
    return titles_list  # Return the full list instead of random.choice            
    
    
class MultiAccountManager:
    def __init__(self):
        self.accounts_file = "accounts.json"
        self.accounts_data = self.load_accounts()
    
    def load_accounts(self):
        """Load multiple accounts from JSON file"""
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)

                return accounts
        except FileNotFoundError:
            print(f"❌ Accounts file {self.accounts_file} not found!")
            return {}
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
            return {}
    
    
    
    async def get_account_token(self, uid, password):
        """Get access token for a specific account"""
        try:
            url = "https://10000067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": await Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            }
            data = {
                "uid": uid,
                "password": password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        open_id = data.get("open_id")
                        access_token = data.get("access_token")
                        return open_id, access_token
            return None, None
        except Exception as e:
            print(f"❌ Error getting token for {uid}: {e}")
            return None, None

async def send_title_packet_direct(target_uid, chat_id, key, iv, region="ind"):
    """Send title packet directly without chat context - for auto-join"""
    try:
        print(f"🎖️ Sending title to {target_uid} in chat {chat_id}")
        
        # Method 1: Using your existing function
        title_packet = await convert_kyro_to_your_system(target_uid, chat_id, key, iv)
        
        if title_packet and whisper_writer:
            # Send via Whisper connection
            whisper_writer.write(title_packet)
            await whisper_writer.drain()
            print(f"✅ Title sent via Whisper to {target_uid}")
            return True
            
    except Exception as e:
        print(f"❌ Error sending title directly: {e}")
        import traceback
        traceback.print_exc()
    
    return False

async def handle_alll_titles_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    """Handle /alltitles command to send all titles sequentially"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) == 1:
        target_uid = uid
        target_name = "Yourself"
    elif len(parts) == 2 and parts[1].isdigit():
        target_uid = parts[1]
        target_name = f"UID {target_uid}"
    else:
        error_msg = f"""[B][C][FF0000]❌ Usage: /alltitles [uid]
        
📝 Examples:
/alltitles - Send all titles to yourself
/alltitles 123456789 - Send all titles to specific UID

🎯 What it does:
1. Sends all 4 titles one by one
2. 2-second delay between each title
3. Sends in background (non-blocking)
4. Shows progress updates
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Start the title sequence in the background
    asyncio.create_task(
        send_all_titles_sequentiallly(target_uid, chat_id, key, iv, region, chat_type)
    )
    

def get_random_sticker():
    """
    Randomly select one sticker from available packs
    """

    sticker_packs = [
        # NORMAL STICKERS (1200000001-1 to 24)
        ("1200000001", 1, 24),

        # KELLY EMOJIS (1200000002-1 to 15)
        ("1200000002", 1, 15),

        # MAD CHICKEN (1200000004-1 to 13)
        ("1200000004", 1, 13),
    ]

    pack_id, start, end = random.choice(sticker_packs)
    sticker_no = random.randint(start, end)

    return f"[1={pack_id}-{sticker_no}]"
        
async def send_sticker(target_uid, chat_id, key, iv, nickname="BLACK"):
    """Send Random Sticker using /sticker command"""
    try:
        sticker_value = get_random_sticker()

        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"StickerStr" : "{sticker_value}", "type":"Sticker"}}',
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(get_random_avatar()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 66,
                    12: 66,
                    13: {1: 2},
                    14: {
                        1: 8804135237,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {
                    2: 2,
                    3: 1
                },
                14: {}
            }
        }

        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()

        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"

        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)

        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)

        print(f"✅ Sticker Sent: {sticker_value}")
        return final_packet

    except Exception as e:
        print(f"❌ Sticker error: {e}")
        return None

# Alternative: DIRECT port of your friend's function but with your UID
async def send_kyro_title_adapted(chat_id, key, iv, target_uid, nickname="BLACK666FF"):
    """Direct adaptation of your friend's working function"""
    try:
        # Import your proto file (make sure it's in the same directory)
        from kyro_title_pb2 import GenTeamTitle
        
        root = GenTeamTitle()
        root.type = 1
        
        nested_object = root.data
        nested_object.uid = int(target_uid)  # CHANGE: Use target UID
        nested_object.chat_id = int(chat_id)
        nested_object.title = f"{{\"TitleID\":{titles()},\"type\":\"Title\"}}"
        nested_object.timestamp = int(datetime.now().timestamp())
        nested_object.language = "en"
        
        nested_details = nested_object.field9
        nested_details.Nickname = f"[C][B][FF0000]{nickname}"  # CHANGE: Your nickname
        nested_details.avatar_id = int(await xBunnEr())  # Use your function
        nested_details.rank = 330
        nested_details.badge = 102000015
        nested_details.Clan_Name = "BOT TEAM"  # CHANGE: Your clan
        nested_details.field10 = 1
        nested_details.global_rank_pos = 1
        nested_details.badge_info.value = 2
        
        nested_details.prime_info.prime_uid = 8804135237
        nested_details.prime_info.prime_level = 8
        # IMPORTANT: This must be bytes, not string!
        nested_details.prime_info.prime_hex = b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
        
        nested_options = nested_object.field13
        nested_options.url_type = 2
        nested_options.curl_platform = 1
        
        nested_object.empty_field.SetInParent()
        
        # Serialize
        packet = root.SerializeToString().hex()
        
        # Use YOUR encryption function
        encrypted_packet = await encrypt_packet(packet, key, iv)
        
        # Calculate length
        packet_length = len(encrypted_packet) // 2
        
        # Convert to hex (4 characters with leading zeros)
        hex_length = f"{packet_length:04x}"
        
        # Build packet EXACTLY like your friend
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        return bytes.fromhex(final_packet_hex)
        
    except Exception as e:
        print(f"❌ Direct adaptation error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def send_all_titles_sequentially(uid, chat_id, key, iv, region, chat_type):
    """Send all titles one by one with 2-second delay"""
    
    # Get all titles
    all_titles = [
        905090075, 904990072, 904990069, 905190079
    ]
    
    total_titles = len(all_titles)
    
    # Send initial message
    start_msg = f"""[B][C][00FF00]🎖️ STARTING TITLE SEQUENCE!

📊 Total Titles: {total_titles}
⏱️ Delay: 2 seconds between titles
🔁 Mode: Sequential
🎯 Target: {uid}

⏳ Sending titles now...
"""
    await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
    
    try:
        for index, title_id in enumerate(all_titles):
            title_number = index + 1
            
            # Create progress message
            progress_msg = f"""[B][C][FFFF00]📤 SENDING TITLE {title_number}/{total_titles}

🎖️ Title ID: {title_id}
📊 Progress: {title_number}/{total_titles}
⏱️ Next in: 2 seconds
"""
            await safe_send_message(chat_type, progress_msg, uid, chat_id, key, iv)
            
            # Send the actual title using your existing method
            # You'll need to use your existing title sending logic here
            # For example:
            title_packet = await convert_kyro_to_your_system(uid, chat_id, key, iv, nickname="BLACK666FF", title_id=title_id)
            
            if title_packet and whisper_writer:
                whisper_writer.write(title_packet)
                await whisper_writer.drain()
                print(f"✅ Sent title {title_number}/{total_titles}: {title_id}")
            
            # Wait 2 seconds before next title (unless it's the last one)
            if title_number < total_titles:
                await asyncio.sleep(2)
        
        # Completion message
        completion_msg = f"""[B][C][00FF00]✅ ALL TITLES SENT SUCCESSFULLY!

🎊 Total: {total_titles} titles sent
🎯 Target: {uid}
⏱️ Duration: {total_titles * 2} seconds
✅ Status: Complete!

🎖️ Titles Sent:
1. 905090075
2. 904990072
3. 904990069
4. 905190079
"""
        await safe_send_message(chat_type, completion_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error sending titles: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def handle_all_titles_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type=0):
    """Handle /alltitles command to send all titles sequentially"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) == 1:
        target_uid = uid
        target_name = "Yourself"
    elif len(parts) == 2 and parts[1].isdigit():
        target_uid = parts[1]
        target_name = f"UID {target_uid}"
    else:
        error_msg = f"""[B][C][FF0000]❌ Usage: /alltitles [uid]
        
📝 Examples:
/alltitles - Send all titles to yourself
/alltitles 123456789 - Send all titles to specific UID

🎯 What it does:
1. Sends all 4 titles one by one
2. 2-second delay between each title
3. Sends in background (non-blocking)
4. Shows progress updates
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Start the title sequence in the background
    asyncio.create_task(
        send_all_titles_sequentially(target_uid, chat_id, key, iv, region, chat_type)
    )
    
    # Immediate response
    response_msg = f"""[B][C][00FF00]🚀 STARTING TITLE SEQUENCE IN BACKGROUND!

👤 Target: {target_name}
🎖️ Total Titles: 4
⏱️ Delay: 2 seconds each
📱 Status: Running in background...

💡 You'll receive progress updates as titles are sent!
"""
    await safe_send_message(chat_type, response_msg, uid, chat_id, key, iv)


async def convert_kyro_to_your_system(target_uid, chat_id, key, iv, nickname="BLACK666FF", title_id=None):
    """EXACT conversion with customizable title ID"""
    try:
        # Use provided title_id or get random one
        if title_id is None:
            # Get a random title from the list
            available_titles = [905090075, 904990072, 904990069, 905190079]
            title_id = random.choice(available_titles)
        
        # Create fields dictionary with specific title_id
        fields = {
            1: 1,
            2: {
                1: int(target_uid),
                2: int(chat_id),
                5: int(datetime.now().timestamp()),
                8: f'{{"TitleID":{title_id},"type":"Title"}}',  # Use specific title ID
                # ... rest of your fields
                9: {
                    1: f"[C][B][FF0000]{nickname}",
                    2: int(await xBunnEr()),
                    4: 330,
                    5: 102000015,
                    8: "BOT TEAM",
                    10: 1,
                    11: 1,
                    13: {
                        1: 2
                    },
                    14: {
                        1: 8804135237,
                        2: 8,
                        3: b"\x10\x15\x08\x0a\x0b\x15\x0c\x0f\x11\x04\x07\x02\x03\x0d\x0e\x12\x01\x05\x06"
                    }
                },
                10: "en",
                13: {
                    2: 2,
                    3: 1
                },
                14: {}
            }
        }
        
        # ... rest of your existing function
        proto_bytes = await CrEaTe_ProTo(fields)
        packet_hex = proto_bytes.hex()
        
        encrypted_packet = await encrypt_packet(packet_hex, key, iv)
        packet_length = len(encrypted_packet) // 2
        hex_length = f"{packet_length:04x}"
        
        zeros_needed = 6 - len(hex_length)
        packet_prefix = "121500" + ("0" * zeros_needed)
        
        final_packet_hex = packet_prefix + hex_length + encrypted_packet
        final_packet = bytes.fromhex(final_packet_hex)
        
        print(f"✅ Created packet with Title ID: {title_id}")
        return final_packet
        
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return None
            
    async def send_join_from_account(self, target_uid, account_uid, password, key, iv, region):
        """Send join request from a specific account"""
        try:
            # Get token for this account
            open_id, access_token = await self.get_account_token(account_uid, password)
            if not open_id or not access_token:
                return False
            
            # Create join packet using the account's credentials
            join_packet = await self.create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region)
            if join_packet:
                await SEndPacKeT('OnLine', join_packet)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error sending join from {account_uid}: {e}")
            return False
            
async def SEnd_InV_with_Cosmetics(Nu, Uid, K, V, region):
    """Simple version - just add field 5 with basic cosmetics"""
    region = "ind"
    fields = {
        1: 2, 
        2: {
            1: int(Uid), 
            2: region, 
            4: int(Nu),
            # Simply add field 5 with basic cosmetics
            5: {
                1: "BOT",                    # Name
                2: int(await get_random_avatar()),     # Avatar
                5: random.choice([1048576, 32768, 2048]),  # Random badge
            }
        }
    }

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
        
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)   
            
async def join_custom_room(room_id, room_password, key, iv, region):
    """Join custom room with proper Free Fire packet structure"""
    fields = {
        1: 61,  # Room join packet type (verified for Free Fire)
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),  # Room ID
                2: int(time.time()),  # Timestamp
                3: "BOT",  # Player name
                5: 12,  # Unknown
                6: 9999999,  # Unknown
                7: 1,  # Unknown
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,  # Room type
            },
            3: str(room_password),  # Room password
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def leave_squad(key, iv, region):
    """Leave squad - converted from your old TCP leave_s()"""
    fields = {
        1: 7,
        2: {
            1: 12480598706  # Your exact value from old TCP
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk(packet, packet_type, key, iv)    
    
async def RedZed_SendInv(bot_uid, uid, key, iv):
    """Async version of send invite function"""
    try:
        fields = {
            1: 33, 
            2: {
                1: int(uid), 
                2: "IND", 
                3: 1, 
                4: 1, 
                6: "RedZedKing!!", 
                7: 330, 
                8: 1000, 
                9: 100, 
                10: "DZ", 
                12: 1, 
                13: int(uid), 
                16: 1, 
                17: {
                    2: 159, 
                    4: "y[WW", 
                    6: 11, 
                    8: "1.120.1", 
                    9: 3, 
                    10: 1
                }, 
                18: 306, 
                19: 18, 
                24: 902000306, 
                26: {}, 
                27: {
                    1: 11, 
                    2: int(bot_uid), 
                    3: 99999999999
                }, 
                28: {}, 
                31: {
                    1: 1, 
                    2: 32768
                }, 
                32: 32768, 
                34: {
                    1: bot_uid, 
                    2: 8, 
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                }
            }
        }
        
        # Convert bytes properly
        if isinstance(fields[2][34][3], str):
            fields[2][34][3] = b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
        
        # Use async versions of your functions
        packet = await CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
        
        # Generate final packet
        final_packet = GeneRaTePk(packet_hex, '0515', key, iv)
        
        return final_packet
        
    except Exception as e:
        print(f"❌ Error in RedZed_SendInv: {e}")
        import traceback
        traceback.print_exc()
        return None
    
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    """Send join request with specific badge - converted from your old TCP"""
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] MG24_GAMER",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(await get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value  # Dynamic badge value
            },
            32: badge_value,    # Dynamic badge value
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk(packet, packet_type, key, iv)    
    
async def start_auto_packet(key, iv, region):
    """Create start match packet"""
    fields = {
        1: 9,
        2: {
            1: 12480598706,
        },
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def leave_squad_packet(key, iv, region):
    """Leave squad packet"""
    fields = {
        1: 7,
        2: {
            1: 12480598706,
        },
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def join_teamcode_packet(team_code, key, iv, region):
    """Join team using code"""
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(team_code),
            6: 6,
            8: 1,
            9: {
                2: 800,
                6: 11,
                8: "1.111.1",
                9: 5,
                10: 1
            }
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def auto_start_loop(team_code, uid, chat_id, chat_type, key, iv, region):
    """Auto start loop that joins, starts match, waits, leaves, repeats"""
    global auto_start_running, stop_auto
    
    print(f"[AUTO] Auto start loop started for team {team_code}")
    
    while not stop_auto:
        try:
            # Send status message
            status_msg = f"[B][C][FFA500]🤖 Auto Start Bot\n🎯 Team: {team_code}\n⚡ Joining team..."
            await safe_send_message(chat_type, status_msg, uid, chat_id, key, iv)
            
            # Join team
            join_packet = await join_teamcode_packet(team_code, key, iv, region)
            await SEndPacKeT('OnLine', join_packet)
            await asyncio.sleep(2)
            
            # Send start spam status
            start_msg = f"[B][C][00FF00]✅ Joined team {team_code}\n🎯 Starting match for {start_spam_duration} seconds..."
            await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
            
            # Start spam
            start_packet = await start_auto_packet(key, iv, region)
            end_time = time.time() + start_spam_duration
            spam_count = 0
            
            while time.time() < end_time and not stop_auto:
                await SEndPacKeT('OnLine', start_packet)
                spam_count += 1
                await asyncio.sleep(start_spam_delay)
            
            if stop_auto:
                break
            
            # Wait after match
            wait_msg = f"[B][C][FFFF00]⏳ Match started! Bot in lobby waiting {wait_after_match} seconds..."
            await safe_send_message(chat_type, wait_msg, uid, chat_id, key, iv)
            
            waited = 0
            while waited < wait_after_match and not stop_auto:
                await asyncio.sleep(1)
                waited += 1
            
            if stop_auto:
                break
            
            # Leave squad
            leave_msg = f"[B][C][FF0000]🔄 Leaving team {team_code} to rejoin and start again..."
            await safe_send_message(chat_type, leave_msg, uid, chat_id, key, iv)
            
            leave_packet = await leave_squad_packet(key, iv, region)
            await SEndPacKeT('OnLine', leave_packet)
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"[AUTO] Error in auto_start_loop: {e}")
            error_msg = f"[B][C][FF0000]❌ Auto start error: {str(e)}\n"
            await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            break
    
    auto_start_running = False
    stop_auto = False
    print(f"[AUTO] Auto start loop stopped for team {team_code}")
    
async def reset_bot_state(key, iv, region):
    """Reset bot to solo mode before spam - Critical step from your old TCP"""
    try:
        # Leave any current squad (using your exact leave_s function)
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT('OnLine', leave_packet)
        await asyncio.sleep(0.5)
        
        print("✅ Bot state reset - left squad")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting bot: {e}")
        return False    
    
async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    """Create a custom room"""
    fields = {
        1: 3,  # Create room packet type
        2: {
            1: room_name,
            2: room_password,
            3: max_players,  # 2, 4, 8, 16, etc.
            4: 1,  # Room mode
            5: 1,  # Map
            6: "en",  # Language
            7: {   # Player info
                1: "BotHost",
                2: int(await get_random_avatar()),
                3: 330,
                4: 1048576,
                5: "BOTCLAN"
            }
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)              
            
async def real_multi_account_join(target_uid, key, iv, region):
    """Send join requests using real account sessions"""
    try:
        # Load accounts
        accounts_data = load_accounts()
        if not accounts_data:
            return 0, 0
        
        success_count = 0
        total_accounts = len(accounts_data)
        
        for account_uid, password in accounts_data.items():
            try:
                print(f"🔄 Authenticating account: {account_uid}")
                
                # Get proper tokens for this account
                open_id, access_token = await GeNeRaTeAccEss(account_uid, password)
                if not open_id or not access_token:
                    print(f"❌ Failed to authenticate {account_uid}")
                    continue
                
                # Create a proper join request using the account's identity
                # We'll use the existing SEnd_InV function but with account context
                join_packet = await create_authenticated_join(target_uid, account_uid, key, iv, region)
                
                if join_packet:
                    await SEndPacKeT('OnLine', join_packet)
                    success_count += 1
                    print(f"✅ Join sent from authenticated account: {account_uid}")
                
                # Important: Wait between requests
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Error with account {account_uid}: {e}")
                continue
        
        return success_count, total_accounts
        
    except Exception as e:
        print(f"❌ Multi-account join error: {e}")
        return 0, 0



async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle individual badge commands"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /{cmd} (uid)\nExample: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Reset bot state
        await reset_bot_state(key, iv, region)
        
        # Create and send join packets
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 3
        
        for i in range(spam_count):
            await SEndPacKeT('OnLine', join_packet)
            print(f"✅ Sent /{cmd} request #{i+1} with badge {badge_value}")
            await asyncio.sleep(0.1)
        
        success_msg = f"[B][C][00FF00]✅ Successfully Sent {spam_count} Join Requests!\n🎯 Target: {target_uid}\n🏷️ Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Cleanup
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def create_authenticated_join(target_uid, account_uid, key, iv, region):
    """Create join request that appears to come from the specific account"""
    try:
        # Use the standard invite function but ensure it uses account context
        join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
        return join_packet
    except Exception as e:
        print(f"❌ Error creating join packet: {e}")
        return None        
    
    async def create_account_join_packet(self, target_uid, account_uid, open_id, access_token, key, iv, region):
        """Create join request packet for specific account"""
        try:
            # This is where you use the account's actual UID instead of main bot UID
            fields = {
                1: 33,
                2: {
                    1: int(target_uid),  # Target UID
                    2: region.upper(),
                    3: 1,
                    4: 1,
                    5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                    6: f"BOT:[C][B][FF0000] ACCOUNT_{account_uid[-4:]}",  # Show account UID
                    7: 330,
                    8: 1000,
                    10: region.upper(),
                    11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                               97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
                    12: 1,
                    13: int(account_uid),  # Use the ACCOUNT'S UID here, not target UID!
                    14: {
                        1: 2203434355,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    },
                    16: 1,
                    17: 1,
                    18: 312,
                    19: 46,
                    23: bytes([16, 1, 24, 1]),
                    24: int(await get_random_avatar()),
                    26: "",
                    28: "",
                    31: {
                        1: 1,
                        2: 32768  # V-Badge
                    },
                    32: 32768,
                    34: {
                        1: int(account_uid),  # Use the ACCOUNT'S UID here too!
                        2: 8,
                        3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
                    }
                },
                10: "en",
                13: {
                    2: 1,
                    3: 1
                }
            }
            
            packet = (await CrEaTe_ProTo(fields)).hex()
            
            if region.lower() == "ind":
                packet_type = '0514'
            elif region.lower() == "bd":
                packet_type = "0519"
            else:
                packet_type = "0515"
                
            return GeneRaTePk(packet, packet_type, key, iv)
            
        except Exception as e:
            print(f"❌ Error creating join packet for {account_uid}: {e}")
            return None

# Global instance
multi_account_manager = MultiAccountManager()
    
    
    
async def auto_rings_emote_dual(sender_uid, key, iv, region):
    """Send The Rings emote to both sender and bot for dual emote effect"""
    try:
        # The Rings emote ID
        rings_emote_id = 909050009
        
        # Get bot's UID
        bot_uid = 13777711848
        
        # Send emote to SENDER (person who invited)
        emote_to_sender = await Emote_k(int(sender_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT('OnLine', emote_to_sender)
        
        # Small delay between emotes
        await asyncio.sleep(0.5)
        
        # Send emote to BOT (bot performs emote on itself)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT('OnLine', emote_to_bot)
        
        print(f"🤖 Bot performed dual Rings emote with sender {sender_uid} and bot {bot_uid}!")
        
    except Exception as e:
        print(f"Error sending dual rings emote: {e}")    
        
        
async def Room_Spam(Uid, Rm, Nm, K, V):
   
    same_value = random.choice([32768])  #you can add any badge value 
    
    fields = {
        1: 78,
        2: {
            1: int(Rm),  
            2: "iG:[C][B][FF0000] MG24_GAMER",  
            3: {
                2: 1,
                3: 1
            },
            4: 330,      
            5: 6000,     
            6: 201,      
            10: int(await get_random_avatar()),  
            11: int(Uid), # Target UID
            12: 1,       
            15: {
                1: 1,
                2: same_value  
            },
            16: same_value,    
            18: {
                1: 11481904755,  
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            
            31: {
                1: 1,
                2: same_value  
            },
            32: same_value,    
            34: {
                1: int(Uid),   
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
    
async def evo_cycle_spam(uids, key, iv, region):
    """Cycle through all evolution emotes one by one with 5-second delay"""
    global evo_cycle_running
    
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Starting evolution emote cycle #{cycle_count}")
        
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running:
                break
                
            print(f"Sending evolution emote {emote_number} (ID: {emote_id})")
            
            for uid in uids:
                try:
                    uid_int = int(uid)
                    H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT('OnLine', H)
                    print(f"Sent emote {emote_number} to UID: {uid}")
                except Exception as e:
                    print(f"Error sending evo emote {emote_number} to {uid}: {e}")
            
            # Wait 10 seconds before moving to next emote (changed from 5 to 10)
            if evo_cycle_running:
                print(f"Waiting 10 seconds before next emote...")
                for i in range(10):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        
        # Small delay before restarting the cycle
        if evo_cycle_running:
            print("Completed one full cycle of all evolution emotes. Restarting...")
            await asyncio.sleep(2)
    
    print("Evolution emote cycle stopped")
    
async def reject_spam_loop(target_uid, key, iv):
    """Send reject spam packets to target in background"""
    global reject_spam_running
    
    count = 0
    max_spam = 150
    
    while reject_spam_running and count < max_spam:
        try:
            # Send both packets
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            
            # Send to Online connection
            await SEndPacKeT('OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT('OnLine', packet2)
            
            count += 1
            print(f"Sent reject spam #{count} to {target_uid}")
            
            # 0.2 second delay between spam cycles
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"Error in reject spam: {e}")
            break
    
    return count    
    
async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle completion of reject spam and send final message"""
    try:
        spam_count = await spam_task
        
        # Send completion message
        if spam_count >= 150:
            completion_msg = f"[B][C][00FF00]✅ Reject Spam Completed Successfully for ID {target_uid}\n✅ Total packets sent: {spam_count * 2}\n"
        else:
            completion_msg = f"[B][C][FFFF00]⚠️ Reject Spam Partially Completed for ID {target_uid}\n⚠️ Total packets sent: {spam_count * 2}\n"
        
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("Reject spam was cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ ERROR in reject spam: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)    
    
async def banecipher(client_id, key, iv):
    """Create reject spam packet 1 - Converted to new async format"""
    banner_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: 5,
        2: {
            1: int(client_id),
            2: 1,
            3: int(client_id),
            4: banner_text
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    """Create reject spam packet 2 - Converted to new async format"""
    gay_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[0. 00000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[0000=00]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: int(client_id),
        2: 5,
        4: 50,
        5: {
            1: int(client_id),
            2: gay_text,
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)
    

async def lag_team_loop(team_code, key, iv, region):
    """Rapid join/leave loop to create lag"""
    global lag_running
    count = 0
    
    while lag_running:
        try:
            # Join the team
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT('OnLine', join_packet)
            
            # Very short delay before leaving
            await asyncio.sleep(0.01)  # 10 milliseconds
            
            # Leave the team
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT('OnLine', leave_packet)
            
            count += 1
            print(f"Lag cycle #{count} completed for team: {team_code}")
            
            # Short delay before next cycle
            await asyncio.sleep(0.01)  # 10 milliseconds between cycles
            
        except Exception as e:
            print(f"Error in lag loop: {e}")
            # Continue the loop even if there's an error
            await asyncio.sleep(0.1)
 
####################################
def bundle_packet(self, bundle_id, target_uid):
        fields = {
            1: 88,
            2: {
                1: {
                    1: bundle_id,
                    2: 1
                },
                2: 2
            }
        }
        packet = create_protobuf_packet(fields).hex()
        encrypted = encrypt_packet(packet, self.key, self.iv)
        header_length = len(encrypted) // 2
        header_length_hex = dec_to_hex(header_length)

        if len(header_length_hex) == 2:
            final_header = "0515000000"
        elif len(header_length_hex) == 3:
            final_header = "051500000"
        elif len(header_length_hex) == 4:
            final_header = "05150000"
        elif len(header_length_hex) == 5:
            final_header = "0515000"
        else:
            final_header = "0515000000"

        final_packet = final_header + header_length_hex + encrypted
        return bytes.fromhex(final_packet)

async def bundle_packet_async(bundle_id, key, iv, region="ind"):
    """Create bundle packet"""
    fields = {
        1: 88,
        2: {
            1: {
                1: bundle_id,
                2: 1
            },
            2: 2
        }
    }
    
    # Use your CrEaTe_ProTo function
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use your encrypt_packet function
    encrypted = await encrypt_packet(packet_hex, key, iv)
    
    # Use your DecodE_HeX function
    header_length = len(encrypted) // 2
    header_length_hex = DecodE_HeX(header_length)
    
    # Build final packet based on region
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    
    # Determine header based on length
    if len(header_length_hex) == 2:
        final_header = f"{packet_type}000000"
    elif len(header_length_hex) == 3:
        final_header = f"{packet_type}00000"
    elif len(header_length_hex) == 4:
        final_header = f"{packet_type}0000"
    elif len(header_length_hex) == 5:
        final_header = f"{packet_type}000"
    else:
        final_header = f"{packet_type}000000"
    
    final_packet_hex = final_header + header_length_hex + encrypted
    return bytes.fromhex(final_packet_hex)

	
#Clan-info-by-clan-id
def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            msg = f""" 
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
▶▶▶▶GUILD DETAILS◀◀◀◀
Achievements: {data['achievements']}\n\n
Balance : {fix_num(data['balance'])}\n\n
Clan Name : {data['clan_name']}\n\n
Expire Time : {fix_num(data['guild_details']['expire_time'])}\n\n
Members Online : {fix_num(data['guild_details']['members_online'])}\n\n
Regional : {data['guild_details']['regional']}\n\n
Reward Time : {fix_num(data['guild_details']['reward_time'])}\n\n
Total Members : {fix_num(data['guild_details']['total_members'])}\n\n
ID : {fix_num(data['id'])}\n\n
Last Active : {fix_num(data['last_active'])}\n\n
Level : {fix_num(data['level'])}\n\n
Rank : {fix_num(data['rank'])}\n\n
Region : {data['region']}\n\n
Score : {fix_num(data['score'])}\n\n
Timestamp1 : {fix_num(data['timestamp1'])}\n\n
Timestamp2 : {fix_num(data['timestamp2'])}\n\n
Welcome Message: {data['welcome_message']}\n\n
XP: {fix_num(data['xp'])}\n\n
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
            """
            return msg
        else:
            msg = """
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
Failed to get info, please try again later!!

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
            """
            return msg
    except:
        pass
#GET INFO BY PLAYER ID
def get_player_info(player_id):
    url = f"https://like2.vercel.app/player-info?uid={player_id}&server={server2}&key={key2}"
    response = requests.get(url)
    print(response)    
    if response.status_code == 200:
        try:
            r = response.json()
            return {
                "Account Booyah Pass": f"{r.get('booyah_pass_level', 'N/A')}",
                "Account Create": f"{r.get('createAt', 'N/A')}",
                "Account Level": f"{r.get('level', 'N/A')}",
                "Account Likes": f" {r.get('likes', 'N/A')}",
                "Name": f"{r.get('nickname', 'N/A')}",
                "UID": f" {r.get('accountId', 'N/A')}",
                "Account Region": f"{r.get('region', 'N/A')}",
                }
        except ValueError as e:
            pass
            return {
                "error": "Invalid JSON response"
            }
    else:
        pass
        return {
            "error": f"Failed to fetch data: {response.status_code}"
        }
#GET PLAYER BIO 
def get_player_bio(uid):
    try:
        url = f"https://mg24-gamer-super-info-api.vercel.app/get?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # Bio is inside socialInfo -> signature
            bio = data.get('socialinfo', {}).get('signature', 'No Bio Found')
            if bio:
                return bio
            else:
                return "No bio available"
        else:
            return f"Failed to fetch bio. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"
#GET PLAYER INFO 
def get_player_basic(uid):
    try:
        url = f"https://mg24-gamer-super-info-api.vercel.app/get?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # basic is inside socialInfo -> signature
            basic = data.get('AccountInfo', {}).get('AccountName', 'Unknown')
            level = data.get('AccountInfo', {}).get('AccountLevel', None)
            like = data.get('AccountInfo', {}).get('AccountLikes', None)
            region = data.get('AccountInfo', {}).get('AccountRegion', None)
            version = data.get('AccountInfo', {}).get('ReleaseVersion', None)
            guild_name = data.get('GuildInfo', {}).get('GuildName', None)
            bp_badge = data.get('AccountInfo', {}).get('AccountBPBadges', None)
            if basic:
                return f"""
[C][B][FFFF00]━━━━━━━━━━━━
[C][B][FFFFFF]Name: [66FF00]{basic}
[C][B][FFFFFF]level: [66FF00]{level}
[C][B][FFFFFF]like: [66FF00]{like}
[C][B][FFFFFF]region: [66FF00]{region}
[C][B][FFFFFF]last login version: [66FF00]{version}
[C][B][FFFFFF]Booyah Pass Badge: [66FF00]{bp_badge}
[C][B][FFFFFF]guild name: [66FF00]{guild_name}
[C][B][FFFF00]━━━━━━━━━━━━
"""
            else:
                return "No basic available"
        else:
            return f"Failed to fetch basic. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"
#GET ADD FRIEND
def get_player_add(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=GUEST_UID&password=YOUR_GUEST_PASSWORD&friend_uid={uid}"
        res = requests.get(url)
        data = res.json()
            # add is inside socialInfo -> signature
        action = data.get('action', 'Unknown')
        status = data.get('status', 'Unknown')
        message = data.get('message', 'No message received')
        if action:
            return message
        else:
            return message
    except Exception as e:
        return f"Error occurred: {e}"

# ১ থেকে ১০০ পর্যন্ত প্রতিটি আইডি এবং পাসওয়ার্ড আলাদা ফাংশন হিসেবে নিচে দেওয়া হলো:
def get_player_add_1(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818952&password=MG24_GAMER_KING_ZL4Y&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_2(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808011&password=MG24_GAMER_KING_M6QE&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_3(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808118&password=MG24_GAMER_KING_KFYN&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_4(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808121&password=MG24_GAMER_KING_DBWT&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_5(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808005&password=MG24_GAMER_KING_A6LQ&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_6(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808465&password=MG24_GAMER_KING_4K2T&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_7(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808488&password=MG24_GAMER_KING_3WYS&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_8(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808492&password=MG24_GAMER_KING_8TO0&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_9(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808487&password=MG24_GAMER_KING_IHLA&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_10(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808744&password=MG24_GAMER_KING_4RLN&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_11(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808757&password=MG24_GAMER_KING_AI2C&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_12(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808745&password=MG24_GAMER_KING_JM3R&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_13(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808736&password=MG24_GAMER_KING_55MV&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_14(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379808779&password=MG24_GAMER_KING_OL5G&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_15(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809073&password=MG24_GAMER_KING_4XV3&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_16(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809095&password=MG24_GAMER_KING_9F3O&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_17(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809093&password=MG24_GAMER_KING_87FM&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_18(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809105&password=MG24_GAMER_KING_YYEX&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_19(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809060&password=MG24_GAMER_KING_A0QN&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_20(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809304&password=MG24_GAMER_KING_QX77&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_21(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809342&password=MG24_GAMER_KING_NW2V&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_22(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809363&password=MG24_GAMER_KING_FGOW&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_23(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809353&password=MG24_GAMER_KING_7P6P&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_24(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809476&password=MG24_GAMER_KING_8RMP&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_25(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809547&password=MG24_GAMER_KING_VWJH&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_26(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809582&password=MG24_GAMER_KING_FHE1&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_27(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809598&password=MG24_GAMER_KING_GRCL&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_28(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379809754&password=MG24_GAMER_KING_0YSB&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_29(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810560&password=MG24_GAMER_KING_HXLD&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_30(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810647&password=MG24_GAMER_KING_OJVS&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_31(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810661&password=MG24_GAMER_KING_BSK8&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_32(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810909&password=MG24_GAMER_KING_YKF9&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_33(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810900&password=MG24_GAMER_KING_PE0H&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_34(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810922&password=MG24_GAMER_KING_I0QH&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_35(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811000&password=MG24_GAMER_KING_N7NM&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_36(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379810998&password=MG24_GAMER_KING_TYRL&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_37(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811235&password=MG24_GAMER_KING_WZB7&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_38(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811249&password=MG24_GAMER_KING_GPS0&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_39(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811282&password=MG24_GAMER_KING_IPS6&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_40(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811297&password=MG24_GAMER_KING_QKR9&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_41(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811310&password=MG24_GAMER_KING_1I6E&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_42(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811554&password=MG24_GAMER_KING_0TCA&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_43(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811557&password=MG24_GAMER_KING_D679&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_44(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379811548&password=MG24_GAMER_KING_XOJA&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_45(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812532&password=MG24_GAMER_KING_DYLJ&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_46(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812544&password=MG24_GAMER_KING_F9YB&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_47(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812595&password=MG24_GAMER_KING_GM2M&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_48(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812617&password=MG24_GAMER_KING_EZAC&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_49(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812814&password=MG24_GAMER_KING_MI7R&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_50(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812846&password=MG24_GAMER_KING_PSOO&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_51(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379812813&password=MG24_GAMER_KING_IZGI&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_52(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813093&password=MG24_GAMER_KING_B6YS&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_53(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813089&password=MG24_GAMER_KING_UUMA&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_54(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813180&password=MG24_GAMER_KING_TGUJ&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_55(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813168&password=MG24_GAMER_KING_JD3L&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_56(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813269&password=MG24_GAMER_KING_8LQW&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_57(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813368&password=MG24_GAMER_KING_9C9J&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_58(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813378&password=MG24_GAMER_KING_3D3L&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_59(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813428&password=MG24_GAMER_KING_73NT&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_60(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813435&password=MG24_GAMER_KING_BRPO&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_61(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379813559&password=MG24_GAMER_KING_BFM3&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_62(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814432&password=MG24_GAMER_KING_ON9Q&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_63(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814474&password=MG24_GAMER_KING_4NVV&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_64(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814479&password=MG24_GAMER_KING_OGK0&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_65(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814533&password=MG24_GAMER_KING_UK5X&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_66(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814523&password=MG24_GAMER_KING_SQ6Q&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_67(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814748&password=MG24_GAMER_KING_KGJX&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_68(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814764&password=MG24_GAMER_KING_R7MR&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_69(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814813&password=MG24_GAMER_KING_EQUM&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_70(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379814861&password=MG24_GAMER_KING_QPFL&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_71(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815049&password=MG24_GAMER_KING_M4GH&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_72(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815096&password=MG24_GAMER_KING_1JVT&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_73(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815083&password=MG24_GAMER_KING_C94W&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_74(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815127&password=MG24_GAMER_KING_7IEK&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_75(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815292&password=MG24_GAMER_KING_UZ5A&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_76(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815109&password=MG24_GAMER_KING_KTB2&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_77(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815329&password=MG24_GAMER_KING_G4TJ&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_78(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815335&password=MG24_GAMER_KING_7RAV&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_79(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379815591&password=MG24_GAMER_KING_ES3B&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_80(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379816326&password=MG24_GAMER_KING_H1C1&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_81(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379816379&password=MG24_GAMER_KING_PHE5&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_82(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379816369&password=MG24_GAMER_KING_KIM7&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_83(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379816395&password=MG24_GAMER_KING_IOHF&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_84(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817290&password=MG24_GAMER_KING_K7SF&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_85(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817308&password=MG24_GAMER_KING_TKHF&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_86(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817306&password=MG24_GAMER_KING_HYR5&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_87(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817897&password=MG24_GAMER_KING_EE0P&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_88(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817940&password=MG24_GAMER_KING_SM3A&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_89(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818394&password=MG24_GAMER_KING_3BXP&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_90(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818381&password=MG24_GAMER_KING_Z3E5&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_91(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818429&password=MG24_GAMER_KING_34YL&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_92(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818752&password=MG24_GAMER_KING_9805&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_93(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818905&password=MG24_GAMER_KING_6R63&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_94(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818947&password=MG24_GAMER_KING_2U5S&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_95(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379819004&password=MG24_GAMER_KING_IX2J&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_96(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818952&password=MG24_GAMER_KING_ZL4Y&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_97(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818900&password=MG24_GAMER_KING_6R63&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_98(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379818390&password=MG24_GAMER_KING_3BXP&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_99(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817945&password=MG24_GAMER_KING_SM3A&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

def get_player_add_100(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4379817310&password=MG24_GAMER_KING_HYR5&friend_uid={uid}"
        res = requests.get(url)
        return res.json().get('message', 'No message')
    except Exception as e: return f"Error: {e}"

async def send_all_friend_requests_async(target_uid):
    # ১০০টি ফাংশনের মাস্টার লিস্ট
    functions = [
        get_player_add_1, get_player_add_2, get_player_add_3, get_player_add_4, get_player_add_5,
        get_player_add_6, get_player_add_7, get_player_add_8, get_player_add_9, get_player_add_10,
        get_player_add_11, get_player_add_12, get_player_add_13, get_player_add_14, get_player_add_15,
        get_player_add_16, get_player_add_17, get_player_add_18, get_player_add_19, get_player_add_20,
        get_player_add_21, get_player_add_22, get_player_add_23, get_player_add_24, get_player_add_25,
        get_player_add_26, get_player_add_27, get_player_add_28, get_player_add_29, get_player_add_30,
        get_player_add_31, get_player_add_32, get_player_add_33, get_player_add_34, get_player_add_35,
        get_player_add_36, get_player_add_37, get_player_add_38, get_player_add_39, get_player_add_40,
        get_player_add_41, get_player_add_42, get_player_add_43, get_player_add_44, get_player_add_45,
        get_player_add_46, get_player_add_47, get_player_add_48, get_player_add_49, get_player_add_50,
        get_player_add_51, get_player_add_52, get_player_add_53, get_player_add_54, get_player_add_55,
        get_player_add_56, get_player_add_57, get_player_add_58, get_player_add_59, get_player_add_60,
        get_player_add_61, get_player_add_62, get_player_add_63, get_player_add_64, get_player_add_65,
        get_player_add_66, get_player_add_67, get_player_add_68, get_player_add_69, get_player_add_70,
        get_player_add_71, get_player_add_72, get_player_add_73, get_player_add_74, get_player_add_75,
        get_player_add_76, get_player_add_77, get_player_add_78, get_player_add_79, get_player_add_80,
        get_player_add_81, get_player_add_82, get_player_add_83, get_player_add_84, get_player_add_85,
        get_player_add_86, get_player_add_87, get_player_add_88, get_player_add_89, get_player_add_90,
        get_player_add_91, get_player_add_92, get_player_add_93, get_player_add_94, get_player_add_95,
        get_player_add_96, get_player_add_97, get_player_add_98, get_player_add_99, get_player_add_100
    ]

    try:
        loop = asyncio.get_event_loop()
        
        # ThreadPoolExecutor ব্যবহার করে ১০০টি রিকোয়েস্টকে নন-ব্লকিং ভাবে সাজানো
        # max_workers=50 দেওয়া হয়েছে যাতে খুব দ্রুত কাজ শেষ হয়
        with ThreadPoolExecutor(max_workers=50) as executor:
            tasks = [
                loop.run_in_executor(executor, func, target_uid) 
                for func in functions
            ]
            
            # সব রিকোয়েস্ট শেষ হওয়া পর্যন্ত অপেক্ষা (কিন্তু বট ফ্রীজ হবে না)
            results = await asyncio.gather(*tasks)
            
        success_count = len([r for r in results if "Error" not in r])
        return f"Successfully processed {success_count}/100 requests."

    except Exception as e:
        return f"System Error: {str(e)}"

#GET ADD FRIEND
def get_player_remove(uid):
    try:
        url = f"https://danger-add-friend.vercel.app/remove_friend?uid=GUEST_UID&password=YOUR_GUEST_PASSWORD&friend_uid={uid}"
        res = requests.get(url)
        data = res.json()
            # add is inside socialInfo -> signature
        action = data.get('action', 'Unknown')
        status = data.get('status', 'Unknown')
        message = data.get('message', 'No message received')
        if action:
            return message
        else:
            return message
    except Exception as e:
        return f"Error occurred: {e}"
#GET PLAYER BAN STATUS
def get_player_ban_status(uid):
    try:
        url = f"http://amin-team-api.vercel.app/check_banned?player_id={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # status is inside socialInfo -> signature
            status = data.get('status', 'Unknown')
            player_name = data.get('player_name', 'Unknown')
            if status:
                return f"""
 [FFDD00][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[00D1FF]Player Name: {player_name}
Player ID : {xMsGFixinG(uid)} 
Status: {status}
[FFDD00]°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[00FF00][b][c]BOT MADE BY Surjo99exe 
"""
            else:
                return "No ban_status available"
        else:
            return f"Failed to fetch ban_status. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"
#CHAT WITH AI
def talk_with_ai(question):
    url = f"https://princeaiapi.vercel.app/prince/api/v1/ask?key=prince&ask={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "An error occurred while connecting to the server."
#SPAM REQUESTS
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."
####################################

# ** NEW INFO FUNCTION using the new API **
def newinfo(uid):
    # Base URL without parameters
    url = "https://like2.vercel.app/player-info"
    # Parameters dictionary - this is the robust way to do it
    params = {
        'uid': uid,
        'server': server2,  # Hardcoded to bd as requested
        'key': key2
    }
    try:
        # Pass the parameters to requests.get()
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the expected data structure is in the response
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # The API returned 200, but the data is not what we expect (e.g., error message in JSON)
                return {"status": "error", "message": data.get("error", "Invalid ID or data not found.")}
        else:
            # The API returned an error status code (e.g., 404, 500)
            try:
                # Try to get a specific error message from the API's response
                error_msg = response.json().get('error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # If the error response is not JSON
                return {"status": "error", "message": f"API returned status {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., timeout, no connection)
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError: 
        # Handle cases where the response is not valid JSON
        return {"status": "error", "message": "Invalid JSON response from API."}
        
    async def run_spam(chat_type, message, count, uid, chat_id, key, iv):
        try:
            for i in range(count):
                await safe_send_message(chat_type, message, uid, chat_id, key, iv)
                await asyncio.sleep(0.12)
        except Exception as e:
            print("Spam Error:", e)
        
    async def send_title_msg(self, chat_id, key, iv):
        """Build title packet using dictionary structure like GenResponsMsg"""
    
        fields = {
            1: 1,  # type
            2: {   # data
                1: "13777711848",  # uid
                2: str(chat_id),   # chat_id  
                3: f"{{\"TitleID\":{get_random_title()},\"type\":\"Title\"}}",  # title
                4: int(datetime.now().timestamp()),  # timestamp
                5: 0,   # chat_type
                6: "en", # language
                9: {    # field9 - player details
                    1: "[C][B][FF0000] MG24_GAMER",  # Nickname
                    2: await get_random_avatar(),          # avatar_id
                    3: 330,                          # rank
                    4: 102000015,                    # badge
                    5: "MG24_GAMER",                 # Clan_Name
                    6: 1,                            # field10
                    7: 1,                            # global_rank_pos
                    8: {                             # badge_info
                        1: 2                         # value
                    },
                    9: {                             # prime_info
                        1: 8804135237,               # prime_uid
                        2: 8,                        # prime_level
                        3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"  # prime_hex
                    }
                },
                13: {   # field13 - url options
                    1: 2,   # url_type
                    2: 1    # curl_platform
                },
                99: b""  # empty_field
            }
        }

        # **EXACTLY like GenResponsMsg:**
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_length = len(encrypt_packet(packet, key, iv)) // 2
        header_length_final = dec_to_hex(header_length)
    
        # **KEY: Use 0515 for title packets instead of 1215**
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
    
        return bytes.fromhex(final_packet)
        
        

	
#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        # Try alternative API endpoints
        api_urls = [
            f"https://like2.vercel.app/send-like?uid={uid}&server=bd",
            f"https://like2.vercel.app/like?uid={uid}&server=bd",
            f"https://ffviplikeapis.vercel.app/like?uid={uid}&server_name=bd"
        ]
        
        likes_api_response = None
        for url in api_urls:
            try:
                likes_api_response = requests.get(url, timeout=10)
                if likes_api_response.status_code == 200:
                    break
            except:
                continue
        
        if not likes_api_response or likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]⚠️ Likes API Currently Unavailable!

Status: API Service Down
All like API endpoints are experiencing issues:
• ffviplikeapis.vercel.app: 404
• like2.vercel.app: 402
• free-fire-like-api: Connection Error

Please try again later or use other commands.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]Surjo99exe [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]You have already taken likes with this UID.
Try again after 24 hours.

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""
#USERNAME TO insta INFO 
def send_insta_info(username):
    try:
        response = requests.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", timeout=15)
        if response.status_code != 200:
            return f"[B][C][FF0000]❌ Instagram API Error! Status Code: {response.status_code}"

        user = response.json()
        full_name = user.get("full_name", "Unknown")
        followers = user.get("edge_followed_by", {}).get("count") or user.get("followers_count", 0)
        following = user.get("edge_follow", {}).get("count") or user.get("following_count", 0)
        posts = user.get("media_count") or user.get("edge_owner_to_timeline_media", {}).get("count", 0)
        profile_pic = user.get("profile_pic_url_hd") or user.get("profile_pic_url")
        private_status = user.get("is_private")
        verified_status = user.get("is_verified")

        return f"""
[B][C][FB0364]╭[D21A92]─[BC26AB]╮[FFFF00]╔═══════╗
[C][B][FF7244]│[FE4250]◯[C81F9C]֯│[FFFF00]║[FFFFFF]INSTAGRAM_INFO[FFFF00]║
[C][B][FDC92B]╰[FF7640]─[F5066B]╯[FFFF00]╚═══════╝
[C][B][FFFF00]━━━━━━━━━━━━
[C][B][FFFFFF]Name: [66FF00]{full_name}
[C][B][FFFFFF]Username: [66FF00]{username}
[C][B][FFFFFF]Followers: [66FF00]{followers}
[C][B][FFFFFF]Following: [66FF00]{following}
[C][B][FFFFFF]Posts: [66FF00]{posts}
[C][B][FFFFFF]Private: [66FF00]{private_status}
[C][B][FFFFFF]Verified: [66FF00]{verified_status}
[C][B][FFFF00]━━━━━━━━━━━━
"""
    except requests.exceptions.RequestException:
        return "[B][C][FF0000]❌ Instagram API Connection Failed!"
    except Exception as e:
        return f"[B][C][FF0000]❌ Unexpected Error: {str(e)}"

####################################
#CHECK ACCOUNT IS BANNED

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB52"}

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

print(get_random_color())
    
# ---- Random Avatar ----
async def get_random_avatar():
    await asyncio.sleep(0)  # makes it async but instant
    avatar_list = [
        '902050001', '902050002', '902050003', '902039016', '902050004',
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
    return random.choice(avatar_list)
    
async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    """Join team, authenticate chat, perform emote, and leave automatically"""
    try:
        # Step 1: Join the team
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Joined team: {team_code}")
        
        # Wait for team data and chat authentication
        await asyncio.sleep(1.5)  # Increased to ensure proper connection
        
        # Step 2: The bot needs to be detected in the team and authenticate chat
        # This happens automatically in TcPOnLine, but we need to wait for it
        
        # Step 3: Perform emote to target UID
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"🎭 Performed emote {emote_id} to UID {target_uid}")
        
        # Wait for emote to register
        await asyncio.sleep(0.5)
        
        # Step 4: Leave the team
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"🚪 Left team: {team_code}")
        
        return True, f"Quick emote attack completed! Sent emote to UID {target_uid}"
        
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"
        
        
def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    # User-Agent rotation
    user_agents = [
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
    ]
    
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": random.choice(user_agents),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                print(f"DEBUG: GeNeRaTeAccEss failed with status {response.status}")
                return None, None
            try:
                data = await response.json()
                open_id = data.get("open_id")
                access_token = data.get("access_token")
                if open_id and access_token:
                    return open_id, access_token
                else:
                    print(f"DEBUG: Missing open_id or access_token in response: {data}")
                    return None, None
            except Exception as e:
                print(f"DEBUG: Failed to parse JSON response: {e}")
                return None, None

def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.120.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(TypE, PacKeT):
    global online_writer, whisper_writer
    try:
        if TypE == 'ChaT':
            if whisper_writer:
                whisper_writer.write(PacKeT)
                await whisper_writer.drain()
                return True
            else:
                print("❌ whisper_writer is None! Cannot send message.")
                return False
        elif TypE == 'OnLine':
            if online_writer:
                online_writer.write(PacKeT)
                await online_writer.drain()
                return True
            else:
                print("❌ online_writer is None! Cannot send packet.")
                return False
        else:
            print(f"❌ Unsupported Type: {TypE}")
            return False
    except Exception as e:
        print(f"❌ Error in SEndPacKeT ({TypE}): {e}")
        return False

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Safely send message with retry mechanism"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            result = await SEndPacKeT('ChaT', P)
            if result:
                print(f"✅ Message sent successfully on attempt {attempt + 1}")
                return True
            else:
                print(f"❌ SEndPacKeT returned False on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(0.5)
        except Exception as e:
            print(f"❌ Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Wait before retry
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    """Fast emote spam function that sends emotes rapidly"""
    global fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times
    
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT('OnLine', H)
            except Exception as e:
                print(f"Error in fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # 0.1 seconds interval between spam cycles

# NEW FUNCTION: Custom emote spam with specified times
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    """Custom emote spam function that sends emotes specified number of times"""
    global custom_spam_running
    count = 0
    
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT('OnLine', H)
            count += 1
            await asyncio.sleep(0.1)  # 0.1 seconds interval between emotes
        except Exception as e:
            print(f"Error in custom_emote_spam for uid {uid}: {e}")
            break

# NEW FUNCTION: Faster spam request loop - Sends exactly 30 requests quickly
async def spam_request_loop_with_cosmetics(target_uid, key, iv, region):
    """Spam request function with cosmetics - using your same structure"""
    global spam_request_running
    
    count = 0
    max_requests = 30
    
    # Different badge values to rotate through
    badge_rotation = [1048576, 32768, 2048, 64, 4094, 11233, 262144]
    
    while spam_request_running and count < max_requests:
        try:
            # Rotate through different badges
            current_badge = badge_rotation[count % len(badge_rotation)]
            
            # Create squad (same as before)
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT('OnLine', PAc)
            await asyncio.sleep(0.2)
            
            # Change squad size (same as before)
            C = await cHSq(5, int(target_uid), key, iv, region)
            await SEndPacKeT('OnLine', C)
            await asyncio.sleep(0.2)
            
            # Send invite WITH COSMETICS (enhanced version)
            V = await SEnd_InV_With_Cosmetics(5, int(target_uid), key, iv, region, current_badge)
            await SEndPacKeT('OnLine', V)
            
            # Leave squad (same as before)
            E = await ExiT(None, key, iv)
            await SEndPacKeT('OnLine', E)
            
            count += 1
            print(f"✅ Sent cosmetic invite #{count} to {target_uid} with badge {current_badge}")
            
            # Short delay
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Error in cosmetic spam: {e}")
            await asyncio.sleep(0.5)
    
    return count
            


# NEW FUNCTION: Evolution emote spam with mapping
async def evo_emote_spam(uids, number, key, iv, region):
    """Send evolution emotes based on number mapping"""
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT('OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending evo emote to {uid}: {e}")
        
        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    
    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"

# NEW FUNCTION: all emote spam with mapping
async def play_emote_spam(uids, number, key, iv, region):
    """Send all emotes based on number mapping"""
    try:
        emote_id = ALL_EMOTE.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-410 only."
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT('OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending play emote to {uid}: {e}")
        
        return True, f"Sent playlution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    
    except Exception as e:
        return False, f"Error in play_emote_spam: {str(e)}"

# NEW FUNCTION: Fast evolution emote spam
async def evo_fast_emote_spam(uids, number, key, iv, region):
    """Fast evolution emote spam function"""
    global evo_fast_spam_running
    count = 0
    max_count = 25  # Spam 25 times
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT('OnLine', H)
            except Exception as e:
                print(f"Error in evo_fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed fast evolution emote spam {count} times"

# NEW FUNCTION: Custom evolution emote spam with specified times
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    """Custom evolution emote spam with specified repeat times"""
    global evo_custom_spam_running
    count = 0
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT('OnLine', H)
            except Exception as e:
                print(f"Error in evo_custom_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed custom evolution emote spam {count} times"
    

async def ArohiAccepted(uid,code,K,V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
            2: 161,
            4: "y[WW",
            6: 11,
            8: "1.114.18",
            9: 3,
            10: 1
            },
            10: str(code),
        }
        }
    return GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)

async def TcPOnLine(ip, port, key, iv, AutHToKen, uid, timestamp, reconnect_delay=5):
    global online_writer, last_status_packet, status_response_cache, insquad, joining_team, whisper_writer, region, auto_join_enabled
    
    if insquad is not None:
        insquad = None
    if joining_team is True:
        joining_team = False
    
    online_writer = None
    
    while True:
        try:
            print(f"Attempting to connect to {ip}:{port}...")
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            
            # Enable TCP keepalive on the socket (basic only)
            try:
                sock = writer.get_extra_info('socket')
                if sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    print("TCP keepalive enabled.")
            except Exception as e:
                print(f"Could not set TCP keepalive: {e}")
            
            # --- SIMPLIFIED CONNECTION (like TcPChaT) ---
            # Just send token and enter read loop, skip complex handshake
            try:
                bytes_payload = bytes.fromhex(AutHToKen)
                online_writer.write(bytes_payload)
                await online_writer.drain()
                print("Token sent (simplified).")
            except Exception as e:
                print(f"Token error: {e}")
                raise

            # Enter read loop immediately (like TcPChaT)
            # Bot is now monitoring for invites and commands
            
            try:
                while True:
                    data2 = await reader.read(4096)
                    if not data2:
                        break
                    
                    # Auto-join team when invited (detect invite packet)
                    data_hex = data2.hex()
                    try:
                        # Try multiple methods to detect invite
                        is_invite = False
                        sender_uid = None
                        
                        # Method 1: Try sQ_pb2 protobuf parsing
                        try:
                            from Pb2 import sQ_pb2
                            invite_msg = sQ_pb2.sq()
                            invite_msg.ParseFromString(data2)
                            
                            packet_type = getattr(invite_msg, 'type', None)
                            
                            if packet_type is not None:
                                # Check for invite packet (type 33)
                                if packet_type == 33 and auto_join_enabled:
                                    is_invite = True
                                    print(f"🎯 TEAM INVITE DETECTED! Type: {packet_type}")
                                    
                                    # Extract sender UID
                                    if hasattr(invite_msg, 'data') and invite_msg.data:
                                        try:
                                            inner_data = invite_msg.data
                                            if hasattr(inner_data, 'uid'):
                                                sender_uid = inner_data.uid
                                        except:
                                            pass
                        except:
                            pass
                        
                        # Method 2: Try Team_msg_pb2
                        if not is_invite:
                            try:
                                from Pb2 import Team_msg_pb2
                                team_msg = Team_msg_pb2.GenTeamWhisper()
                                team_msg.ParseFromString(data2)
                                
                                team_type = getattr(team_msg, 'type', None)
                                if team_type == 33 and auto_join_enabled:
                                    is_invite = True
                                    print(f"🎯 TEAM INVITE via Team_msg!")
                            except:
                                pass
                        
                        # If invite detected, auto-join
                        if is_invite and auto_join_enabled:
                            print(f"[AUTO JOIN] Joining team...")
                            
                            join_packet = await GenJoinSquadsPacket("", key, iv)
                            if online_writer and not online_writer.is_closing():
                                await SEndPacKeT('OnLine', join_packet)
                                print(f"✅ Auto-joined team!")
                                
                                insquad = sender_uid if sender_uid else True
                                joining_team = False
                                
                                try:
                                    if sender_uid:
                                        await auto_rings_emote_dual(sender_uid, key, iv, region)
                                except:
                                    pass
                    except:
                        pass
                        
            except Exception as e:
                print(f"Read loop error: {e}")
                
            if online_writer is not None:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
            
            insquad = None
            joining_team = False
            
            print(f"Connection closed. Reconnecting in {reconnect_delay} seconds...")
            await asyncio.sleep(reconnect_delay)

        except ConnectionRefusedError:
            print(f"Connection refused to {ip}:{port}. Retrying...")
            await asyncio.sleep(reconnect_delay)
        except asyncio.TimeoutError:
            print(f"Connection timeout to {ip}:{port}. Retrying...")
            await asyncio.sleep(reconnect_delay)
        except Exception as e:
            print(f"Unexpected error in TcPOnLine: {e}")
            await asyncio.sleep(reconnect_delay)
                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task, auto_accept_invite
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            
            while True:
                try:
                    data = await reader.read(9999)
                except Exception as e:
                    print(f"Error reading data: {e}")
                    break
                
                if not data: break
                
                # AUTO-ACCEPT INVITATION LOGIC
                if auto_accept_invite and data.hex().startswith("0800"):
                    try:
                        # Parse invitation packet
                        msg_data = DeCode_PackEt(data.hex()[8:])
                        if msg_data and '"1": 2' in msg_data:
                            # Extract inviter UID from packet
                            packet_json = json.loads(msg_data)
                            if '2' in packet_json and '1' in packet_json.get('2', {}):
                                inviter_uid = packet_json['2']['1']['data']
                                print(f"[AUTO-ACCEPT] Invitation received from: {inviter_uid}")
                                
                                # Send accept packet
                                await asyncio.sleep(auto_accept_delay)
                                accept_packet = await GenJoinSquadsPacket(str(inviter_uid), key, iv)
                                if whisper_writer:
                                    whisper_writer.write(accept_packet)
                                    await whisper_writer.drain()
                                    print(f"[AUTO-ACCEPT] Automatically joined squad of: {inviter_uid}")
                    except Exception as e:
                        print(f"[AUTO-ACCEPT] Error processing invitation: {e}")
                
                if data.hex().startswith("120000"):

                    msg = DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        
                        # Debug print to see what we're receiving
                        print(f"Received message: {inPuTMsG} from UID: {uid} in chat type: {XX}")
                        
                    except:
                        response = None


                    if response:
                        # ALL COMMANDS NOW WORK IN ALL CHAT TYPES (SQUAD, GUILD, PRIVATE)
                        
                        # AI Command - /ai
                        if inPuTMsG.strip().startswith('/ai '):
                            print('Processing AI command in any chat type')
                            
                            question = inPuTMsG[4:].strip()
                            if question:
                                initial_message = f"[B][C]{get_random_color()}\n🤖 AI is thinking...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    ai_response = await loop.run_in_executor(executor, talk_with_ai, question)
                                
                                # Format the AI response
                                ai_message = f"""
[B][C][00FF00]🤖 AI Response:

[00FFFF]{ai_response}

[C][B][FFB300]Question: [FFFFFF]{question}
"""
                                await safe_send_message(response.Data.chat_type, ai_message, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Please provide a question after /ai\nExample: /ai What is Free Fire?\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Likes Command - /likes
                        if inPuTMsG.strip().startswith('/likes '):
                            print('Processing likes command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /likes (uid)\nExample: /likes 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending 100 likes to {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    likes_result = await loop.run_in_executor(executor, send_likes, target_uid)
                                
                                await safe_send_message(response.Data.chat_type, likes_result, uid, chat_id, key, iv)
                                
                                #TEAM SPAM MESSAGE COMMAND
                        if inPuTMsG.strip().startswith('/ms '):
                            print('Processing /ms command')
                            
                            # Send confirmation that command was received
                            await safe_send_message(response.Data.chat_type, "[B][C][00FF00]🚀 Starting message spam...", uid, chat_id, key, iv)

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/ms <message>\n"
                                        "Example: /ms Surjo99exe"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()

                                    for _ in range(30):
                                        color = get_random_color()  # random color from your list
                                        colored_message = f"[B][C]{color} {user_message}"  # correct format
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)
                                    
                                    # Send completion message
                                    await safe_send_message(response.Data.chat_type, "[B][C][00FF00]✅ Message spam completed!", uid, chat_id, key, iv)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #GALI SPAM MESSAGE 
                        if inPuTMsG.strip().startswith('/gali '):
                            print('Processing /gali command')
                            
                            # Send confirmation that command was received
                            await safe_send_message(response.Data.chat_type, "[B][C][00FF00]🔥 Starting gali spam...", uid, chat_id, key, iv)

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/gali <name>\n"
                                        "Example: /gali hater"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()

                                    messages = [
                                        "{Name} খান🤫কির ছেলে !!",
                                        "{Name} মাদার চো🤫দ, তোর মা🤫কে চু🤫দি !!",
                                        "{Name} মাদার চো🤫দ, তোর মা🤫কে 5G স্পিডে চু🤫দি !!",
                                        "{Name} বোকাচো🤫দা, তোর মা🤫কে কন🤫ডম লাগিয়ে চু🤫দি !!",
                                        "{Name} বোকাচো🤫দা, তোর মা🤫কে প্রতিদিন ১০,০০০ টাকার সার্ভিস দেই !!",
                                        "F🤫U🤫C🤫K {Name} !!",
                                        "{Name} মাদার চো🤫দ, পো🤫দ মে🤫রে দিবো !!",
                                        "{Name} মাদার চো🤫দ !!",
                                        "{Name} খান🤫কি, আমি তোর বা🤫প !!",
                                        "{Name} তোর মা🤫কে আমি চু🤫ই🤫দা তোরে জন্মায় ছি !!",
                                        "{Name} বোকাচো🤫দা, খান🤫কির ছেলে !!",
                                        "{Name} মাদার চো🤫দ, তোর মা🤫কে ১৮০ কি.মি. স্পিডে চু🤫দি !!",
                                        "{Name} খা🤫ন🤫কির ছেলে বট, নুব🤫রা প্লেয়ার !!",
                                        "বাংলাদেশের NO-1 বট PLAYER {Name}",
                                        "{Name} জুতা চোর !!",
                                        "{Name} মাদারচো🤫দ, ফ্রি ফায়ার খেলা বাদ দিয়ে লুডু খেল যা !!",
                                        "{Name} যাই করিস, আমি তোর অব্বা এইডা কখনো ভুলিস না !!"
            ]

                                    # Send each message one by one with random color
                                    for msg in messages:
                                        colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.upper())}"
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)
                                    
                                    # Send completion message
                                    await safe_send_message(response.Data.chat_type, "[B][C][00FF00]✅ Gali spam completed!", uid, chat_id, key, iv)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #INSTA USERNAME TO INFO-/ig
                        if inPuTMsG.strip().startswith('/ig '):
                            print('Processing insta command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ig <username>\nExample: /ig virat.kohli\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_username = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching Instagram info for {target_username}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
        # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    insta_result = await loop.run_in_executor(executor, send_insta_info, target_username)
        
                                await safe_send_message(response.Data.chat_type, insta_result, uid, chat_id, key, iv)

                                #GET PLAYER BIO-/bio
                        if inPuTMsG.strip().startswith('/bio '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /bio <uid>\nExample: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching the player bio...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    bio_result = await loop.run_in_executor(executor, get_player_bio, target_uid)

                                await safe_send_message(response.Data.chat_type, f"[B][C]{get_random_color()}\n{bio_result}", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/rejectmsg '):
                            print('Processing rejectmsg command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /rejectmsg <uid>\nExample: /rejectmsg 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending reject message...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                try:
                                    inv_packet = await RejectMSGtaxt(target_uid, uid, key, iv)
                                    await SEndPacKeT('OnLine', inv_packet)
                                    success_msg = f"[B][C][00FF00]✅ Reject message sent to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        #GET PLAYER LIKE
                        if inPuTMsG.strip().startswith('/like '):
                            print('Processing like command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /like <uid>\nExample: /like 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending Likes...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    like_result = await loop.run_in_executor(executor, send_likes, target_uid)

                                await safe_send_message(response.Data.chat_type, like_result, uid, chat_id, key, iv)

                                #GET PLAYER basic-/info
                        if inPuTMsG.strip().startswith('/info '):
                            print('Processing basic command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /info <uid>\nExample: /info 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching the player info...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    basic_result = await loop.run_in_executor(executor, get_player_basic, target_uid)
                                await safe_send_message(response.Data.chat_type, f"\n{basic_result}\n", uid, chat_id, key, iv)

                                #GET PLAYER ADD FRIEND
                        if inPuTMsG.strip().startswith('/add '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /add <uid>"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}🚀 Sending Friend Requests..."
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # ১০০টি রিকোয়েস্ট একসাথে পাঠানোর জন্য মাস্টার ফাংশন কল
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    # এখানে send_all_friend_requests কল করা হচ্ছে
                                    final_result = await loop.run_in_executor(executor, get_player_add, target_uid)

                                await safe_send_message(response.Data.chat_type, f"\n[B][C][00FF00]✅ {final_result}\n", uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/spam_req '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /spam_req <uid>"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}🚀 Sending 100 Friend Requests to: {target_uid}..."
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                try:
                                    # এটি ব্যাকগ্রাউন্ডে ১০০টি রিকোয়েস্ট প্রসেস করবে এবং বট ফ্রীজ হবে না
                                    final_result = await send_all_friend_requests_async(target_uid)
                                    
                                    success_msg = f"\n[B][C][00FF00]✅ {final_result}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Error: {str(e)}", uid, chat_id, key, iv)


                                #GET PLAYER REMOVE FRIEND
                        if inPuTMsG.strip().startswith('/remove '):
                            print('Processing add command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /remove <uid>\nExample: /remove 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Removeing Friend Request ..."
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    remove_result = await loop.run_in_executor(executor, get_player_remove, target_uid)
                                await safe_send_message(response.Data.chat_type, f"\n{remove_result}\n", uid, chat_id, key, iv)

                                initial_message = f"[B][C]{get_random_color()}Friend REMOVED !!"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                #GET PLAYER BAN STATUS
                        if inPuTMsG.strip().startswith('/check '):
                            print('Processing ban_status command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /check <uid>\nExample: /check 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nFetching the player ban status...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    ban_status_result = await loop.run_in_executor(executor, get_player_ban_status, target_uid)
                                await safe_send_message(response.Data.chat_type, f"\n{ban_status_result}\n", uid, chat_id, key, iv)

                        # QUICK EMOTE ATTACK COMMAND - /quick [team_code] [emote_id] [target_uid?]
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Processing quick emote attack command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /quick (team_code) [emote_id] [target_uid]\n\n[FFFFFF]Examples:\n[00FF00]/quick ABC123[FFFFFF] - Join, send Rings emote, leave\n[00FF00]/ghostquick ABC123[FFFFFF] - Ghost join, send emote, leave\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
        
                                # Set default values
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)  # Default: Sender's UID
        
                                # Parse optional parameters
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
        
                                # Determine target name for message
                                if target_uid == str(response.Data.uid):
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {target_uid}"
        
                                initial_message = f"[B][C][FFFF00]⚡ QUICK EMOTE ATTACK!\n\n[FFFFFF]🎯 Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n[FFFFFF]⏱️ Estimated: [00FF00]2 seconds\n\n[FFFF00]Executing sequence...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try regular method first
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
            
                                    if success:
                                        success_message = f"[B][C][00FF00]✅ QUICK ATTACK SUCCESS!\n\n[FFFFFF]🏷️ Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n\n[00FF00]Bot joined → emoted → left! ✅\n"
                                    else:
                                        success_message = f"[B][C][FF0000]❌ Regular attack failed: {result}\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print("failed")
            
                        if inPuTMsG.startswith('noob'):
                            await handle_alll_titles_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)


# ================= BUNDLE COMMAND START =================
   # ================= FINAL BUNDLE COMMAND (FAST) =================
                        if inPuTMsG.strip().startswith('/bundle'):
                            print('Processing bundle command')
    
                            parts = inPuTMsG.strip().split()
                            
                            if len(parts) < 2:
                                # Show available bundles
                                bundle_list = """[B][C][00FF00]🎁 AVAILABLE BUNDLES 🎁
[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[FFFFFF]• midnight
[FFFFFF]• aurora
[FFFFFF]• naruto  
[FFFFFF]• paradox
[FFFFFF]• frostfire
[FFFFFF]• rampage
[FFFFFF]• cannibal
[FFFFFF]• devil
[FFFFFF]• scorpio
[FFFFFF]• dreamspace
[FFFFFF]• itachi
[FF6347]━[32CD32]━[7B68EE]━[FF4500]━[1E90FF]━[ADFF2F]━[FF69B4]━[8A2BE2]━[DC143C]━[FF8C00]━[BA55D3]━[7CFC00]━[FFC0CB]
[00FF00]Usage: /bundle [name]
[FFFFFF]Example: /bundle midnight"""
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle_name = parts[1].lower()
        
                                # All bundles use the same ID: 914000002
                                bundle_id = BUNDLE.get(bundle_name)
        
                                initial_msg = f"[B][C][00FF00]🎁 Sending {bundle_name}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Create bundle packet
                                    bundle_packet = await bundle_packet_async(bundle_id, key, iv, region)
            
                                    if bundle_packet and online_writer:
                                        await SEndPacKeT('OnLine', bundle_packet)
                                        success_msg = f"[B][C][00FF00]✅ Done: {bundle_name}"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ Failed to create bundle packet!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Error sending bundle: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # ===============================================================

                        # Invite Command - /inv (creates 5-player group and sends request)
                        if inPuTMsG.strip().startswith('/inv '):
                            print('Processing invite command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /inv (uid)\nExample: /inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nCreating 5-Player Group and sending request to {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:

                                    V = await SEnd_InV(4, int(target_uid), key, iv, region)
                                    await SEndPacKeT('OnLine', V)
                                    await asyncio.sleep(0.3)

                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Player Group invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending invite: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)


                        if inPuTMsG.startswith(("/6")):
                            # Process /6 command - Create 4 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 6-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 4 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT('OnLine', PAc)
                            
                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT('OnLine', C)
                            
                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT('OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT('OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        # KICK COMMAND - /kick [uid]
                        if inPuTMsG.strip().startswith('/kick'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /kick <uid>"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                try:
                                    kick_packet = await send_kick_packet(target_uid, key, iv, region)
                                    await SEndPacKeT('OnLine', kick_packet)
                                    success_msg = f"[B][C][00FF00]✅ Kicked member: {target_uid}"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Kick Error: {str(e)}", uid, chat_id, key, iv)

                        # LEAVE COMMAND - /leave
                        if inPuTMsG.strip() == '/leave':
                            try:
                                leave_packet = await ExiT(None, key, iv)
                                await SEndPacKeT('OnLine', leave_packet)
                                success_msg = f"[B][C][00FF00]✅ Bot left the group!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            except Exception as e:
                                await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Leave Error: {str(e)}", uid, chat_id, key, iv)

                        # START COMMAND - /start
                        if inPuTMsG.strip() == '/start':
                            try:
                                start_packet = await send_start_packet(key, iv, region)
                                await SEndPacKeT('OnLine', start_packet)
                                success_msg = f"[B][C][00FF00]✅ Match started!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            except Exception as e:
                                await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Start Error: {str(e)}", uid, chat_id, key, iv)

                        # HELP COMMAND - /help
                        if inPuTMsG.strip() == '/help':
                            help_msg = """[B][C][00FF00]🤖 BOT COMMANDS HELP 🤖
[FFFFFF]
[FFD700]━━━[FF0000] GAME COMMANDS [FF0000]━━━[FFD700]
[00FFFF]/kick [uid] [FFFFFF]- Kick squad member
[00FFFF]/leave [FFFFFF]- Leave squad
[00FFFF]/start [FFFFFF]- Start match
[00FFFF]/autoaccept [FFFFFF]- Toggle auto-accept invites
[FFFFFF]
[FFD700]━━━[FF0000] EMOTES & ANIMATIONS [FF0000]━━━[FFD700]
[00FFFF]/evo [1-18] [FFFFFF]- Standard emotes
[00FFFF]/emote [1-363] [FFFFFF]- All emotes
[00FFFF]/dance [1-8] [FFFFFF]- Dance emotes
[00FFFF]/rare [1-12] [FFFFFF]- Rare collection
[00FFFF]/legend [1-10] [FFFFFF]- Legendary emotes
[00FFFF]/vip [1-8] [FFFFFF]- VIP exclusive
[00FFFF]/weapon [name] [FFFFFF]- Weapon showcase
[00FFFF]/victory [1-8] [FFFFFF]- Victory dances
[00FFFF]/pet [1-8] [FFFFFF]- Pet showcase
[00FFFF]/vehicle [1-6] [FFFFFF]- Vehicle emotes
[00FFFF]/graffiti [1-6] [FFFFFF]- Spray paints
[00FFFF]/rainbow [FFFFFF]- Rainbow animation
[00FFFF]/flash [FFFFFF]- Flash animation
[00FFFF]/super [id] [count] [FFFFFF]- Emote spam
[FFFFFF]
[FFD700]━━━[FF0000] GAME STRATEGY & INFO [FF0000]━━━[FFD700]
[00FFFF]/callout [type] [FFFFFF]- Quick callouts
[00FFFF]/loadout [type] [FFFFFF]- Team loadouts
[00FFFF]/rank [tier] [FFFFFF]- Rank push tips
[00FFFF]/mode [type] [FFFFFF]- Game modes info
[00FFFF]/drop [location] [FFFFFF]- Drop locations
[00FFFF]/scrim [mode] [FFFFFF]- Tournament setup
[00FFFF]/char [name] [FFFFFF]- Character skills
[00FFFF]/weaponstats [name] [FFFFFF]- Weapon stats
[00FFFF]/strategy [type] [FFFFFF]- Game strategies
[FFFFFF]
[FFD700]━━━[FF0000] UTILITY COMMANDS [FF0000]━━━[FFD700]
[00FFFF]/ai [question] [FFFFFF]- Ask AI anything
[00FFFF]/likes [uid] [FFFFFF]- Send 100 likes
[00FFFF]/like [uid] [FFFFFF]- Send likes
[00FFFF]/bio [uid] [FFFFFF]- Get player bio
[00FFFF]/info [uid] [FFFFFF]- Get player info
[00FFFF]/check [uid] [FFFFFF]- Check ban status
[00FFFF]/add [uid] [FFFFFF]- Add friend
[00FFFF]/remove [uid] [FFFFFF]- Remove friend
[00FFFF]/ig [username] [FFFFFF]- Instagram info
[00FFFF]/ms [msg] [FFFFFF]- Message spam
[00FFFF]/bundle [name] [FFFFFF]- Send bundle
[00FFFF]/inv [uid] [FFFFFF]- Invite player
[00FFFF]/3 [FFFFFF]- Create 3-player group
[00FFFF]/6 [FFFFFF]- Create 6-player group
[FFFFFF]
[00FF00]✨ Type /emotes for full emote categories!
[00FF00]✨ Type any command without args for help!"""
                            await safe_send_message(response.Data.chat_type, help_msg, uid, chat_id, key, iv)

                        # EMOTES LIST COMMAND - /emotes
                        if inPuTMsG.strip() == '/emotes':
                            await safe_send_message(response.Data.chat_type, EMOTE_CATEGORIES, uid, chat_id, key, iv)

                        # RARE EMOTES - /rare [1-12]
                        if inPuTMsG.strip().startswith('/rare'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                rare_list = "[B][C][00FF00]💎 RARE EMOTES 💎\n[FFFFFF]1-Rare AK, 2-Rare SCAR, 3-Rare MP40, 4-Rare M1014\n5-Rare XM8, 6-Rare UMP, 7-Rare M1887, 8-Rare Groza\n9-Rare M4A1, 10-Rare Thompson, 11-Rare P90, 12-Rare Woodpecker\n[00FFFF]Usage: /rare [1-12]"
                                await safe_send_message(response.Data.chat_type, rare_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    rare_id = parts[1]
                                    if rare_id in RARE_EMOTES:
                                        emote_id = int(RARE_EMOTES[rare_id])
                                        from xC4 import Emote_k
                                        rare_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', rare_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][00FF00]💎 Rare emote {rare_id} performed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid rare ID! Use 1-12", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Rare emote error: {str(e)}", uid, chat_id, key, iv)

                        # LEGENDARY EMOTES - /legend [1-10]
                        if inPuTMsG.strip().startswith('/legend'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                legend_list = "[B][C][FFD700]👑 LEGENDARY EMOTES 👑\n[FFFFFF]1-Legend AK, 2-Legend SCAR, 3-Legend MP40, 4-Legend M1887\n5-Legend Groza, 6-Legend M4A1, 7-Legend P90, 8-Legend AWM\n9-Legend Desert Eagle, 10-Legend AN94\n[00FFFF]Usage: /legend [1-10]"
                                await safe_send_message(response.Data.chat_type, legend_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    legend_id = parts[1]
                                    if legend_id in LEGEND_EMOTES:
                                        emote_id = int(LEGEND_EMOTES[legend_id])
                                        from xC4 import Emote_k
                                        legend_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', legend_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][FFD700]👑 Legendary emote {legend_id} performed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid legend ID! Use 1-10", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Legend emote error: {str(e)}", uid, chat_id, key, iv)

                        # VIP EMOTES - /vip [1-8]
                        if inPuTMsG.strip().startswith('/vip'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                vip_list = "[B][C][9400D3]🔥 VIP EXCLUSIVE EMOTES 🔥\n[FFFFFF]1-VIP Exclusive 1, 2-VIP Exclusive 2, 3-VIP Exclusive 3\n4-VIP Exclusive 4, 5-VIP Exclusive 5, 6-VIP Exclusive 6\n7-VIP Exclusive 7, 8-VIP Exclusive 8\n[00FFFF]Usage: /vip [1-8]"
                                await safe_send_message(response.Data.chat_type, vip_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    vip_id = parts[1]
                                    if vip_id in VIP_EMOTES:
                                        emote_id = int(VIP_EMOTES[vip_id])
                                        from xC4 import Emote_k
                                        vip_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', vip_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][9400D3]🔥 VIP emote {vip_id} performed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid VIP ID! Use 1-8", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ VIP emote error: {str(e)}", uid, chat_id, key, iv)

                        # WEAPON EMOTES - /weapon [name]
                        if inPuTMsG.strip().startswith('/weapon'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                weapon_list = "[B][C][1E90FF]🔫 WEAPON SHOWCASE EMOTES 🔫\n[FFFFFF]ak, scar, mp40, mp40_2, m1014, m1014_2, xm8, famas\nump, m1887, woodpecker, groza, m4a1, thompson\ng18, parafal, p90, m60, awm, desert_eagle\nan94, mp5, vector, sks, m14, sniper\n[00FFFF]Usage: /weapon ak"
                                await safe_send_message(response.Data.chat_type, weapon_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    weapon_name = parts[1].lower()
                                    if weapon_name in WEAPON_EMOTES:
                                        emote_id = int(WEAPON_EMOTES[weapon_name])
                                        from xC4 import Emote_k
                                        weapon_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', weapon_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][1E90FF]🔫 {weapon_name.upper()} emote performed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid weapon name! Type /weapon for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Weapon emote error: {str(e)}", uid, chat_id, key, iv)

                        # VICTORY EMOTES - /victory [1-8]
                        if inPuTMsG.strip().startswith('/victory'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                victory_list = "[B][C][FFD700]🏆 VICTORY EMOTES 🏆\n[FFFFFF]1-Victory Dance 1, 2-Victory Dance 2, 3-Victory Dance 3\n4-Victory Dance 4, 5-Victory Dance 5, 6-Victory Dance 6\n7-Victory Dance 7, 8-Victory Dance 8\n[00FFFF]Usage: /victory [1-8]"
                                await safe_send_message(response.Data.chat_type, victory_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    victory_id = parts[1]
                                    if victory_id in VICTORY_EMOTES:
                                        emote_id = int(VICTORY_EMOTES[victory_id])
                                        from xC4 import Emote_k
                                        victory_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', victory_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][FFD700]🏆 Victory emote {victory_id} performed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid victory ID! Use 1-8", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Victory emote error: {str(e)}", uid, chat_id, key, iv)

                        # PET EMOTES - /pet [1-8]
                        if inPuTMsG.strip().startswith('/pet'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                pet_list = "[B][C][FF69B4]🐾 PET SHOWCASE EMOTES 🐾\n[FFFFFF]1-Kitty, 2-Puppy, 3-Panda, 4-Robot\n5-Dragon, 6-Eagle, 7-Tiger, 8-Fox\n[00FFFF]Usage: /pet [1-8]"
                                await safe_send_message(response.Data.chat_type, pet_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    pet_id = parts[1]
                                    if pet_id in PET_EMOTES:
                                        emote_id = int(PET_EMOTES[pet_id])
                                        from xC4 import Emote_k
                                        pet_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', pet_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][FF69B4]🐾 Pet {pet_id} showcased!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid pet ID! Use 1-8", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Pet emote error: {str(e)}", uid, chat_id, key, iv)

                        # VEHICLE EMOTES - /vehicle [1-6]
                        if inPuTMsG.strip().startswith('/vehicle'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                vehicle_list = "[B][C][1E90FF]🚗 VEHICLE EMOTES 🚗\n[FFFFFF]1-SUV, 2-Sports Car, 3-Monster Truck\n4-Motorcycle, 5-Jeep, 6-Tuk-Tuk\n[00FFFF]Usage: /vehicle [1-6]"
                                await safe_send_message(response.Data.chat_type, vehicle_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    vehicle_id = parts[1]
                                    if vehicle_id in VEHICLE_EMOTES:
                                        emote_id = int(VEHICLE_EMOTES[vehicle_id])
                                        from xC4 import Emote_k
                                        vehicle_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', vehicle_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][1E90FF]🚗 Vehicle {vehicle_id} showcased!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid vehicle ID! Use 1-6", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Vehicle emote error: {str(e)}", uid, chat_id, key, iv)

                        # GRAFFITI/SPRAY EMOTES - /graffiti [1-6]
                        if inPuTMsG.strip().startswith('/graffiti'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                graffiti_list = "[B][C][FF8C00]🎨 GRAFFITI SPRAYS 🎨\n[FFFFFF]1-Crown, 2-Skull, 3-Fire\n4-Heart, 5-GG, 6-Boss\n[00FFFF]Usage: /graffiti [1-6]"
                                await safe_send_message(response.Data.chat_type, graffiti_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    graffiti_id = parts[1]
                                    if graffiti_id in GRAFFITI_SPRAYS:
                                        emote_id = int(GRAFFITI_SPRAYS[graffiti_id])
                                        from xC4 import Emote_k
                                        graffiti_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', graffiti_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][FF8C00]🎨 Graffiti {graffiti_id} sprayed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid graffiti ID! Use 1-6", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Graffiti error: {str(e)}", uid, chat_id, key, iv)

                        # GAME CALLOUTS - /callout [type]
                        if inPuTMsG.strip().startswith('/callout'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                callout_list = """[B][C][FF0000]📢 QUICK GAME CALLOUTS 📢
[FFFFFF]
[00FFFF]enemy [FFFFFF]- ⚠️ ENEMY SPOTTED!
[00FFFF]backup [FFFFFF]- 🆘 NEED BACKUP!
[00FFFF]help [FFFFFF]- 📢 NEED HELP!
[00FFFF]rush [FFFFFF]- ⚡ RUSH! RUSH! RUSH!
[00FFFF]camp [FFFFFF]- 🎯 CAMP HERE!
[00FFFF]loot [FFFFFF]- 💰 LOOT HERE!
[00FFFF]medic [FFFFFF]- 🏥 NEED MEDIC!
[00FFFF]ammo [FFFFFF]- 🔫 NEED AMMO!
[00FFFF]thanks [FFFFFF]- 🙏 THANKS!
[00FFFF]gg [FFFFFF]- 🏆 GG! WELL PLAYED!
[FFFFFF]Usage: /callout enemy"""
                                await safe_send_message(response.Data.chat_type, callout_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    callout_type = parts[1].lower()
                                    if callout_type in GAME_CALLOUTS:
                                        callout_msg = GAME_CALLOUTS[callout_type]
                                        await safe_send_message(response.Data.chat_type, callout_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid callout! Type /callout for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Callout error: {str(e)}", uid, chat_id, key, iv)

                        # TEAM LOADOUTS - /loadout [type]
                        if inPuTMsG.strip().startswith('/loadout'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                loadout_list = """[B][C][00FF00]🎒 TEAM LOADOUTS 🎒
[FFFFFF]
[00FFFF]sniper [FFFFFF]- 🎯 Sniper Setup
[00FFFF]rusher [FFFFFF]- ⚡ Rusher Setup
[00FFFF]support [FFFFFF]- 🛡️ Support Setup
[00FFFF]assault [FFFFFF]- 🔫 Assault Setup
[FFFFFF]Usage: /loadout sniper"""
                                await safe_send_message(response.Data.chat_type, loadout_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    loadout_type = parts[1].lower()
                                    if loadout_type in LOADOUTS:
                                        loadout_msg = LOADOUTS[loadout_type]
                                        await safe_send_message(response.Data.chat_type, loadout_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid loadout! Type /loadout for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Loadout error: {str(e)}", uid, chat_id, key, iv)

                        # RANK PUSH TIPS - /rank [tier]
                        if inPuTMsG.strip().startswith('/rank'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                rank_list = """[B][C][00FF00]📈 RANK PUSH TIPS 📈
[FFFFFF]
[00FFFF]bronze [FFFFFF]- 🥉 Bronze Tips
[00FFFF]silver [FFFFFF]- 🥈 Silver Tips
[00FFFF]gold [FFFFFF]- 🥇 Gold Tips
[00FFFF]platinum [FFFFFF]- 💎 Platinum Tips
[00FFFF]diamond [FFFFFF]- 💠 Diamond Tips
[00FFFF]heroic [FFFFFF]- 🔥 Heroic Tips
[00FFFF]grandmaster [FFFFFF]- 👑 Grandmaster Tips
[FFFFFF]Usage: /rank gold"""
                                await safe_send_message(response.Data.chat_type, rank_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    rank_tier = parts[1].lower()
                                    if rank_tier in RANK_TIPS:
                                        rank_msg = RANK_TIPS[rank_tier]
                                        await safe_send_message(response.Data.chat_type, rank_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid rank! Type /rank for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Rank tip error: {str(e)}", uid, chat_id, key, iv)

                        # GAME MODES - /mode [type]
                        if inPuTMsG.strip().startswith('/mode'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                mode_list = """[B][C][00FF00]🎮 GAME MODES 🎮
[FFFFFF]
[00FFFF]br [FFFFFF]- 🔥 Battle Royale
[00FFFF]cs [FFFFFF]- ⚔️ Clash Squad
[00FFFF]lone [FFFFFF]- 🐺 Lone Wolf
[00FFFF]rush [FFFFFF]- ⚡ Rush Hour
[00FFFF]gun [FFFFFF]- 🔫 Gun King
[FFFFFF]Usage: /mode br"""
                                await safe_send_message(response.Data.chat_type, mode_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    mode_type = parts[1].lower()
                                    if mode_type in GAME_MODES:
                                        mode_msg = GAME_MODES[mode_type]
                                        await safe_send_message(response.Data.chat_type, mode_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid mode! Type /mode for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Mode error: {str(e)}", uid, chat_id, key, iv)

                        # DROP LOCATIONS - /drop [location]
                        if inPuTMsG.strip().startswith('/drop'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                drop_list = """[B][C][00FF00]📍 DROP LOCATIONS 📍
[FFFFFF]
[00FFFF]peaks [FFFFFF]- 🏔️ Bermuda Peaks
[00FFFF]mill [FFFFFF]- 🏭 Bermuda Mill
[00FFFF]dock [FFFFFF]- ⚓ Bermuda Dock
[00FFFF]clock [FFFFFF]- 🕐 Kalahari Clock Tower
[00FFFF]refinery [FFFFFF]- 🏭 Kalahari Refinery
[00FFFF]alpine [FFFFFF]- 🏔️ Alpine Main Town
[FFFFFF]Usage: /drop peaks"""
                                await safe_send_message(response.Data.chat_type, drop_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    drop_loc = parts[1].lower()
                                    if drop_loc in DROP_LOCATIONS:
                                        drop_msg = DROP_LOCATIONS[drop_loc]
                                        await safe_send_message(response.Data.chat_type, drop_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid location! Type /drop for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Drop location error: {str(e)}", uid, chat_id, key, iv)

                        # TOURNAMENT/SCRIM SETUP - /scrim [mode]
                        if inPuTMsG.strip().startswith('/scrim'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                scrim_list = """[B][C][00FF00]🏆 TOURNAMENT MODES 🏆
[FFFFFF]
[00FFFF]1v1 [FFFFFF]- 1v1 Duel
[00FFFF]2v2 [FFFFFF]- 2v2 Team
[00FFFF]4v4 [FFFFFF]- 4v4 Squad
[00FFFF]solo [FFFFFF]- Solo Battle
[00FFFF]duo [FFFFFF]- Duo Battle
[00FFFF]squad [FFFFFF]- Full Squad
[FFFFFF]Usage: /scrim 4v4"""
                                await safe_send_message(response.Data.chat_type, scrim_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    scrim_mode = parts[1].lower()
                                    if scrim_mode in TOURNAMENT_MODES:
                                        scrim_name = TOURNAMENT_MODES[scrim_mode]
                                        scrim_setup_msg = f"""[B][C][FFD700]🏆 TOURNAMENT SETUP 🏆
[FFFFFF]
Mode: [00FF00]{scrim_name}
[FFFFFF]
[FF0000]RULES:
[FFFFFF]• No camping
[FFFFFF]• Fair play
[FFFFFF]• Follow zone
[FFFFFF]• Best of 3 rounds
[FFFFFF]• Good luck! 👊"""
                                        await safe_send_message(response.Data.chat_type, scrim_setup_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid mode! Type /scrim for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Scrim error: {str(e)}", uid, chat_id, key, iv)

                        # CHARACTER SKILLS - /char [name]
                        if inPuTMsG.strip().startswith('/char'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                char_list = """[B][C][00FF00]🎮 CHARACTER SKILLS 🎮
[FFFFFF]
[00FFFF]dj [FFFFFF]- 🎧 DJ ALOK
[00FFFF]chrono [FFFFFF]- 🛡️ CHRONO
[00FFFF]k [FFFFFF]- 🔥 K
[00FFFF]joseph [FFFFFF]- ⚡ JOSEPH
[00FFFF]moco [FFFFFF]- 🔍 MOCO
[00FFFF]clu [FFFFFF]- 🎯 CLU
[00FFFF]wolfrahh [FFFFFF]- 🐺 WOLFRAHH
[00FFFF]dasha [FFFFFF]- 💃 DASHA
[FFFFFF]Usage: /char alok"""
                                await safe_send_message(response.Data.chat_type, char_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    char_name = parts[1].lower()
                                    if char_name in CHARACTER_SKILLS:
                                        char_msg = CHARACTER_SKILLS[char_name]
                                        await safe_send_message(response.Data.chat_type, char_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid character! Type /char for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Character error: {str(e)}", uid, chat_id, key, iv)

                        # WEAPON STATS - /weaponstats [name]
                        if inPuTMsG.strip().startswith('/weaponstats'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                weapon_stats_list = """[B][C][00FF00]🔫 WEAPON STATS GUIDE 🔫
[FFFFFF]
[00FFFF]ak [FFFFFF]- AK47
[00FFFF]mp40 [FFFFFF]- MP40
[00FFFF]awm [FFFFFF]- AWM
[00FFFF]m1887 [FFFFFF]- M1887
[00FFFF]scar [FFFFFF]- SCAR
[00FFFF]m4a1 [FFFFFF]- M4A1
[00FFFF]groza [FFFFFF]- GROZA
[00FFFF]ump [FFFFFF]- UMP
[FFFFFF]Usage: /weaponstats ak"""
                                await safe_send_message(response.Data.chat_type, weapon_stats_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    weapon_name = parts[1].lower()
                                    if weapon_name in WEAPON_STATS:
                                        weapon_msg = WEAPON_STATS[weapon_name]
                                        await safe_send_message(response.Data.chat_type, weapon_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid weapon! Type /weaponstats for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Weapon stats error: {str(e)}", uid, chat_id, key, iv)

                        # STRATEGIES - /strategy [type]
                        if inPuTMsG.strip().startswith('/strategy'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                strategy_list = """[B][C][00FF00]📋 GAME STRATEGIES 📋
[FFFFFF]
[00FFFF]rush [FFFFFF]- ⚡ Rush Strategy
[00FFFF]camp [FFFFFF]- 🎯 Camp Strategy
[00FFFF]balance [FFFFFF]- ⚖️ Balanced Strategy
[00FFFF]sniper [FFFFFF]- 🎯 Sniper Strategy
[FFFFFF]Usage: /strategy rush"""
                                await safe_send_message(response.Data.chat_type, strategy_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    strategy_type = parts[1].lower()
                                    if strategy_type in STRATEGIES:
                                        strategy_msg = STRATEGIES[strategy_type]
                                        await safe_send_message(response.Data.chat_type, strategy_msg, uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid strategy! Type /strategy for list", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Strategy error: {str(e)}", uid, chat_id, key, iv)

                        # RAINBOW ANIMATION - /rainbow
                        if inPuTMsG.strip() == '/rainbow':
                            global rainbow_running, rainbow_task
                            if rainbow_running:
                                rainbow_running = False
                                if rainbow_task:
                                    rainbow_task.cancel()
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]🌈 Rainbow animation stopped!", uid, chat_id, key, iv)
                            else:
                                rainbow_running = True
                                await safe_send_message(response.Data.chat_type, "[B][C][00FF00]🌈 Rainbow animation started!\n[B][C][FFFFFF]Type /rainbow again to stop.", uid, chat_id, key, iv)
                                
                                async def rainbow_loop():
                                    color_index = 0
                                    while rainbow_running:
                                        try:
                                            color = RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
                                            msg = f"[B][C][{color}]🌈 RAINBOW MODE ACTIVATED 🌈"
                                            await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                            color_index += 1
                                            await asyncio.sleep(2)
                                        except asyncio.CancelledError:
                                            break
                                        except Exception as e:
                                            print(f"Rainbow error: {e}")
                                            await asyncio.sleep(2)
                                
                                rainbow_task = asyncio.create_task(rainbow_loop())

                        # FLASH ANIMATION - /flash
                        if inPuTMsG.strip() == '/flash':
                            global flash_running, flash_task
                            if flash_running:
                                flash_running = False
                                if flash_task:
                                    flash_task.cancel()
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]⚡ Flash animation stopped!", uid, chat_id, key, iv)
                            else:
                                flash_running = True
                                await safe_send_message(response.Data.chat_type, "[B][C][00FF00]⚡ Flash animation started!\n[B][C][FFFFFF]Type /flash again to stop.", uid, chat_id, key, iv)
                                
                                async def flash_loop():
                                    flash_colors = ["FF0000", "FFFFFF", "000000", "FFFF00", "00FFFF", "FF00FF"]
                                    while flash_running:
                                        try:
                                            for color in flash_colors:
                                                if not flash_running:
                                                    break
                                                msg = f"[B][C][{color}]⚡ FLASH MODE ⚡"
                                                await safe_send_message(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                                await asyncio.sleep(0.5)
                                        except asyncio.CancelledError:
                                            break
                                        except Exception as e:
                                            print(f"Flash error: {e}")
                                            await asyncio.sleep(1)
                                
                                flash_task = asyncio.create_task(flash_loop())

                        # DANCE EMOTES - /dance [1-6]
                        if inPuTMsG.strip().startswith('/dance'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                dance_list = "[B][C][00FF00]🕺 DANCE EMOTES 🕺\n[FFFFFF]1-Hip Hop, 2-Breakdance, 3-Salsa, 4-Disco, 5-TikTok, 6-Free Style\n[00FFFF]Usage: /dance [1-6]"
                                await safe_send_message(response.Data.chat_type, dance_list, uid, chat_id, key, iv)
                            else:
                                try:
                                    dance_id = parts[1]
                                    if dance_id in DANCE_EMOTES:
                                        emote_id = int(DANCE_EMOTES[dance_id])
                                        # Send dance emote packet
                                        from xC4 import Emote_k
                                        dance_packet = await Emote_k(uid, emote_id, key, iv, region)
                                        await SEndPacKeT('OnLine', dance_packet)
                                        await safe_send_message(response.Data.chat_type, f"[B][C][00FF00]🕺 Dance {dance_id} performed!", uid, chat_id, key, iv)
                                    else:
                                        await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Invalid dance ID! Use 1-6", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Dance error: {str(e)}", uid, chat_id, key, iv)

                        # SUPER EMOTE SPAM - /super [emote_id] [count]
                        if inPuTMsG.strip().startswith('/super'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Usage: /super [emote_id] [count]\nExample: /super 1 50", uid, chat_id, key, iv)
                            else:
                                try:
                                    emote_id = int(parts[1])
                                    count = int(parts[2]) if len(parts) > 2 else 30
                                    count = min(count, 100)  # Max 100
                                    
                                    await safe_send_message(response.Data.chat_type, f"[B][C][00FF00]🚀 Starting SUPER emote spam: {count} emotes!", uid, chat_id, key, iv)
                                    
                                    from xC4 import Emote_k
                                    for i in range(count):
                                        try:
                                            emote_packet = await Emote_k(uid, ALL_EMOTE.get(emote_id, 909000001), key, iv, region)
                                            await SEndPacKeT('OnLine', emote_packet)
                                            await asyncio.sleep(0.1)
                                        except Exception as e:
                                            print(f"Super emote error: {e}")
                                            continue
                                    
                                    await safe_send_message(response.Data.chat_type, f"[B][C][00FF00]✅ Super emote spam completed!", uid, chat_id, key, iv)
                                except Exception as e:
                                    await safe_send_message(response.Data.chat_type, f"[B][C][FF0000]❌ Super error: {str(e)}", uid, chat_id, key, iv)

                        # AUTO-ACCEPT TOGGLE - /autoaccept
                        if inPuTMsG.strip() == '/autoaccept':
                            global auto_accept_invite
                            auto_accept_invite = not auto_accept_invite
                            status = "[00FF00]ENABLED ✅" if auto_accept_invite else "[FF0000]DISABLED ❌"
                            await safe_send_message(response.Data.chat_type, f"[B][C][00FFFF]🤖 Auto-accept invitations: {status}", uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/3")):
                            # Process /3 command - Create 3 player group
                            initial_message = f"[B][C]{get_random_color()}\n\nCreating 3-Player Group...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT('OnLine', PAc)
                            
                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT('OnLine', C)
                            
                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT('OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT('OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! 6-Player Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/roommsg'):
                            print('Processing room message command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /roommsg (room_id) (message)\nExample: /roommsg 489775386 Hello room!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                message = " ".join(parts[2:])
        
                                initial_msg = f"[B][C][00FF00]📢 Sending to room {room_id}: {message}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Get bot UID
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else 13699776666
            
                                    # Send room chat using leaked packet structure
                                    room_chat_packet = await send_room_chat_enhanced(message, room_id, key, iv, region)
                                    await SEndPacKeT('OnLine', room_chat_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Message sent to room {room_id}!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"✅ Room message sent to {room_id}: {message}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/5")):
                            # Process /5 command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\n\nSending Group Invitation...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Fast squad creation and invite
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT('OnLine', PAc)
                            
                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT('OnLine', C)
                            
                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT('OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)  # Reduced from 3 seconds
                            await SEndPacKeT('OnLine', E)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Group invitation sent successfully to {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip() == "/admin":
                            # Process /admin command in any chat type
                            admin_message = """
[C][B][FF0000]╔══════════╗
[FFFFFF]✨ folow on youtube   
[FFFFFF]          ⚡ Surjo99exe ❤️  
[FFFFFF]                   thank for support 
[FF0000]╠══════════╣
[FFD700]⚡ OWNER : [FFFFFF]Surjo99exe    
[FFD700]✨ কেউ GUILD BOT কিনতে চাইলে telegram এ message করবেন, telegram username @Surjo99exe ❤️  
[FF0000]╚══════════╝
[FFD700]✨ Developer —͟͞͞ </> Surjo99exe ❄️  ⚡
"""
                            await safe_send_message(response.Data.chat_type, admin_message, uid, chat_id, key, iv)

                        # Add this with your other command handlers in the TcPChaT function
                        if inPuTMsG.strip().startswith('/multijoin'):
                            print('Processing multi-account join request')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /multijoin (target_uid)\nExample: /multijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                initial_msg = f"[B][C][00FF00]🚀 Starting multi-join attack on {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Try the fake multi-account method (more reliable)
                                    success_count, total_attempts = await real_multi_account_join(target_uid, key, iv, region)
            
                                    if success_count > 0:
                                        result_msg = f"""
[B][C][00FF00]✅ MULTI-JOIN ATTACK COMPLETED!

🎯 Target: {target_uid}
✅ Successful Requests: {success_count}
📊 Total Attempts: {total_attempts}
⚡ Different squad variations sent!

💡 Check your game for join requests!
"""
                                    else:
                                        result_msg = f"[B][C][FF0000]❌ All join requests failed! Check bot connection.\n"
            
                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Multi-join error: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

           
                        if inPuTMsG.strip().startswith('/fastmultijoin'):
                            print('Processing fast multi-account join spam')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fastmultijoin (uid)\nExample: /fastmultijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Load accounts
                                accounts_data = load_accounts()
                                if not accounts_data:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! No accounts found!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                
                                initial_msg = f"[B][C][00FF00]⚡ FAST MULTI-ACCOUNT JOIN SPAM!\n🎯 Target: {target_uid}\n👥 Accounts: {len(accounts_data)}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    join_count = 0
                                    # Send join requests rapidly from all accounts
                                    for uid, password in accounts_data.items():
                                        try:
                                            # Use your existing join request function
                                            join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
                                            await SEndPacKeT('OnLine', join_packet)
                                            join_count += 1
                                            print(f"✅ Fast join from account {uid}")
                    
                                            # Very short delay
                                            await asyncio.sleep(0.1)
                    
                                        except Exception as e:
                                            print(f"❌ Fast join failed for {uid}: {e}")
                                            continue
            
                                    success_msg = f"[B][C][00FF00]✅ FAST MULTI-JOIN COMPLETED!\n🎯 Target: {target_uid}\n✅ Successful: {join_count}/{len(accounts_data)}\n⚡ Speed: Ultra fast\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR in fast multi-join: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
           
           
                        # Update the command handler
                        if inPuTMsG.strip().startswith('/reject'):
                            print('Processing reject spam command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /reject (target_uid)\nExample: /reject 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing reject spam
                                if reject_spam_task and not reject_spam_task.done():
                                    reject_spam_running = False
                                    reject_spam_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Send start message
                                start_msg = f"[B][C][1E90FF]🌀 Started Reject Spam on: {target_uid}\n🌀 Packets: 150 each type\n🌀 Interval: 0.2 seconds\n"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
        
                                # Start reject spam in background
                                reject_spam_running = True
                                reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
        
                                # Wait for completion in background and send completion message
                                asyncio.create_task(handle_reject_completion(reject_spam_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))


                        if inPuTMsG.strip() == '/reject_stop':
                            if reject_spam_task and not reject_spam_task.done():
                                reject_spam_running = False
                                reject_spam_task.cancel()
                                stop_msg = f"[B][C][00FF00]✅ Reject spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ No active reject spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                                    
                                                                        
                        # In your command handler where you call Room_Spam:
                        if inPuTMsG.strip().startswith('/room'):
                            print('Processing advanced room spam command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /room (uid)\nExample: /room 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                room_id = parts[2]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                # Send initial message
                                initial_msg = f"[B][C][00FF00]🔍 Working on room spam for {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                try:
                                    # Method 1: Try to get room ID from recent packets
                                
                                    

                                    room_msg = f"[B][C][00FF00]🎯 Detected player in room {room_id}\n"
                                    await safe_send_message(response.Data.chat_type, room_msg, uid, chat_id, key, iv)
            
                                    # Create spam packet
                                    spam_packet = await Room_Spam(target_uid, room_id, "Surjo99exe", key, iv)
            
                                    # Send 99 spam packets rapidly (like your other TCP)
                                    spam_count = 99
                                    
                                    start_msg = f"[B][C][00FF00]🚀 Starting spam: {spam_count} packets to room {room_id}\n"
                                    await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
            
                                    for i in range(spam_count):
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
                
                                        # Progress updates
                                        if (i + 1) % 25 == 0:
                                            progress_msg = f"[B][C][00FF00]📦 Progress: {i+1}/{spam_count} packets sent\n"
                                            await safe_send_message(response.Data.chat_type, progress_msg, uid, chat_id, key, iv)
                                            print(f"Room spam progress: {i+1}/{spam_count} to UID: {target_uid}")
                
                                        # Very short delay (0.05 seconds = 50ms)
                                        await asyncio.sleep(0.05)
            
                                    # Final success message
                                    success_msg = f"[B][C][00FF00]✅ ROOM SPAM COMPLETED!\n🎯 Target: {target_uid}\n📦 Packets: {spam_count}\n🏠 Room: {room_id}\n⚡ Speed: Ultra fast\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"Room spam completed for UID: {target_uid}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR in room spam: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    print(f"Room spam error: {e}")          
                                    
                                    
                        # Individual command handlers for /s1 to /s5
                        if inPuTMsG.strip().startswith('/s1'):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
    
                        if inPuTMsG.strip().startswith('/s2'):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s3'):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s4'):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s5'):
                            await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            
                            #ALL BADGE SPAM REQUEST 
                        if inPuTMsG.strip().startswith('/spam'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ Usage: /spam <uid>\nExample: /spam 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                total_requests = 10  # total join requests
                                sequence = ['s1', 's2', 's3', 's4', 's5']  # all badge commands

                                # Send initial consolidated message
                                initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid} with all badges...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                count = 0
                                while count < total_requests:
                                    for cmd in sequence:
                                        if count >= total_requests:
                                            break
                                        # Build a fake command string like "/s1 123456789"
                                        fake_command = f"/{cmd} {target_uid}"
                                        await handle_badge_command(cmd, fake_command, uid, chat_id, key, iv, region, response.Data.chat_type)
                                        count += 1

                                # Success message after all 30 requests
                                success_msg = f"[B][C][00FF00]✅ Successfully sent {total_requests} Join Requests!\n🎯 Target: {target_uid}\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                    
                                                                                             #JOIN ROOM       
                        if inPuTMsG.strip().startswith('/joinroom'):
                            print('Processing custom room join command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /joinroom (room_id) (password)\nExample: /joinroom 123456 0000\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
        
                                initial_msg = f"[B][C][00FF00]🚀 Joining custom room...\n🏠 Room: {room_id}\n🔑 Password: {room_password}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Join the custom room
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT('OnLine', join_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Joined custom room {room_id}!\n🤖 Bot is now in room chat!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to join room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/createroom'):
                            print('Processing custom room creation')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /createroom (room_name) (password) [players=4]\nExample: /createroom BOTROOM 0000 4\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_name = parts[1]
                                room_password = parts[2]
                                max_players = parts[3] if len(parts) > 3 else "4"
        
                                initial_msg = f"[B][C][00FF00]🏠 Creating custom room...\n📛 Name: {room_name}\n🔑 Password: {room_password}\n👥 Max Players: {max_players}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Create custom room
                                    create_packet = await create_custom_room(room_name, room_password, int(max_players), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', create_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Custom room created!\n🏠 Room: {room_name}\n🔑 Password: {room_password}\n👥 Max: {max_players}\n🤖 Bot is now hosting!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to create room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)                                                                                                                                                                                                               
                                                
                                              
                                                                                          # FIXED JOIN COMMAND
                        if inPuTMsG.startswith('/join'):
                            # Process /join command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /join (team_code)\nExample: /join ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                sender_uid = response.Data.uid  # Get the UID of person who sent the command
        
                                initial_message = f"[B][C]{get_random_color()}\nJoining squad with code: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try using the regular join method first
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT('OnLine', EM)
            
                                    # Wait a bit for the join to complete
                                    await asyncio.sleep(2)
            
                                    # DUAL RINGS EMOTE - BOTH SENDER AND BOT
                                    try:
                                        await auto_rings_emote_dual(sender_uid, key, iv, region)
                                    except Exception as emote_error:
                                        print(f"Dual emote failed but join succeeded: {emote_error}")
            
                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! Joined squad: {CodE}!\n💍 Dual Rings emote activated!\n🤖 Bot + You = 💕\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print(f"Regular join failed, trying ghost join: {e}")
                                    # If regular join fails, try ghost join
                                    try:
                                        # Get bot's UID from global context or login data
                                        bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                
                                        ghost_packet = await GenJoinSquadsPacket("", key, iv)
                                        if ghost_packet:
                                            await SEndPacKeT('OnLine', ghost_packet)
                    
                                            # Wait a bit for ghost join to complete
                                            await asyncio.sleep(2)
                    
                                            # DUAL RINGS EMOTE - BOTH SENDER AND BOT
                                            try:
                                                await auto_rings_emote_dual(sender_uid, key, iv, region)
                                            except Exception as emote_error:
                                                print(f"Dual emote failed but ghost join succeeded: {emote_error}")
                    
                                            success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joined squad: {CodE}!\n💍 Dual Rings emote activated!\n🤖 Bot + You = 💕\n"
                                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                    
                                    except Exception as ghost_error:
                                        print(f"Ghost join also failed: {ghost_error}")
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to join squad: {str(ghost_error)}\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                
                        if inPuTMsG.strip().startswith('/ghost'):
                            # Process /ghost command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ghost (team_code)\nExample: /ghost ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nGhost joining squad with code: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Get bot's UID from global context or login data
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                                    
                                    ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                    if ghost_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                        success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joined squad with code: {CodE}!\n"
                                        await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Ghost join failed: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW LAG COMMAND
                        if inPuTMsG.strip().startswith('/lag '):
                            print('Processing lag command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /lag (team_code)\nExample: /lag ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                
                                # Stop any existing lag task
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)
                                
                                # Start new lag task
                                lag_running = True
                                lag_task = asyncio.create_task(lag_team_loop(team_code, key, iv, region))
                                
                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack started!\nTeam: {team_code}\nAction: Rapid join/leave\nSpeed: Ultra fast (milliseconds)\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # STOP LAG COMMAND
                        if inPuTMsG.strip() == '/stop lag':
                            if lag_task and not lag_task.done():
                                lag_running = False
                                lag_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Lag attack stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active lag attack to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith('/exit'):
                            # Process /exit command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nLeaving current squad...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT('OnLine', leave)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Left the squad successfully!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/start'):
                            # Process /start command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nStarting match...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            EM = await FS(key , iv)
                            await SEndPacKeT('OnLine', EM)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Match starting command sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith('/title'):
                            await handle_all_titles_command(inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            

                        # Emote command - works in all chat types
                        # Check for /e followed by space to avoid matching /evos, /evo, etc.
                        if inPuTMsG.strip().startswith('/e ') or inPuTMsG.strip() == '/e':
                            print(f'Processing emote command in chat type: {response.Data.chat_type}')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /e (uid) (emote_id)\nExample: /e 123456789 909000001\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                                
                            initial_message = f'[B][C]{get_random_color()}\nSending emote to target...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []

                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1])  # Last part is emote ID

                            except ValueError as ve:
                                print("ValueError:", ve)
                                s = True
                            except Exception as e:
                                print(f"Error parsing emote command: {e}")
                                s = True

                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(target, idT, key, iv, region)
                                        await SEndPacKeT('OnLine', H)
                                        await asyncio.sleep(0.1)
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Emote {idT} sent to {len(target_uids)} player(s)!\nTargets: {', '.join(map(str, target_uids))}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending emote: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Invalid UID format. Usage: /e (uid) (emote_id)\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                                # /lvup command - Auto Start Bot
                        if inPuTMsG.strip().startswith('/lw'):
                            print('Processing /lvup auto-start command')
                            global auto_start_running, auto_start_teamcode, stop_auto, auto_start_task
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /lvup (team_code)\nExample: /lvup 123456\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                
                                # Check if numeric
                                if not team_code.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Team code must be numbers only!\nExample: /lvup 123456\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                
                                # Check if already running
                                if auto_start_running:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Auto start already running for team {auto_start_teamcode}!\nUse /stop to stop first.\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                
                                # Start auto start
                                global auto_start_task, stop_auto
                                stop_auto = False
                                auto_start_running = True
                                auto_start_teamcode = team_code
                                
                                # Send initial message
                                initial_msg = f"""
[B][C][00FFFF]🤖 AUTO START BOT ACTIVATED!

🎯 Team Code: {team_code}
⚡ Action: Join → Start → Wait → Leave → Repeat
⏰ Start Spam: {start_spam_duration} seconds
⏳ Wait Time: {wait_after_match} seconds
🔄 Loop: Continuous 24x7

💡 To stop: /stop
"""
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                # Start auto loop in background
                                auto_start_task = asyncio.create_task(
                                    auto_start_loop(team_code, uid, chat_id, response.Data.chat_type, key, iv, region)
                                )
                        

                        if inPuTMsG.strip().startswith('/stop'):
                            print('Processing /lvup auto-start command')
                            
                                # Start auto start
                            stop_auto = True
                            auto_start_running = False
                            auto_start_teamcode = None
                                
                                # Send initial message
                            initial_msg = f"""
[B][C][00FFFF]🤖 AUTO START BOT STOPED !

🎯 Team Code: {team_code}
⚡ Action: Join → Start → Wait → Leave → Repeat
⏰ Start Spam: {start_spam_duration} seconds
⏳ Wait Time: {wait_after_match} seconds
🔄 Loop: Continuous 24x7

💡 To on: /lw [team_code]
"""
                            await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                

                        # EVO CYCLE START COMMAND - /evos
                        if inPuTMsG.strip().startswith('/evos'):
                            print('Processing evo cycle start command in any chat type')
                            # Declare global variables

                            parts = inPuTMsG.strip().split()
                            uids = []
    
                            # Always use the sender's UID (the person who typed /evos)
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
                            print(f"Using sender's UID: {sender_uid}")
    
                            # Optional: Also allow specifying additional UIDs
                            if len(parts) > 1:
                                for part in parts[1:]:  # Skip the first part which is "/evos"
                                    if part.isdigit() and len(part) >= 7 and part != sender_uid:  # UIDs are usually 7+ digits
                                        uids.append(part)
                                        print(f"Added additional UID: {part}")

                            # Stop any existing evo cycle
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
    
                            # Start new evo cycle
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region))
    
                            # SUCCESS MESSAGE
                            if len(uids) == 1:
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle started!\n🎯 Target: Yourself\n🎭 Emotes: All 18 evolution emotes\n⏰ Delay: 5 seconds between emotes\n🔄 Cycle: Continuous loop until /sevos\n"
                            else:
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle started!\n🎯 Targets: Yourself + {len(uids)-1} other players\n🎭 Emotes: All 18 evolution emotes\n⏰ Delay: 5 seconds between emotes\n🔄 Cycle: Continuous loop until /sevos\n"
    
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            print(f"Started evolution emote cycle for UIDs: {uids}")
                        
                        # EVO CYCLE STOP COMMAND - /sevos
                        if inPuTMsG.strip() == '/sevos':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution emote cycle stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                print("Evolution emote cycle stopped by command")
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution emote cycle to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Fast emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/fast'):
                            print('Processing fast emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fast uid1 [uid2] [uid3] [uid4] [1-410]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and [1-410]
                                uids = []
                                emote_id = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:  # Assuming UIDs are longer than 3 digits
                                            uids.append(part)
                                        else:
                                            emote_id = ALL_EMOTE.get(int(part))
                                    else:
                                        break
                                
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /fast uid1 [uid2] [uid3] [uid4] [1-410]\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    # Stop any existing fast spam
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    
                                    # Start new fast spam
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast emote spam started!\nTargets: {len(uids)} players\nEmote: {emote_id}\nSpam count: 25 times\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Custom emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/p'):
                            print('Processing custom emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /p (uid) [1-410] (times)\nExample: /p 123456789 [1-410] 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = ALL_EMOTE.get(int(parts[2]))
                                    times = int(parts[3])
                                    
                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Times must be greater than 0!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif times > 100:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Maximum 100 times allowed for safety!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        # Stop any existing custom spam
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                                        
                                        # Start new custom spam
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                                        
                                        # SUCCESS MESSAGE
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom emote spam started!\nTarget: {target_uid}\nEmote: {emote_id}\nTimes: {times}\n"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Usage: /p (uid) [1-410] (times)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Spam request command - works in all chat types
                        if inPuTMsG.strip().startswith('/spm_inv'):
                            print('Processing spam invite with cosmetics')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /spm_inv (uid)\nExample: /spm_inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing spam request
                                if spam_request_task and not spam_request_task.done():
                                    spam_request_running = False
                                    spam_request_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Start new spam request WITH COSMETICS
                                spam_request_running = True
                                spam_request_task = asyncio.create_task(spam_request_loop_with_cosmetics(target_uid, key, iv, region))
        
                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ COSMETIC SPAM STARTED!\n🎯 Target: {target_uid}\n📦 Requests: 30\n🎭 Features: V-Badges + Cosmetics\n⚡ Each invite has different cosmetics!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Stop spam request command - works in all chat types
                        if inPuTMsG.strip() == '/stop spm_inv':
                            if spam_request_task and not spam_request_task.done():
                                spam_request_running = False
                                spam_request_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Spam request stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active spam request to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW PLAY COMMANDS
                        if inPuTMsG.strip().startswith('/play '):
                            print('Processing evo command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /play uid1 [uid2] [uid3] [uid4] number(1-410)\nExample: /play 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 3:  # Number should be 1-410 (1,2 or 3 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /play uid1 [uid2] [uid3] [uid4] number(1-410)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in ALL_EMOTE:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-410 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending emote {number_int}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await play_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use (1-410) only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW 100 LV EMOTE COMMANDS
                        if inPuTMsG.strip().startswith('/100 '):
                            print('Processing evo command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /100 uid1 [uid2] [uid3] [uid4]\nExample: /100 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 3:  # Number should be 1-410 (1,2 or 3 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /100 uid1 [uid2] [uid3] [uid4]\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = 268
                                        if number_int not in ALL_EMOTE:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-410 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending 100 level emote...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await play_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use (1-410) only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO COMMANDS
                        if inPuTMsG.strip().startswith('/evo '):
                            print('Processing evo command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending evolution emote {number_int}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evo_fast '):
                            print('Processing evo_fast command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo_fast 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_fast uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_fast spam
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_fast spam
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nSpam count: 25 times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO_CUSTOM COMMAND
                        if inPuTMsG.strip().startswith('/evo_c '):
                            print('Processing evo_c command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\nExample: /evo_c 123456789 1 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids, number, and time
                                uids = []
                                number = None
                                time_val = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number or time should be 1-100 (1, 2, or 3 digits)
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                # If we still don't have time_val, try to get it from the last part
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        # Remove time_val from uids if it was added by mistake
                                        if time_val in uids:
                                            uids.remove(time_val)
                                
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo_c uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Time must be between 1-100 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_custom spam
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_custom spam
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nRepeat: {time_int} times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number/time format! Use numbers only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_fast spam command
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution fast spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution fast spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_custom spam command
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution custom spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution custom spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        # NEW UTILITY COMMANDS
                        # Time command - shows current time
                        if inPuTMsG.strip() == '/time':
                            from datetime import datetime
                            current_time = datetime.now().strftime("%H:%M:%S")
                            time_msg = f"[B][C][00FF00]🕐 Current Time: {current_time}\n"
                            await safe_send_message(response.Data.chat_type, time_msg, uid, chat_id, key, iv)
                        
                        # Date command - shows current date
                        if inPuTMsG.strip() == '/date':
                            from datetime import datetime
                            current_date = datetime.now().strftime("%Y-%m-%d")
                            date_msg = f"[B][C][00FF00]📅 Current Date: {current_date}\n"
                            await safe_send_message(response.Data.chat_type, date_msg, uid, chat_id, key, iv)
                        
                        # UID command - shows bot's UID
                        if inPuTMsG.strip() == '/uid':
                            bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else 14149309921
                            uid_msg = f"[B][C][00FF00]🤖 Bot UID: {bot_uid}\n"
                            await safe_send_message(response.Data.chat_type, uid_msg, uid, chat_id, key, iv)
                        
                        # Server command - shows server info
                        if inPuTMsG.strip() == '/server':
                            server_msg = f"[B][C][00FF00]🌐 Server: {region}\n📍 IP: 202.81.106.16\n"
                            await safe_send_message(response.Data.chat_type, server_msg, uid, chat_id, key, iv)
                        
                        # Ping command - simple response test
                        if inPuTMsG.strip() == '/ping':
                            ping_msg = f"[B][C][00FF00]🏓 Pong! Bot is online and responsive!\n"
                            await safe_send_message(response.Data.chat_type, ping_msg, uid, chat_id, key, iv)
                        
                        # Calculator command
                        if inPuTMsG.strip().startswith('/calc '):
                            try:
                                expression = inPuTMsG[6:].strip()
                                # Safe eval - only allow math operations
                                allowed_chars = set('0123456789+-*/.() ')
                                if all(c in allowed_chars for c in expression):
                                    result = eval(expression)
                                    calc_msg = f"[B][C][00FF00]🧮 {expression} = {result}\n"
                                else:
                                    calc_msg = f"[B][C][FF0000]❌ Invalid characters in expression!\n"
                            except:
                                calc_msg = f"[B][C][FF0000]❌ Invalid calculation!\n"
                            await safe_send_message(response.Data.chat_type, calc_msg, uid, chat_id, key, iv)
                        
                        # Random number command
                        if inPuTMsG.strip().startswith('/random '):
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) >= 3:
                                    min_val = int(parts[1])
                                    max_val = int(parts[2])
                                    import random
                                    random_num = random.randint(min_val, max_val)
                                    random_msg = f"[B][C][00FF00]🎲 Random number ({min_val}-{max_val}): {random_num}\n"
                                else:
                                    random_msg = f"[B][C][FF0000]❌ Usage: /random [min] [max]\n"
                            except:
                                random_msg = f"[B][C][FF0000]❌ Usage: /random [min] [max]\n"
                            await safe_send_message(response.Data.chat_type, random_msg, uid, chat_id, key, iv)
                        
                        # Coin flip command
                        if inPuTMsG.strip() == '/coin':
                            import random
                            result = random.choice(['Heads', 'Tails'])
                            coin_msg = f"[B][C][00FF00]🪙 Coin flip: {result}\n"
                            await safe_send_message(response.Data.chat_type, coin_msg, uid, chat_id, key, iv)
                        
                        # Dice command
                        if inPuTMsG.strip() == '/dice':
                            import random
                            dice = random.randint(1, 6)
                            dice_msg = f"[B][C][00FF00]🎲 Dice roll: {dice}\n"
                            await safe_send_message(response.Data.chat_type, dice_msg, uid, chat_id, key, iv)
                        
                        # Auto-join toggle command
                        if inPuTMsG.strip() == '/autojoin on':
                            global auto_join_enabled
                            auto_join_enabled = True
                            aj_msg = f"[B][C][00FF00]✅ Auto-join enabled!\n"
                            await safe_send_message(response.Data.chat_type, aj_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip() == '/autojoin off':
                            auto_join_enabled = False
                            aj_msg = f"[B][C][FF0000]❌ Auto-join disabled!\n"
                            await safe_send_message(response.Data.chat_type, aj_msg, uid, chat_id, key, iv)
                        
                        # Manual accept invite command
                        if inPuTMsG.strip() == '/accept':
                            print(f'Processing manual accept command')
                            
                            initial_message = f"[B][C]{get_random_color()}\nAccepting team invite...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            try:
                                # Send join packet without team code (for accepting invite)
                                join_packet = await GenJoinSquadsPacket("", key, iv)
                                await SEndPacKeT('OnLine', join_packet)
                                
                                success_msg = f"[B][C][00FF00]✅ Joined team!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                
                                # Set squad status
                                global insquad, joining_team
                                insquad = uid
                                joining_team = False
                                
                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ Failed to join: {str(e)}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # status message 
                        
                        # Uptime command - show how long bot has been running
                        if inPuTMsG.strip() == '/uptime':
                            from datetime import datetime
                            import time
                            # Calculate uptime (simplified - from current time)
                            current_time = time.time()
                            uptime_seconds = int(current_time % 86400)  # Today's seconds
                            hours = uptime_seconds // 3600
                            minutes = (uptime_seconds % 3600) // 60
                            uptime_msg = f"[B][C][00FF00]⏱️ Bot Uptime: {hours}h {minutes}m\n🤖 Running smoothly!\n"
                            await safe_send_message(response.Data.chat_type, uptime_msg, uid, chat_id, key, iv)
                        
                        # Echo command - repeat what user said
                        if inPuTMsG.strip().startswith('/echo '):
                            echo_text = inPuTMsG[6:].strip()
                            if echo_text:
                                echo_msg = f"[B][C][00FFFF]📢 {echo_text}\n"
                                await safe_send_message(response.Data.chat_type, echo_msg, uid, chat_id, key, iv)
                        
                        # Repeat command - repeat text multiple times
                        if inPuTMsG.strip().startswith('/repeat '):
                            parts = inPuTMsG.strip().split(maxsplit=2)
                            if len(parts) >= 3:
                                try:
                                    times = int(parts[1])
                                    if 1 <= times <= 5:
                                        text = parts[2]
                                        for i in range(times):
                                            repeat_msg = f"[B][C][FFD700]🔁 ({i+1}/{times}): {text}\n"
                                            await safe_send_message(response.Data.chat_type, repeat_msg, uid, chat_id, key, iv)
                                            await asyncio.sleep(0.3)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ Repeat count must be 1-5!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ Usage: /repeat [1-5] [text]\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ Usage: /repeat [1-5] [text]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # Countdown command
                        if inPuTMsG.strip().startswith('/countdown '):
                            try:
                                seconds = int(inPuTMsG.strip().split()[1])
                                if 1 <= seconds <= 10:
                                    for i in range(seconds, 0, -1):
                                        cd_msg = f"[B][C][FF6600]⏳ Countdown: {i}...\n"
                                        await safe_send_message(response.Data.chat_type, cd_msg, uid, chat_id, key, iv)
                                        await asyncio.sleep(1)
                                    end_msg = f"[B][C][00FF00]✅ Time's up!\n"
                                    await safe_send_message(response.Data.chat_type, end_msg, uid, chat_id, key, iv)
                                else:
                                    error_msg = f"[B][C][FF0000]❌ Countdown must be 1-10 seconds!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            except (ValueError, IndexError):
                                error_msg = f"[B][C][FF0000]❌ Usage: /countdown [1-10]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # Joke command
                        if inPuTMsG.strip() == '/joke':
                            import random
                            jokes = [
                                "Why don't scientists trust atoms? Because they make up everything!",
                                "Why did the scarecrow win an award? He was outstanding in his field!",
                                "Why don't eggs tell jokes? They'd crack each other up!",
                                "What do you call a fake noodle? An impasta!",
                                "Why did the math book look sad? Because it had too many problems!"
                            ]
                            joke = random.choice(jokes)
                            joke_msg = f"[B][C][FF66CC]😂 Random Joke:\n[B][C][FFFFFF]{joke}\n"
                            await safe_send_message(response.Data.chat_type, joke_msg, uid, chat_id, key, iv)
                        
                        # Quote command
                        if inPuTMsG.strip() == '/quote':
                            import random
                            quotes = [
                                "The only way to do great work is to love what you do. - Steve Jobs",
                                "Innovation distinguishes between a leader and a follower. - Steve Jobs",
                                "Life is what happens when you're busy making other plans. - John Lennon",
                                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                                "It is during our darkest moments that we must focus to see the light. - Aristotle"
                            ]
                            quote = random.choice(quotes)
                            quote_msg = f"[B][C][FFD700]💭 Inspirational Quote:\n[B][C][FFFFFF]{quote}\n"
                            await safe_send_message(response.Data.chat_type, quote_msg, uid, chat_id, key, iv)
                        
                        # 8-ball command
                        if inPuTMsG.strip().startswith('/8ball '):
                            import random
                            responses = ["Yes", "No", "Maybe", "Definitely", "Not sure", "Ask again later", "Certainly", "No way"]
                            answer = random.choice(responses)
                            ball_msg = f"[B][C][9400D3]🎱 Magic 8-Ball says:\n[B][C][FFFFFF]{answer}\n"
                            await safe_send_message(response.Data.chat_type, ball_msg, uid, chat_id, key, iv)
                        
                        # RPS command - Rock Paper Scissors
                        if inPuTMsG.strip().startswith('/rps '):
                            import random
                            user_choice = inPuTMsG.strip().split()[1].lower()
                            if user_choice in ['rock', 'paper', 'scissors']:
                                bot_choice = random.choice(['rock', 'paper', 'scissors'])
                                if user_choice == bot_choice:
                                    result = "It's a tie!"
                                    color = "FFFF00"
                                elif (user_choice == 'rock' and bot_choice == 'scissors') or \
                                     (user_choice == 'paper' and bot_choice == 'rock') or \
                                     (user_choice == 'scissors' and bot_choice == 'paper'):
                                    result = "You win!"
                                    color = "00FF00"
                                else:
                                    result = "Bot wins!"
                                    color = "FF0000"
                                rps_msg = f"[B][C][{color}]✊ Rock Paper Scissors:\nYou: {user_choice}\nBot: {bot_choice}\nResult: {result}\n"
                                await safe_send_message(response.Data.chat_type, rps_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ Usage: /rps [rock/paper/scissors]\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        
                        # Compliment command
                        if inPuTMsG.strip() == '/compliment':
                            import random
                            compliments = [
                                "You're amazing just the way you are!",
                                "Your smile brightens up the room!",
                                "You're a true friend!",
                                "You're incredibly talented!",
                                "You make a difference in the world!"
                            ]
                            compliment = random.choice(compliments)
                            comp_msg = f"[B][C][FF69B4]💝 Compliment for you:\n[B][C][FFFFFF]{compliment}\n"
                            await safe_send_message(response.Data.chat_type, comp_msg, uid, chat_id, key, iv)
                        
                        if inPuTMsG.strip() == '/status':
                            footer ="""[00FFFA]╔═•══•════════════════•══•═╗
[FF1493]║ ⚡ [B][FFFF00]BOT INFO[FFFF00][/B] ⚡
[00FFFA]║
[FFFF00]║ 👤 Developer    :: [FF1493]Surjo99exe
[32CD32]║ 💻 Status        :: [32CD32]ONLINE
[1E90FF]║ 🛠 Version      :: [1E90FF]ENHANCED V2
[00FFFA]╚═•══•════════════════•══•═╝"""

    


                            await safe_send_message(response.Data.chat_type, footer, uid, chat_id, key, iv)

# IMPROVED TREE-STYLE HELP MENU SYSTEM (Commands in their original menus) 🌳
                        if inPuTMsG.strip().lower() in ("help", "/help", "menu", "/menu", "commands"):
                            print(f"Help command detected from UID: {uid} in chat type: {response.Data.chat_type}")

                            # Header
                            header = f"[b][c]{get_random_color()}Hey User Welcome To Surjo99exe's BOT"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Group Commands ─────
                            group_commands = """[C][B][FFD700]═══⚡ ADVANCED COMMANDS ⚡═══[00AAFF][B]
├─ [00AAFF]⚡Send Likes ✅️✅️
│  └─ [FF0000]/like [uid]
├─ [00AAFF]Create 3-Player Group
│  └─ [FF0000]/3
├─ [00AAFF]Create 5-Player Group
│  └─ [FF0000]/5
├─ [00AAFF]Create 6-Player Group
│  └─ [FF0000]/6
├─ [00AAFF]Invite Player in Team
│  └─ [FF0000]/inv [uid]
├─ [00AAFF]Join Bot in Team
│  └─ [FF0000]/join [team_code]
└─ [00AAFF]Leave Bot Team
   └─ [FF0000]/exit
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, group_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Advanced Commands ─────
                            advanced_commands = """[C][B][800080]═══⚡ ADVANCED COMMANDS ⚡═══[00AAFF][B]
├─ [00AAFF]Start Level up bot
│  └─ [FF0000]/lw [team code]
├─ [00AAFF]Stop level up bot
│  └─ [FF0000]/stop
├─ [00AAFF]Equip Rare Bundle
│  └─ [FF0000]/bundle [code]
├─ [00AAFF]Lag Attack Team
│  └─ [FF0000]/lag [code]
├─ [00AAFF]Stop Lag Attack
│  └─ [FF0000]/stop lag
└─ [00AAFF]Reject Spam
   └─ [FF0000]/reject [uid]
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, advanced_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Emote Commands ─────
                            emote_commands = """[C][B][FF0000]═══⚡ EMOTE COMMANDS ⚡═══[00AAFF][B]
├─ [00AAFF]Send Single Emote
│  └─ [FF0000]/play [uid] [1-410]
├─ [00AAFF]Fast Emote (25x)
│  └─ [FF0000]/fast [uid] [1-410]
├─ [00AAFF]Custom Emote (X Times)
│  └─ [FF0000]/p [uid] [1-410] [X]
├─ [00AAFF]Play 100 level emote
│  └─ [FF0000]/play [uid] 263
├─ [00AAFF]Emote Menu
│  └─ [FF0000]/emote
└─ [00AAFF]Custom Emote (Using Id)
   └─ [FF0000]/e [uid] [id]
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, emote_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Evolution Emote Commands ─────
                            evo_commands = """[C][B][FF0000]═══⚡ EVOLUTION EMOTES ⚡═══[00AAFF][B]
├─ [00AAFF]Send Evolution Emote
│  └─ [FF0000]/evo [uid] [1-21]
├─ [00AAFF]Fast Evo (25x)
│  └─ [FF0000]/evo_fast [uid] [1-21]
├─ [00AAFF]Custom Evo (X times)
│  └─ [FF0000]/evo_c [uid] [1-21] [x]
├─ [00AAFF]Auto Cycle All Evo Emotes
│  └─ [FF0000]/evos [uid]
└─ [00AAFF]Stop Evo Emote Cycle
   └─ [FF0000]/sevos
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, evo_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── AI & Utility Commands ─────
                            ai_commands = """[C][B][FF0000]═══⚡ TOOLS & FUN COMMANDS ⚡═══[00AAFF][B]
├─ [00AAFF]Get player bio by uid
│  └─ [FF0000]/bio [uid]
├─ [00AAFF]Fetch Instagram User Info
│  └─ [FF0000]/ig [username]
├─ [00AAFF]Send custom spam message
│  └─ [FF0000]/ms <text>
├─ [00AAFF]Ask AI Anything
│  └─ [FF0000]/ai [question]
├─ [00AAFF]Current Time
│  └─ [FF0000]/time
├─ [00AAFF]Current Date
│  └─ [FF0000]/date
├─ [00AAFF]Bot UID
│  └─ [FF0000]/uid
├─ [00AAFF]Server Info
│  └─ [FF0000]/server
├─ [00AAFF]Ping Test
│  └─ [FF0000]/ping
├─ [00AAFF]Calculator
│  └─ [FF0000]/calc [expression]
├─ [00AAFF]Random Number
│  └─ [FF0000]/random [min] [max]
├─ [00AAFF]Coin Flip
│  └─ [FF0000]/coin
├─ [00AAFF]Dice Roll
│  └─ [FF0000]/dice
├─ [00AAFF]Bot Uptime
│  └─ [FF0000]/uptime
├─ [00AAFF]Echo Message
│  └─ [FF0000]/echo [text]
├─ [00AAFF]Repeat Message
│  └─ [FF0000]/repeat [1-5] [text]
├─ [00AAFF]Countdown Timer
│  └─ [FF0000]/countdown [1-10]
├─ [00AAFF]Auto-join ON
│  └─ [FF0000]/autojoin on
└─ [00AAFF]Auto-join OFF
   └─ [FF0000]/autojoin off
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, ai_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Badges Commands ─────
                            badge_commands = """[C][B][FF0000]═══⚡ BADGE JOIN REQUESTS ⚡═══[00AAFF][B]
├─ [00AAFF]Join Req Craftland Badge
│  └─ [FF0000]/s1 [uid]
├─ [00AAFF]Join Req New V-Badge
│  └─ [FF0000]/s2 [uid]
├─ [00AAFF]Join Req Moderator Badge
│  └─ [FF0000]/s3 [uid]
├─ [00AAFF]Join Req Small V-Badge
│  └─ [FF0000]/s4 [uid]
├─ [00AAFF]Join Req Pro Badge
│  └─ [FF0000]/s5 [uid]
└─ [00AAFF]Join Requests All Badge
   └─ [FF0000]/spam [uid]
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, badge_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                            
                            # ───── Fun & Games Commands ─────
                            fun_commands = """[C][B][FF0000]═══⚡ FUN & GAMES ⚡═══[00AAFF][B]
├─ [00AAFF]Random Joke
│  └─ [FF0000]/joke
├─ [00AAFF]Inspirational Quote
│  └─ [FF0000]/quote
├─ [00AAFF]Magic 8-Ball
│  └─ [FF0000]/8ball [question]
├─ [00AAFF]Rock Paper Scissors
│  └─ [FF0000]/rps [rock/paper/scissors]
└─ [00AAFF]Random Compliment
   └─ [FF0000]/compliment
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, fun_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                                                        # ───── info Commands ─────
                            info_commands = """[C][B][FF0000]═══⚡ TOOLS & FUN COMMANDS ⚡═══[00AAFF][B]
├─ [00AAFF]Get player basic info
│  └─ [FF0000]/info [uid]
├─ [00AAFF]Check account ban status
│  └─ [FF0000]/check [uid]
├─ [00AAFF]Add bot in friend list
│  └─ [FF0000]/add [uid]
├─ [00AAFF]Remove from friend list
│  └─ [FF0000]/remove [uid]
├─ [00AAFF]Spam Friend Requests 
│  └─ [FF0000]/spam_req [uid]
└─ [00AAFF]Gali any friend
   └─ [FF0000]/gali [name]
[00AAFF]━━━━━━━━━━━━[FF0000]"""
                            await safe_send_message(response.Data.chat_type, info_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            
                            footer ="""[00FFFA]╔═•══•════════════════•══•═╗
[FF1493]║ ⚡ [B][FFFF00]BOT INFO[FFFF00][/B] ⚡
[00FFFA]║
[FFFF00]║ 👤 Developer    :: [FF1493]Surjo99exe
[32CD32]║ 💻 Status        :: [32CD32]ONLINE
[1E90FF]║ 🛠 Version      :: [1E90FF]ENHANCED V2
[00FFFA]╚═•══•════════════════•══•═╝"""

    


                            await safe_send_message(response.Data.chat_type, footer, uid, chat_id, key, iv)
                        response = None
                            
                        try:
                            if whisper_writer:
                                whisper_writer.close()
                                await whisper_writer.wait_closed()
                        except:
                            pass
                        finally:
                            whisper_writer = None
                                
                    	
                    	
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)





async def load_accounts():
    # Only run the specific ID requested by the user
    return {"4347380157": "425C71313FF438CB284C079D465116BA55ABE915D77B1093105237C1451F93EF"}

async def MaiiiinE():
    accounts = await load_accounts()
    if not accounts:
        print("No accounts found in accounts.json")
        return None

    account_list = list(accounts.items())
    random.shuffle(account_list)

    PyL = None
    for Uid, Pw in account_list:
        print(f"Attempting login with UID: {Uid}")
        open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
        
        if not open_id or not access_token:
            print(f"Failed login for {Uid}, trying next account...")
            await asyncio.sleep(5)
            continue
        
        PyL = EncRypTMajoRLoGin(open_id , access_token)
        break

    if PyL is None:
        print("All accounts failed. Waiting before retry...")
        await asyncio.sleep(60)
        return None
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") ; return None
    
    MajoRLoGinauTh = DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    # In the MaiiiinE function, find and comment out these print statements:
    os.system('cls')
    print("🔄 Starting TCP Connections...")
    print("📡 Connecting to Free Fire servers...")
    print("🌐 Server connection established")

    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    print("🔐 Authentication successful")
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("ErroR - GeTinG PorTs From LoGin DaTa !") ; return None
    LoGinDaTaUncRypTinG = DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    try:
        OnLineiP , OnLineporT = OnLinePorTs.rsplit(":", 1)
    except ValueError:
        print(f"DEBUG: OnLinePorTs format error: '{OnLinePorTs}'")
        raise
    try:
        ChaTiP , ChaTporT = ChaTPorTs.rsplit(":", 1)
    except ValueError:
        print(f"DEBUG: ChaTPorTs format error: '{ChaTPorTs}'")
        raise
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen, int(TarGeT), int(timestamp)))  

    os.system('cls')
    print("Initializing Surjo99exe Bot...")
    print("┌────────────────────────────────────┐")
    print("│ █████████████░░░░░░░░░░░░░░░░░░ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.5)
    os.system('cls')
    print("Connecting to Free Fire servers...")
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████░░░░░░░░░░░░ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.5)
    os.system('cls')

    print("🤖 Surjo99exe BOT - ONLINE")
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████████████████ │")
    print("└────────────────────────────────────┘")
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Name: {acc_name}")
    print(f"🔹 Status: 🟢 READY")
    print("")
    print("💡 Type /help for commands")
    await asyncio.gather(task1, task2)
    time.sleep(0.5)
    os.system('cls')
    await ready_event.wait()
    await asyncio.sleep(1)

    os.system('cls')
    print(render('Surjo99exe', colors=['white', 'green'], align='center'))
    print('')
    print("🤖 Surjo99exe BOT - ONLINE")
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Name: {acc_name}")
    print(f"🔹 Status: 🟢 READY")
    


def handle_keyboard_interrupt(signum, frame):
    """Clean handling for Ctrl+C"""
    print("\n\n🛑 Bot shutdown requested...")
    print("👋 Thanks for using Surjo99exe")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot shutdown by user")
            print("👋 Thanks for using Surjo99exe!")
            break
        except asyncio.TimeoutError: print("Token ExpiRed ! , ResTartinG")
        except Exception as e:
            import traceback
            # traceback.print_exc()
            if "429" in str(e):
                print("Rate limited (429). Waiting 30 seconds...")
                await asyncio.sleep(30)
            else:
                print(f"ErroR TcP - {e} => ResTarTinG ...")
                await asyncio.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=start_insta_api, daemon=True).start()
    asyncio.run(StarTinG())