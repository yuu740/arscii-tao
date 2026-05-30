import os
import io
import random
import discord
import requests
import pyfiglet
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# --- Load Token dari File .env ---
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("🔀 Semua Slash Commands ASCII Teks Berhasil Disinkronisasi!")

bot = MyBot()

# Kumpulan karakter teks murni untuk gradasi HD (Dari paling gelap ke paling terang)
ASCII_CHARS = ["@", "#", "W", "M", "B", "8", "&", "q", "w", "m", "k", "b", "d", "p", "o", "a", "h", "*", "O", "0", "Z", "X", "U", "C", "L", "Q", "v", "c", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", '"', "^", "`", "'", ".", " ", " "]

# Font untuk merender text ke format GIF bergerak dengan skala besar
try:
    # Menggunakan font bawaan OS (Courier New) berukuran besar agar hasil GIF tajam dan tidak buram
    FONT_ENGRAVER = ImageFont.truetype("cour.ttf", 20) 
except:
    FONT_ENGRAVER = ImageFont.load_default()

# --- UTILITY FUNCTIONS ---
def convert_to_text_ascii(img_data, target_width=60):
    w, h = img_data.size
    target_height = int(target_width * (h / w) * 0.55)
    img_data = img_data.resize((target_width, target_height)).convert("L")
    
    pixels = img_data.getdata()
    num_chars = len(ASCII_CHARS)
    
    ascii_str = "".join([ASCII_CHARS[int((p / 255) * (num_chars - 1))] for p in pixels])
    lines = [ascii_str[i:(i + target_width)] for i in range(0, len(ascii_str), target_width)]
    return lines

def create_gif_from_ascii_lines(all_frames_lines, width_chars, height_chars, bg_color="black", text_color="green"):
    # Ukuran per karakter diperbesar menjadi 14x24 piksel agar hasil GIF berukuran besar di Discord
    char_w, char_h = 14, 24
    img_w = width_chars * char_w + 20
    img_h = height_chars * char_h + 20
    
    gif_frames = []
    for lines in all_frames_lines:
        frame_img = Image.new("RGB", (img_w, img_h), color=bg_color)
        draw = ImageDraw.Draw(frame_img)
        
        y_offset = 10
        for line in lines:
            draw.text((10, y_offset), line, fill=text_color, font=FONT_ENGRAVER)
            y_offset += char_h
            
        gif_frames.append(frame_img)
        
    out_stream = io.BytesIO()
    if gif_frames:
        gif_frames[0].save(
            out_stream, format="GIF", save_all=True,
            append_images=gif_frames[1:], duration=120, loop=0
        )
    out_stream.seek(0)
    return out_stream


# ==================== FITUR 1: HD IMAGE TO ASCII TEXT ====================
@bot.tree.command(name="ascii_image", description="Ubah fotomu menjadi seni teks ASCII murni bergaya HD!")
@app_commands.describe(gambar="Lampirkan foto yang ingin kamu ubah")
async def ascii_image(interaction: discord.Interaction, gambar: discord.Attachment):
    await interaction.response.defer(ephemeral=False)

    if not gambar.content_type or not gambar.content_type.startswith("image/"):
        await interaction.followup.send("❌ File harus berupa gambar!")
        return

    try:
        res = requests.get(gambar.url)
        img = Image.open(io.BytesIO(res.content))
        
        lines = convert_to_text_ascii(img, target_width=65)
        
        safe_lines = []
        curr_len = 0
        for line in lines:
            clean_line = line.replace("`", "'")
            if curr_len + len(clean_line) + 1 > 1850:
                break
            safe_lines.append(clean_line)
            curr_len += len(clean_line) + 1
            
        ascii_img = "\n".join(safe_lines)
        await interaction.followup.send(f"```\n{ascii_img}\n```")
    except Exception as e:
        await interaction.followup.send(f"❌ Gagal memproses gambar. Error: {e}")


# ==================== FITUR 2: TEXT TO BANNER (REQUIRED CHOICE + NEW FONTS) ====================
@bot.tree.command(name="ascii_banner", description="Ubah teks biasa menjadi spanduk teks ASCII besar dengan variasi gaya!")
@app_commands.describe(teks="Tulis kata bebas", gaya="Pilih bentuk/gaya seni karakter teks (Wajib)")
@app_commands.choices(gaya=[
    app_commands.Choice(name="Standard Retro", value="standard"),
    app_commands.Choice(name="Slant (Miring Keren)", value="slant"),
    app_commands.Choice(name="Doom (Gaya Game Blok)", value="doom"),
    app_commands.Choice(name="Block (Kotak Rapi)", value="block"),
    app_commands.Choice(name="Bubbles (Lingkaran Bulat)", value="bubbles"),
    app_commands.Choice(name="Graffiti (Gaya Jalanan)", value="graffiti"),
    app_commands.Choice(name="Epic Star Wars", value="starwars"),
    app_commands.Choice(name="3D Fly", value="3d_diagonal"),
    app_commands.Choice(name="Isometric", value="isometric1")
])
# Menghapus nilai default (= "standard") membuat opsi ini wajib diisi oleh pengguna di Discord
async def ascii_banner(interaction: discord.Interaction, teks: str, gaya: app_commands.Choice[str]):
    await interaction.response.defer(ephemeral=False)
    try:
        # Mengambil nilai teks pilihan gaya dari objek Choice Discord
        pilihan_font = gaya.value
        fig = pyfiglet.Figlet(font=pilihan_font)
        banner = fig.renderText(teks).replace("`", "'")
        
        if len(banner) > 1900:
            await interaction.followup.send("❌ Struktur teks terlalu raksasa untuk kotak chat Discord!")
            return
        await interaction.followup.send(f"```\n{banner}\n```")
    except Exception as e:
        await interaction.followup.send(f"❌ Gagal membuat banner teks. Error: {e}")


# ==================== FITUR 3: GIF TO TEXT MOVING ANIMATION (BIG SIZE) ====================
@bot.tree.command(name="ascii_gif", description="Ubah animasi GIF menjadi animasi GIF teks ASCII murni berukuran besar!")
@app_commands.describe(gif_file="Lampirkan file animasi GIF")
async def ascii_gif(interaction: discord.Interaction, gif_file: discord.Attachment):
    await interaction.response.defer(ephemeral=False)

    if not gif_file.content_type or "gif" not in gif_file.content_type:
        await interaction.followup.send("❌ File wajib berformat animasi GIF!")
        return

    try:
        res = requests.get(gif_file.url)
        gif = Image.open(io.BytesIO(res.content))
        
        all_frames_lines = []
        w_chars, h_chars = 0, 0
        frame_count = 0
        
        try:
            while True:
                frame = gif.copy()
                lines = convert_to_text_ascii(frame, target_width=52)
                
                w_chars = len(lines[0])
                h_chars = len(lines)
                all_frames_lines.append(lines)
                
                frame_count += 1
                if frame_count >= 20:
                    break
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        gif_stream = create_gif_from_ascii_lines(all_frames_lines, w_chars, h_chars, bg_color="white", text_color="black")
        file_discord = discord.File(fp=gif_stream, filename="animasi_ascii_large.gif")
        
        await interaction.followup.send("✅ Animasi GIF Karakter Teks ASCII berukuran besar berhasil dibuat:", file=file_discord)
    except Exception as e:
        await interaction.followup.send(f"❌ Gagal memproses animasi GIF. Error: {e}")


# ==================== FITUR 4: MOVING MATRIX CODES (BIG SIZE) ====================
@bot.tree.command(name="ascii_matrix", description="Hasilkan animasi hujan kode digital bergerak ukuran besar (Unlimited Looping)!")
async def ascii_matrix(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    
    pool = ["0", "1", "X", "7", "Ø", "Ψ", "ｦ", "ｧ", "ｨ", "ｳ", "ｶ", "ｷ", "ｹ", " ", " ", " "]
    cols, rows = 45, 22
    
    streams = [{"start": random.randint(-15, 0), "len": random.randint(6, 15)} for _ in range(cols)]
    all_frames_lines = []
    
    for frame_idx in range(18):
        grid = []
        for r in range(rows):
            row_chars = []
            for c in range(cols):
                stream = streams[c]
                curr_start = stream["start"] + frame_idx
                if curr_start <= r <= (curr_start + stream["len"]):
                    if r == (curr_start + stream["len"]):
                        row_chars.append("@")
                    else:
                        row_chars.append(random.choice(pool))
                else:
                    row_chars.append(" ")
            grid.append("".join(row_chars))
        all_frames_lines.append(grid)

    gif_stream = create_gif_from_ascii_lines(all_frames_lines, cols, rows, bg_color="black", text_color="#00FF00")
    file_matrix = discord.File(fp=gif_stream, filename="matrix_rain_large.gif")
    
    await interaction.followup.send("🌐 **[ SYSTEM INTRUSION DETECTED — LARGE MATRIX LOOP ]**", file=file_matrix)


# ==================== FITUR 5: AUTOMATIC DETECT AVATAR PFP (FIX WEB ANIMATION) ====================
@bot.tree.command(name="ascii_pfp", description="Ubah foto profil menjadi format teks ASCII (Otomatis mendukung foto & GIF PFP)!")
@app_commands.describe(user="Pilih pengguna (Kosongkan jika ingin profil diri sendiri)")
async def ascii_pfp(interaction: discord.Interaction, user: discord.User = None):
    await interaction.response.defer(ephemeral=False)
    target_user = user if user else interaction.user
    
    is_gif = target_user.display_avatar.is_animated()

    if is_gif:
        # Solusi Utama: Menambahkan parameter '?size=256&format=gif' untuk memaksa rute aset Discord menjadi file GIF asli yang valid
        fixed_pfp_url = str(target_user.display_avatar.replace(format="gif", size=256).url)
        
        try:
            res = requests.get(fixed_pfp_url)
            gif = Image.open(io.BytesIO(res.content))
            all_frames_lines = []
            w_chars, h_chars = 0, 0
            frame_count = 0
            
            try:
                while True:
                    frame = gif.copy()
                    lines = convert_to_text_ascii(frame, target_width=52)
                    w_chars = len(lines[0])
                    h_chars = len(lines)
                    all_frames_lines.append(lines)
                    frame_count += 1
                    if frame_count >= 20:
                        break
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass

            gif_stream = create_gif_from_ascii_lines(all_frames_lines, w_chars, h_chars, bg_color="white", text_color="black")
            file_discord = discord.File(fp=gif_stream, filename=f"pfp_animation_{target_user.name}.gif")
            await interaction.followup.send(content=f"🎞️ Seni Avatar Teks Bergerak Berukuran Besar untuk **{target_user.name}**:", file=file_discord)
        except Exception as e:
            await interaction.followup.send(f"❌ Gagal memproses animasi PFP. Error: {e}")
            
    else:
        # Jika PFP berupa gambar statis
        pfp_url = str(target_user.display_avatar.replace(format="png", size=256).url)
        try:
            res = requests.get(pfp_url)
            img = Image.open(io.BytesIO(res.content))
            lines = convert_to_text_ascii(img, target_width=65)
            
            safe_lines = []
            curr_len = 0
            for line in lines:
                clean_line = line.replace("`", "'")
                if curr_len + len(clean_line) + 1 > 1850:
                    break
                safe_lines.append(clean_line)
                curr_len += len(clean_line) + 1
                
            ascii_img = "\n".join(safe_lines)
            await interaction.followup.send(f"👤 Seni Profil Teks ASCII untuk **{target_user.name}**:\n```\n{ascii_img}\n```")
        except Exception as e:
            await interaction.followup.send(f"❌ Gagal mengubah PFP gambar. Error: {e}")


# --- Jalankan Bot ---
bot.run(DISCORD_TOKEN)