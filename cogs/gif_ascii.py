import io
import requests
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
from cogs.utils import convert_to_text_ascii, create_gif_from_ascii_lines

class GifAscii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_gif", description="Ubah animasi GIF menjadi animasi GIF teks ASCII murni berukuran besar!")
    @app_commands.describe(gif_file="Lampirkan file animasi GIF")
    async def ascii_gif(self, interaction: discord.Interaction, gif_file: discord.Attachment):
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

async def setup(bot):
    await bot.add_cog(GifAscii(bot))