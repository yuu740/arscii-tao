import discord
from discord import app_commands
from discord.ext import commands

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/'
}

class Encrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ascii_encrypt", description="Enkripsi kalimat menjadi kode Desimal, Binari, dan Sandi Morse + Rangkuman Gabungan Teks!")
    @app_commands.describe(kalimat="Masukkan kata/kalimat rahasia yang ingin diubah")
    async def ascii_encrypt(self, interaction: discord.Interaction, kalimat: str):
        await interaction.response.defer(ephemeral=False)
        
        result_text = (
            "+-------------------------------------------------------------------------+\n"
            "|                     ASCII ADVANCED TEXT ENCRYPTION                      |\n"
            "+-------------------------------------------------------------------------+\n"
        )
        
        combined_binary = []
        combined_morse = []
        combined_decimal = []
        
        for char in kalimat:
            char_upper = char.upper()
            decimal_val = ord(char)
            binary_val = bin(decimal_val).replace("0b", "").zfill(8)
            morse_val = MORSE_CODE_DICT.get(char_upper, "?")
            
            combined_decimal.append(str(decimal_val))
            combined_binary.append(binary_val)
            combined_morse.append(morse_val)
            
            result_text += f"  Character '{char}' -> Decimal: {str(decimal_val).ljust(3)} | Binary: {binary_val} | Morse: {morse_val}\n"
            
        result_text += (
            "+-------------------------------------------------------------------------+\n"
            "|                       TOTAL GABUNGAN HASIL ENKRIPSI                     |\n"
            "+-------------------------------------------------------------------------+\n"
            f"  • Input Word      : {kalimat}\n"
            f"  • Decimal Stream  : {'-'.join(combined_decimal)}\n"
            f"  • Binary Stream   : {' '.join(combined_binary)}\n"
            f"  • Morse Stream    : {' '.join(combined_morse)}\n"
            "+-------------------------------------------------------------------------+\n\n"
            "========================= CONTOH PENERAPAN (KATA: REI) ===================\n"
            "  Character 'R' -> Decimal Code: 82  | Binary: 01010010 | Morse: .-.\n"
            "  Character 'e' -> Decimal Code: 101 | Binary: 01100101 | Morse: .\n"
            "  Character 'i' -> Decimal Code: 105 | Binary: 01101001 | Morse: ..\n"
            "---------------------------------------------------------------------------\n"
            "  • Gabungan Desimal : 82-101-105\n"
            "  • Gabungan Biner   : 01010010 01100101 01101001\n"
            "  • Gabungan Morse   : .-. . ..\n"
            "==========================================================================="
        )
        
        if len(result_text) > 1900:
            await interaction.followup.send("❌ Input kalimat terlalu panjang! Batasi maksimal 12 karakter saja.")
            return
            
        await interaction.followup.send(content=f"🔒 **[ SECURE SYSTEM DATA CRYPTO-ASCII COMPLETED ]**\n```\n{result_text}\n```")

async def setup(bot):
    await bot.add_cog(Encrypt(bot))