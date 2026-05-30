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

    @app_commands.command(name="ascii_encrypt", description="Encrypt a sentence into raw Decimal streams, 8-bit Binary, and International Morse code!")
    @app_commands.describe(kalimat="Enter the secret word or sentence to encrypt")
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
            "|                       TOTAL CIPHER CONSOLIDATION                        |\n"
            "+-------------------------------------------------------------------------+\n"
            f"  • Input Word      : {kalimat}\n"
            f"  • Decimal Stream  : {'-'.join(combined_decimal)}\n"
            f"  • Binary Stream   : {' '.join(combined_binary)}\n"
            f"  • Morse Stream    : {' '.join(combined_morse)}\n"
            "+-------------------------------------------------------------------------+\n\n"
            "======================= IMPLEMENTATION EXAMPLE (WORD: REI) ===============\n"
            "  Character 'R' -> Decimal Code: 82  | Binary: 01010010 | Morse: .-.\n"
            "  Character 'e' -> Decimal Code: 101 | Binary: 01100101 | Morse: .\n"
            "  Character 'i' -> Decimal Code: 105 | Binary: 01101001 | Morse: ..\n"
            "---------------------------------------------------------------------------\n"
            "  • Decimal Stream : 82-101-105\n"
            "  • Binary Stream  : 01010010 01100101 01101001\n"
            "  • Morse Stream   : .-. . ..\n"
            "==========================================================================="
        )
        
        if len(result_text) > 1900:
            await interaction.followup.send("❌ Input string is too long! Please limit to a maximum of 12 characters.")
            return
            
        await interaction.followup.send(content=f"🔒 **[ SECURE SYSTEM DATA CRYPTO-ASCII COMPLETED ]**\n```\n{result_text}\n```")

async def setup(bot):
    await bot.add_cog(Encrypt(bot))