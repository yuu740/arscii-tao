import io
import requests
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
from cogs.utils import convert_to_text_ascii

class ImageAscii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_image", description="Ubah fotomu menjadi seni teks ASCII murni bergaya HD!")
    @app_commands.describe(gambar="Lampirkan foto yang ingin kamu ubah")
    async def ascii_image(self, interaction: discord.Interaction, gambar: discord.Attachment):
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

async def setup(bot):
    await bot.add_cog(ImageAscii(bot))