import io
import requests
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
from cogs.utils import convert_to_text_ascii, create_gif_from_ascii_lines

class PfpAscii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_pfp", description="Ubah foto profil menjadi format teks ASCII (100% Kebal Bug Nitro/Dekorasi)!")
    @app_commands.describe(user="Pilih pengguna (Kosongkan jika ingin profil diri sendiri)")
    async def ascii_pfp(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer(ephemeral=False)
        
        # Deteksi profile server lokal jika tersedia
        target_user = interaction.guild.get_member(user.id) if (interaction.guild and user) else (user if user else interaction.user)
        
        # --- STRATEGI DEBUG 1: Ambil data animasi dasar ---
        is_animated_avatar = target_user.display_avatar.is_animated()
        
        # Bangun URL dasar. Jika terdeteksi animasi dari Discord, paksa rute ke format .gif murni
        if is_animated_avatar:
            pfp_url = str(target_user.display_avatar.replace(format="gif", size=256).url)
        else:
            pfp_url = str(target_user.display_avatar.replace(format="png", size=256).url)
            
        try:
            # Unduh data biner dari Discord CDN
            res = requests.get(pfp_url, timeout=10)
            
            # --- STRATEGI DEBUG 2: Cek tipe konten via Header HTTP (Bypass Pillow) ---
            content_type = res.headers.get('Content-Type', '').lower()
            
            # Jika di header HTTP mengandung kata 'gif', kita anggap ini berkas animasi
            is_gif_animation = "gif" in content_type or is_animated_avatar

            image_bytes = io.BytesIO(res.content)
            
            # Membuka gambar menggunakan Pillow dalam blok pengaman
            img = Image.open(image_bytes)
            
            if is_gif_animation:
                # JALUR ANIMASI (GIF/WebP Bergerak)
                all_frames_lines = []
                w_chars, h_chars = 0, 0
                frame_count = 0
                
                try:
                    while True:
                        frame = img.copy()
                        lines = convert_to_text_ascii(frame, target_width=52)
                        w_chars = len(lines[0])
                        h_chars = len(lines)
                        all_frames_lines.append(lines)
                        frame_count += 1
                        if frame_count >= 20:
                            break
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass

                # Pastikan ada frame yang berhasil di-render
                if not all_frames_lines:
                    raise ValueError("Gagal mengekstrak frame dari avatar animasi.")

                gif_stream = create_gif_from_ascii_lines(all_frames_lines, w_chars, h_chars, bg_color="white", text_color="black")
                file_discord = discord.File(fp=gif_stream, filename=f"pfp_animation_{target_user.name}.gif")
                await interaction.followup.send(content=f"🎞️ Seni Avatar Teks Bergerak Berukuran Besar untuk **{target_user.name}**:", file=file_discord)
                
            else:
                # JALUR STATIS (Gambar PNG/JPG Biasa)
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
                await interaction.followup.send(content=f"👤 Seni Profil Teks ASCII untuk **{target_user.name}**:\n```\n{ascii_img}\n```")
                
        except Exception as e:
            # Jika skenario di atas masih gagal karena format hibrida aneh, gunakan emergency fallback (Paksa jadikan PNG statis)
            try:
                emergency_url = str(target_user.display_avatar.replace(format="png", size=256).url)
                res = requests.get(emergency_url, timeout=10)
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
                await interaction.followup.send(content=f"👤 [Emergency Fallback] Seni Profil Teks ASCII untuk **{target_user.name}**:\n```\n{ascii_img}\n```")
            except Exception as emergency_error:
                await interaction.followup.send(content=f"❌ Gagal memproses data gambar profil. Error Utama: {e} | Emergency Error: {emergency_error}")

async def setup(bot):
    await bot.add_cog(PfpAscii(bot))