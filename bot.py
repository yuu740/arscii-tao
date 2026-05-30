import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Otomatis membaca dan memuat seluruh berkas Python di dalam folder cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        
        await self.tree.sync()
        print("🔀 Semua Modul Fitur ASCII Cog Berhasil Disinkronisasi Global!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"✅ (ArS)CII Tao Resmi Online sebagai {bot.user.name}!")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)