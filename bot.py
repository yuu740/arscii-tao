import os
import io
import asyncio
import threading
import discord
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- Load Token dari File .env / Hugging Face Secret Fallback ---
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if not DISCORD_TOKEN:
    jalur_secret_hf = "/space_secrets/DISCORD_TOKEN"
    if os.path.exists(jalur_secret_hf):
        with open(jalur_secret_hf, "r") as f:
            DISCORD_TOKEN = f.read().strip()

# =====================================================================
# RAKITAN BOT KUSTOM UNTUK BYPASS DNS JARINGAN CLOUD HUGGING FACE
# =====================================================================
class BadakBypassBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 1. Memaksa internal library aiohttp menggunakan DNS Google & Cloudflare secara agresif
        # Menggunakan kombinasi aiodns + dnspython dari requirements.txt
        resolver = aiohttp.AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])
        connector = aiohttp.TCPConnector(resolver=resolver, use_dns_cache=False)
        
        # Suntikkan konektor bypass ke dalam HTTP Client Session milik bot
        self.http.connector = connector

        # 2. OTOMATIS MEMUAT SELURUH FILE COMMANDS DI DALAM FOLDER COGS
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                # Melewati utils/utility agar tidak ikut terdaftar sebagai command
                if "util" in filename:
                    continue
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"📦 Berhasil memuat modul: {filename}", flush=True)
                except Exception as extension_error:
                    print(f"❌ Gagal memuat modul {filename}. Error: {extension_error}", flush=True)
        
        # 3. Sinkronisasi struktur Slash Command ke Discord
        await self.tree.sync()
        print("🔀 Seluruh Modul Fitur ASCII Cog Berhasil Disinkronisasi Global!", flush=True)

bot = BadakBypassBot()

@bot.event
async def on_ready():
    print(f"✅ (ArS)CII Tao Resmi Online di Cloud Server sebagai {bot.user.name}!", flush=True)


# =====================================================================
# SERVER WEB PALSU UNTUK MENJAGA BOT TETAP HIDUP 24/7 DI HF SPACES
# =====================================================================
class KustomWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = (
            "<html><body style='background:#11111b; color:#a6e3a1; text-align:center; font-family:sans-serif; padding-top:10%;'>"
            "<h1>(ArS)CII Tao Engine Status: ACTIVE 24/7</h1>"
            "<p style='color:#cdd6f4;'>All Localhost Stream Canvas & Cryptography Modules are running smoothly.</p>"
            "</body></html>"
        )
        self.wfile.write(bytes(html, "utf-8"))

    def log_message(self, format, *args):
        return

def jalankan_server_palsu():
    httpd = HTTPServer(('0.0.0.0', 7860), KustomWebHandler)
    print("🌍 Fake Web Server aktif mengamankan Port 7860 Hugging Face!", flush=True)
    httpd.serve_forever()


# =====================================================================
# STRATEGI EKSEKUSI UTAMA (MENGANDALKAN AUTO-RECONNECT INTERNAL)
# =====================================================================
async def main():
    # Jalankan Fake Web Server di thread terpisah (background daemon)
    threading.Thread(target=jalankan_server_palsu, daemon=True).start()
    
    # Biarkan discord.py menangani siklus hidup koneksi & retry internalnya sendiri secara kokoh
    async with bot:
        print("🔄 Memulai proses autentikasi token ke gateway Discord...", flush=True)
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Proses bot dihentikan secara manual.", flush=True)
    except Exception as e:
        print(f"❌ Eror fatal luar pada sistem bot: {e}", flush=True)