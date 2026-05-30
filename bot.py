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
    # Jika dideploy di HF, rahasia (Secret) dibaca dari jalur file enkripsi ini
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
        resolver = aiohttp.AsyncResolver(nameservers=["8.8.8.8", "1.1.1.1"])
        connector = aiohttp.TCPConnector(resolver=resolver, use_dns_cache=False)
        
        # Suntikkan konektor bypass ke dalam HTTP Client Session milik bot
        self.http.connector = connector

        # 2. Otomatis membaca dan memuat seluruh modul berkas perintah di folder cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                # Melewati utils/utility agar tidak ikut terdaftar sebagai command
                if "util" in filename:
                    continue
                await self.load_extension(f'cogs.{filename[:-3]}')
        
        # 3. Sinkronisasi struktur Slash Command ke Discord
        await self.tree.sync()
        print("🔀 Semua Modul Fitur ASCII Cog Berhasil Disinkronisasi via Bypass Connector!", flush=True)

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
            "<p style='color:#cdd6f4;'>Localhost Stream Canvas & GIF Generator is running smoothly.</p>"
            "</body></html>"
        )
        self.wfile.write(bytes(html, "utf-8"))

    # Menonaktifkan log terminal bawaan http.server agar konsol bersih dari spam request HF ping
    def log_message(self, format, *args):
        return

def jalankan_server_palsu():
    # Hugging Face Spaces mewajibkan aplikasi membuka port HTTP di angka 7860
    httpd = HTTPServer(('0.0.0.0', 7860), KustomWebHandler)
    print("🌍 Fake Web Server aktif mengamankan Port 7860 Hugging Face!", flush=True)
    httpd.serve_forever()


# =====================================================================
# LOGIKA STRATEGI RETRY REKONEKSI OTOMATIS GANGGUAN CLOUD
# =====================================================================
async def start_bot_dengan_retry():
    while True:
        try:
            print("🔄 Mencoba mengetuk pintu server Discord...", flush=True)
            await bot.start(DISCORD_TOKEN)
        except Exception as e:
            print(f"⚠️ Gagal connect karena blokir/delay jaringan ({e}). Mengulang dalam 10 detik...", flush=True)
            await asyncio.sleep(10)

async def main():
    # Jalankan Fake Web Server di thread terpisah (background daemon)
    threading.Thread(target=jalankan_server_palsu, daemon=True).start()
    
    async with bot:
        await start_bot_dengan_retry()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Eror fatal luar pada sistem bot: {e}", flush=True)