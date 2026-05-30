import os
import io
import discord
import requests
import pyfiglet
from discord import app_commands
from discord.ext import commands
from PIL import Image
from dotenv import load_dotenv

# --- Load Token dari File .env ---
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Inisialisasi Bot dengan Client standar untuk Slash Commands
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("🔀 Slash Commands berhasil disinkronisasi global!")

bot = MyBot()

# Kumpulan karakter untuk konversi gambar & GIF (70 karakter untuk detail maksimal)
ASCII_CHARS = ["$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c", "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", '"', "^", "`", "'", ".", " "]

# --- UTILITY FUNCTIONS UNTUK FOTO & GIF ---
def resize_image(image, new_width=50):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    num_chars = len(ASCII_CHARS)
    characters = "".join([ASCII_CHARS[int((pixel / 255) * (num_chars - 1))] for pixel in pixels])
    return characters


# ==================== FITUR 1: IMAGE TO ASCII (/ascii_image) ====================
@bot.tree.command(name="ascii_image", description="Ubah fotomu menjadi seni teks ASCII yang estetik!")
@app_commands.describe(gambar="Lampirkan foto yang ingin kamu ubah")
async def ascii_image(interaction: discord.Interaction, gambar: discord.Attachment):
    if not gambar.content_type or not gambar.content_type.startswith("image/"):
        await interaction.response.send_message("❌ File yang kamu lampirkan harus berupa gambar (PNG/JPG)!", ephemeral=True)
        return

    await interaction.response.send_message("🎨 *Sedang memahat gambarmu menjadi teks...*")

    try:
        response = requests.get(gambar.url)
        img = Image.open(io.BytesIO(response.content))

        img = resize_image(img)
        img = grayify(img)
        
        ascii_str = pixels_to_ascii(img)
        img_width = img.width
        
        lines = [ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)]
        
        safe_lines = []
        current_length = 0
        is_truncated = False

        for line in lines:
            clean_line = line.replace("`", "'") 
            if current_length + len(clean_line) + 1 > 1850: 
                is_truncated = True
                break
            safe_lines.append(clean_line)
            current_length += len(clean_line) + 1

        ascii_img = "\n".join(safe_lines)
        if is_truncated:
            ascii_img += "\n... (sisa gambar dipotong agar tidak meledakkan limit Discord)"

        await interaction.edit_original_response(content=f"```\n{ascii_img}\n```")
        
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ Gagal memproses gambar. Error: {e}")


# ==================== FITUR 2: TEXT TO BANNER (/ascii_banner) ====================
@bot.tree.command(name="ascii_banner", description="Ubah teks biasa menjadi spanduk teks ASCII besar yang keren!")
@app_commands.describe(teks="Tulis kata yang ingin diubah (Alfabet/Angka)", font="Pilih gaya tulisan ASCII")
@app_commands.choices(font=[
    app_commands.Choice(name="Standard Retro", value="standard"),
    app_commands.Choice(name="Slant (Miring)", value="slant"),
    app_commands.Choice(name="3D-Diagonal", value="3d_diagonal"),
    app_commands.Choice(name="Bubbles (Bulat)", value="bubbles")
])
async def ascii_banner(interaction: discord.Interaction, teks: str, font: str = "standard"):
    # Gunakan defer agar aman dari kendala delay pengiriman Discord
    await interaction.response.defer()
    
    try:
        # Membuat seni teks menggunakan pyfiglet secara lokal
        fig = pyfiglet.Figlet(font=font)
        banner_result = fig.renderText(teks)
        
        # Bersihkan karakter backtick jika ada agar tidak merusak format codeblock Discord
        banner_result = banner_result.replace("`", "'")
        
        # Validasi limit 2000 karakter Discord
        if len(banner_result) > 1900:
            await interaction.followup.send("❌ Teks terlalu panjang atau pilihan font terlalu besar untuk chat Discord!")
            return
            
        await interaction.followup.send(f"```\n{banner_result}\n```")
    except Exception as e:
        await interaction.followup.send(f"❌ Gagal membuat banner teks. Error: {e}")


# ==================== FITUR 3: GIF TO ASCII FILE (/ascii_gif) ====================
@bot.tree.command(name="ascii_gif", description="Ubah animasi GIF menjadi file teks (.txt) berisi tumpukan frame ASCII!")
@app_commands.describe(gif_file="Lampirkan file animasi GIF yang ingin dikonversi")
async def ascii_gif(interaction: discord.Interaction, gif_file: discord.Attachment):
    # Validasi apakah file beneran GIF
    if not gif_file.content_type or "gif" not in gif_file.content_type:
        await interaction.response.send_message("❌ File yang dilampirkan wajib berupa animasi GIF!", ephemeral=True)
        return

    await interaction.response.defer()
    await interaction.followup.send("🎞️ *Sedang memecah frame GIF dan merajutnya menjadi text art lokal...*")

    try:
        # Ambil file GIF dari Discord
        response = requests.get(gif_file.url)
        gif = Image.open(io.BytesIO(response.content))
        
        output_text = "=== MAHA KARYA ANIMASI ASCII ===\n"
        output_text += f"Nama File: {gif_file.filename}\n"
        output_text += "Tips: Matikan 'Word Wrap' di Notepad komputer kamu agar bentuk gambarnya rapi!\n"
        output_text += "================================\n\n"
        
        frame_number = 1
        
        # Melakukan looping ekstraksi frame GIF menggunakan Pillow secara lokal
        try:
            while True:
                # Copy frame aktif saat ini
                frame = gif.copy()
                # Proses frame (Resize ke lebar 45 agar muat di notepad standar & ubah ke hitam putih)
                frame = resize_image(frame, new_width=45)
                frame = grayify(frame)
                
                # Konversi pixel frame ke karakter teks
                ascii_str = pixels_to_ascii(frame)
                img_width = frame.width
                ascii_frame = "\n".join([ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)])
                
                # Susun ke dalam variabel teks raksasa
                output_text += f"[ FRAME {frame_number} ]\n"
                output_text += ascii_frame + "\n"
                output_text += "-" * img_width + "\n\n"
                
                frame_number += 1
                # Batasi maksimal 40 frame agar ukuran file teks tidak terlalu membengkak
                if frame_number > 40:
                    output_text += "... (Frame dibatasi hingga 40 frame terdepan demi ukuran file)\n"
                    break
                    
                # Berpindah ke frame GIF berikutnya
                gif.seek(gif.tell() + 1)
        except EOFError:
            # Loop akan otomatis berhenti ke sini jika frame GIF asli memang sudah habis
            pass

        # Mengubah string teks menjadi file virtual di memori RAM (.txt) tanpa mengotori harddisk
        text_stream = io.BytesIO(output_text.encode('utf-8'))
        discord_file = discord.File(fp=text_stream, filename="animasi_ascii_art.txt")
        
        # Kirim file .txt ke channel Discord
        await interaction.followup.send("✅ Pemrosesan GIF selesai! Silakan unduh file teks mahakaryamu di bawah ini:", file=discord_file)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Gagal memproses file GIF. Error: {e}")


# --- Event saat bot berhasil online ---
@bot.event
async def on_ready():
    print(f"✅ Bot Berhasil Online sebagai {bot.user.name}!")

# --- Jalankan Bot ---
bot.run(DISCORD_TOKEN)