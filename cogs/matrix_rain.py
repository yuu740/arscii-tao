import random
import discord
from discord import app_commands
from discord.ext import commands
from cogs.utils import create_gif_from_ascii_lines

class MatrixRain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_matrix", description="Generate a large-scale, indefinitely looping digital code rain animation styled after The Matrix!")
    async def ascii_matrix(self, interaction: discord.Interaction):
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

async def setup(bot):
    await bot.add_cog(MatrixRain(bot))