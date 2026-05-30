import discord
import pyfiglet
import platform
from discord import app_commands
from discord.ext import commands

class TextBanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_banner", description="Ubah teks biasa menjadi spanduk teks ASCII besar dengan variasi gaya!")
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
    async def ascii_banner(self, interaction: discord.Interaction, teks: str, gaya: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=False)
        try:
            pilihan_font = gaya.value
            fig = pyfiglet.Figlet(font=pilihan_font)
            banner = fig.renderText(teks).replace("`", "'")
            
            if len(banner) > 1900:
                await interaction.followup.send("❌ Struktur teks terlalu raksasa untuk kotak chat Discord!")
                return
            await interaction.followup.send(f"```\n{banner}\n```")
        except Exception as e:
            await interaction.followup.send(f"❌ Gagal membuat banner teks. Error: {e}")

    @app_commands.command(name="ascii_table", description="Cetak tabel perbandingan kode biner komputer Science resmi bertema ASCII!")
    async def ascii_table(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        it_lesson_table = (
            "+---------+---------+------+-------------------------+\n"
            "| Decimal |   Hex   | Char |      Description        |\n"
            "+---------+---------+------+-------------------------+\n"
            "|    0    |   00    | [NL] | Null Character          |\n"
            "|   32    |   20    | [SP] | Space (Spasi Kosong)    |\n"
            "|   33    |   21    |  !   | Exclamation Mark        |\n"
            "|   35    |   23    |  #   | Number Sign / Hashtag   |\n"
            "|   36    |   24    |  $   | Dollar Sign             |\n"
            "|   42    |   2A    |  * | Asterisk / Bintang      |\n"
            "|   48    |   30    |  0   | Number Zero             |\n"
            "|   64    |   40    |  @   | At Sign Symbol          |\n"
            "|   65    |   41    |  A   | Uppercase Letter A      |\n"
            "|   97    |   61    |  a   | Lowercase Letter a      |\n"
            "|   126   |   7E    |  ~   | Tilde Operator          |\n"
            "+---------+---------+------+-------------------------+"
        )
        await interaction.followup.send(f"📊 **[ IT ACADEMIC ACADEMY: COMPUTER ASCII BLUEPRINT ]**\n```\n{it_lesson_table}\n```")

    @app_commands.command(name="ascii_info", description="Edukasi sejarah & asal-usul lahirnya standar pengkodean karakter ASCII!")
    async def ascii_info(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        educational_history = (
            "+-----------------------------------------------------------------+\n"
            "|                    HISTORICAL BRIEF OF ASCII                    |\n"
            "+-----------------------------------------------------------------+\n"
            "  ASCII (American Standard Code for Information Interchange)      \n"
            "  adalah sistem pengkodean karakter berbasis 7-bit yang resmi     \n"
            "  tercetus pada tahun 1963 oleh Komite ASA (sekarang ANSI).       \n"
            "                                                                  \n"
            "  Sejarah Awal:                                                   \n"
            "  Dahulu, komputer antar pabrik memiliki bahasa biner berbeda.   \n"
            "  ASCII diciptakan agar machines telegraf dan komputer di dunia   \n"
            "  memiliki satu standar angka biner yang seragam untuk huruf     \n"
            "  (A = 65, Spasi = 32, dll).                                      \n"
            "                                                                  \n"
            "  Mengapa Menjadi Seni (ASCII Art) di Discord?                    \n"
            "  Pada era internet purba (sebelum kartu grafis penampil gambar   \n"
            "  ditemukan), para engineer memanfaatkan kepekatan visual font    \n"
            "  monospace (seperti huruf @ yang padat vs titik . yang tipis)    \n"
            "  untuk memahat bayangan gambar objek fiktif di layar monitor.     \n"
            "                                                                  \n"
            "  Di platform modern seperti Discord, implementasi seni tebal     \n"
            "  karakter ASCII murni mengembalikan estetika komputasi retro     \n"
            "  klasik yang ringan namun bernilai artistik sangat tinggi.       \n"
            "+-----------------------------------------------------------------+"
        )
        await interaction.followup.send(f"ℹ️ **[ KNOWLEDGE CENTER: WHAT IS ASCII? ]**\n```\n{educational_history}\n```")

    @app_commands.command(name="ascii_help", description="Tampilkan panduan interaktif seluruh daftar command bot ASCII Tao!")
    async def ascii_help(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        help_menu = (
            "=========================================================\n"
            "              (ArS)CII TAO UTILITY COMMANDS MENU         \n"
            "=========================================================\n"
            " 1. /ascii_image   -> Mengubah foto (JPG/PNG) jadi Seni Teks HD\n"
            " 2. /ascii_banner  -> Membuat spanduk kata besar (9 Gaya Font)\n"
            " 3. /ascii_gif     -> Mengubah animasi GIF jadi Teks GIF Besar\n"
            " 4. /ascii_matrix  -> Hujan kode hacker Matrix bergerak Unlimited\n"
            " 5. /ascii_pfp     -> Render otomatis Foto/GIF Profil User ke ASCII\n"
            " 6. /ascii_table   -> Tampilkan tabel data biner IT resmi komputasi\n"
            " 7. /ascii_encrypt -> Terjemahkan kata rahasia menjadi kode biner\n"
            " 8. /ascii_info    -> Edukasi lengkap sejarah lahirnya teori ASCII\n"
            " 9. /ascii_help    -> Menu pusat panduan pintasan bot ini\n"
            "========================================================="
        )
        await interaction.followup.send(f"📋 **[ COMMAND CENTER INTERFACE MANUAL ]**\n```\n{help_menu}\n```")

async def setup(bot):
    await bot.add_cog(TextBanner(bot))