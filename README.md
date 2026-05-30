---
title: ArS-CII Tao Bot
emoji: 🔀
colorFrom: indigo
colorTo: gray
sdk: docker
pinned: false
app_port: 7860
---

# 🔀 (ArS)CII Tao — Ultimate ASCII & Crypto Utility Bot

<(ArS)CII Tao> is a modular Discord bot built on top of Slash Commands designed to bring retro-classic computing aesthetics into modern communication platforms. It operates 100% on a localized graphics parsing engine without any dependencies on external third-party AI APIs, ensuring ultra-fast execution, zero operational costs, and complete immunity to cloud API request bottlenecks.

---

## 🚀 Key Features Pack

### 👤 Profile & Media Art
* **`/ascii_image`** — Converts any attached standard raster image (PNG/JPG) into an optimized, high-density, sharp grayscale ASCII text art.
* **`/ascii_gif`** — Disassembles animated GIF streams locally, extracts frame-by-frame asset arrays, and synthesizes them into an upscaled, animated ASCII text art.
* **`/ascii_pfp`** — Automatically captures a specified user's avatar (fully bypasses Discord's complex dynamic Nitro avatar loops or Server Profiles decoration metadata) and renders it into clean monochrome ASCII sequences.

### 🌐 Cyberpunk Simulation
* **`/ascii_matrix`** — Generates a randomized digital code rain animation sequence (mixing katakana, binary bits, and sci-fi glyphs) styled after *The Matrix* trilogy, looping indefinitely as a `.gif` file.

### 📝 Text Banner & Data Layout
* **`/ascii_banner`** — Transforms plain text input strings into giant retro typographical display banners. Features a mandatory dropdown parameter for choosing among 9 distinct styling fonts (*Slant, Doom, Graffiti, Isometric, etc.*).
* **`/ascii_table`** — Generates a structural, aligned data conversion table patterned directly after an academic *Computer Science* curriculum blueprint.

### 🔒 Information & Security Science
* **`/ascii_encrypt`** — An interactive hacker cipher module that dissects input alphabets into their underlying Decimal codes, 8-bit Binary representations, and International Morse Code translations, topped off with an implementation summary block.
* **`/ascii_info`** — An educational hub detailing the architectural constraints, historical milestones, and origins of the 1963 ASCII standardization.
* **`/ascii_help`** — An interface command center detailing instructions and technical manuals for the entire directory of the bot's features.

---

## 📂 Modular Proyek Directory (Cogs Architecture)

The project leverages `discord.py`'s built-in **Cogs System** to enforce clean encapsulation, isolated environments, and scalable framework maintenance.

```text
arscii-tao/
│
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions automation to sync code to HF Spaces
│
├── cogs/
│   ├── utils.py             # Shared matrix pixel and framework drawing helper utilities
│   ├── image_ascii.py       # Intercepts and parses /ascii_image execution
│   ├── text_banner.py       # Handles /ascii_banner, info, table, and help data strings
│   ├── gif_ascii.py         # Intercepts and renders /ascii_gif structures
│   ├── matrix_rain.py       # Mathematical matrix algorithm engine for /ascii_matrix
│   ├── pfp_ascii.py         # Handles /ascii_pfp (Bypasses dynamic avatar encoding layers)
│   └── encrypt.py           # Encrypts alphabets into cryptography arrays for /ascii_encrypt
│
├── .env                     # Hidden vault for local DISCORD_TOKEN variables
├── bot.py                   # Main orchestrator engine and HTTP Keep-Alive server (Port 7860)
├── Dockerfile               # Container setup blueprint optimized for Hugging Face Linux env
└── requirements.txt         # Package dependency records