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

    @app_commands.command(name="ascii_pfp", description="Ubah foto profil menjadi format teks ASCII Bergerak HD (Anti-Bug Nitro/Dekorasi)!")
    @app_commands.describe(user="Pilih pengguna (Kosongkan jika ingin profil diri sendiri)")
    async def ascii_pfp(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer(ephemeral=False)
        
        # Deteksi profile server lokal jika tersedia
        target_user = interaction.guild.get_member(user.id) if (interaction.guild and user) else (user if user else interaction.user)
        
        # Ambil aset dasar global (Bypass sistem dekorasi profil virtual server)
        avatar_asset = target_user.avatar if target_user.avatar else target_user.default_avatar
        
        # Periksa apakah jenis profilnya animasi melalui hash key Discord murni (Avatar bergerak pasti diawali huruf 'a_')
        is_animated_file = avatar_asset.key.startswith("a_") if avatar_asset.key else False

        try:
            if is_animated_file:
                # JALUR 1: AKUN NITRO ANIMASI BERGERAK MURNI
                # Kita tembak endpoint aset CDN biner lama Discord. Rute ini dijamin 100% menghasilkan ekstensi .gif tradisional tanpa hibrida WebP
                pfp_url = f"https://cdn.discordapp.com/avatars/{target_user.id}/{avatar_asset.key}.gif?size=256"
                
                res = requests.get(pfp_url, timeout=10)
                img = Image.open(io.BytesIO(res.content))
                
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

                gif_stream = create_gif_from_ascii_lines(all_frames_lines, w_chars, h_chars, bg_color="white", text_color="black")
                file_discord = discord.File(fp=gif_stream, filename=f"pfp_animation_{target_user.name}.gif")
                await interaction.followup.send(content=f"🎞️ Seni Avatar Teks Bergerak Berukuran Besar untuk **{target_user.name}**:", file=file_discord)
                
            else:
                # JALUR 2: AKUN STATIS/FOTO BIASA (PNG)
                pfp_url = str(avatar_asset.replace(format="png", size=256).url)
                res = requests.get(pfp_url, timeout=10)
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
                await interaction.followup.send(content=f"👤 Seni Profil Teks ASCII untuk **{target_user.name}**:\n```\n{ascii_img}\n```")
                
        except Exception as e:
            # Skenario penyelamatan terakhir jika rute CDN mengalami kendala intermiten
            try:
                fallback_url = str(target_user.display_avatar.replace(format="png", size=256).url)
                res = requests.get(fallback_url, timeout=10)
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
            except Exception as backup_err:
                await interaction.followup.send(content=f"❌ Gagal total memproses gambar profil. Error: {e} | Fallback Error: {backup_err}")

async def setup(bot):
    await bot.add_cog(PfpAscii(bot))