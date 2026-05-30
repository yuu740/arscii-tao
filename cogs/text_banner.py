import discord
import pyfiglet
from discord import app_commands
from discord.ext import commands

class TextBanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_banner", description="Transform plain text into giant typographical retro layout display banners!")
    @app_commands.describe(teks="Enter your word", gaya="Choose the explicit structure font style (Required)")
    @app_commands.choices(gaya=[
        app_commands.Choice(name="Standard Retro", value="standard"),
        app_commands.Choice(name="Slant (Cool Slanted)", value="slant"),
        app_commands.Choice(name="Doom (Bold Gaming Blocks)", value="doom"),
        app_commands.Choice(name="Block (Clean Boxes)", value="block"),
        app_commands.Choice(name="Bubbles (Rounded Circles)", value="bubbles"),
        app_commands.Choice(name="Graffiti (Street Art Layout)", value="graffiti"),
        app_commands.Choice(name="Epic Star Wars", value="starwars"),
        app_commands.Choice(name="3D Fly", value="3d_diagonal"),
        app_commands.Choice(name="Isometric", value="isometric1")
    ])
    async def ascii_banner(self, interaction: discord.Interaction, teks: str, gaya: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=False)
        try:
            pilihan_font = gaya.value
            fig = pyfiglet.Figlet(font=pilihan_font)
            banner = fig.renderText(teks).replace("`", "'")
            
            if len(banner) > 1900:
                await interaction.followup.send("❌ Structure banner is too large for a Discord chat block!")
                return
            await interaction.followup.send(f"```\n{banner}\n```")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to construct banner text. Error: {e}")

    @app_commands.command(name="ascii_table", description="Print an aligned character-to-binary data blueprint schema!")
    async def ascii_table(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        it_lesson_table = (
            "+---------+---------+------+-------------------------+\n"
            "| Decimal |   Hex   | Char |      Description        |\n"
            "+---------+---------+------+-------------------------+\n"
            "|    0    |   00    | [NL] | Null Character          |\n"
            "|   32    |   20    | [SP] | Space (Empty Gap)       |\n"
            "|   33    |   21    |  !   | Exclamation Mark        |\n"
            "|   35    |   23    |  #   | Number Sign / Hashtag   |\n"
            "|   36    |   24    |  $   | Dollar Sign             |\n"
            "|   42    |   2A    |  * | Asterisk / Star Symbol  |\n"
            "|   48    |   30    |  0   | Number Zero             |\n"
            "|   64    |   40    |  @   | At Sign Symbol          |\n"
            "|   65    |   41    |  A   | Uppercase Letter A      |\n"
            "|   97    |   61    |  a   | Lowercase Letter a      |\n"
            "|   126   |   7E    |  ~   | Tilde Operator          |\n"
            "+---------+---------+------+-------------------------+"
        )
        await interaction.followup.send(f"📊 **[ IT ACADEMIC ACADEMY: COMPUTER ASCII BLUEPRINT ]**\n```\n{it_lesson_table}\n```")

    @app_commands.command(name="ascii_info", description="Read about the technical origins, constraints, and blueprints of the ASCII standard.")
    async def ascii_info(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        educational_history = (
            "+-----------------------------------------------------------------+\n"
            "|                    HISTORICAL BRIEF OF ASCII                    |\n"
            "+-----------------------------------------------------------------+\n"
            "  ASCII (American Standard Code for Information Interchange)      \n"
            "  is a 7-bit character encoding architecture officially established \n"
            "  in 1963 by the ASA committee (now known as ANSI).               \n"
            "                                                                  \n"
            "  Early Architectural Milestones:                                 \n"
            "  In early telecommunications, computing systems lacked a uniform \n"
            "  binary representation framework. ASCII bridged this gap, text   \n"
            "  interchange protocols became unified (A = 65, Space = 32, etc.) \n"
            "                                                                  \n"
            "  Evolution into Monochromatic Art (ASCII Art):                   \n"
            "  Before modern raster rendering microprocessors were introduced, \n"
            "  network engineers leveraged the structural density variations    \n"
            "  of fixed-width monospace fonts (such as high density '@' symbols\n"
            "  versus low density '.' dots) to sketch shaded geometry outlines. \n"
            "                                                                  \n"
            "  On modern platforms like Discord, utilizing uncompressed raw    \n"
            "  character streams preserves the clean, nostalgic elegance of     \n"
            "  early computer science aesthetics.                              \n"
            "+-----------------------------------------------------------------+"
        )
        await interaction.followup.send(f"ℹ️ **[ KNOWLEDGE CENTER: WHAT IS ASCII? ]**\n```\n{educational_history}\n```")

    @app_commands.command(name="ascii_help", description="Review a comprehensive instruction manual detailing every interactive command.")
    async def ascii_help(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        help_menu = (
            "=========================================================\n"
            "              (ArS)CII TAO UTILITY COMMANDS MENU         \n"
            "=========================================================\n"
            " 1. /ascii_image   -> Converts raster images (JPG/PNG) into text arts\n"
            " 2. /ascii_banner  -> Builds prominent typography layouts (9 styles)\n"
            " 3. /ascii_gif     -> Converts animated files into large ASCII GIFs\n"
            " 4. /ascii_matrix  -> Spawns indefinitely moving code rain ciphers\n"
            " 5. /ascii_pfp     -> Parses users profile avatar layers into ASCII\n"
            " 6. /ascii_table   -> Prints unified data metrics blueprint lists\n"
            " 7. /ascii_encrypt -> Translates input lines into hexadecimal ciphers\n"
            " 8. /ascii_info    -> Educational reference catalog for ASCII theories\n"
            " 9. /ascii_help    -> Launches this main system handbook interface\n"
            "========================================================="
        )
        await interaction.followup.send(f"📋 **[ COMMAND CENTER INTERFACE MANUAL ]**\n```\n{help_menu}\n```")

async def setup(bot):
    await bot.add_cog(TextBanner(bot))