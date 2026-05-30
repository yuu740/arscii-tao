import io
from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = ["@", "#", "W", "M", "B", "8", "&", "q", "w", "m", "k", "b", "d", "p", "o", "a", "h", "*", "O", "0", "Z", "X", "U", "C", "L", "Q", "v", "c", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", '"', "^", "`", "'", ".", " ", " "]

try:
    FONT_ENGRAVER = ImageFont.truetype("cour.ttf", 20)
except:
    FONT_ENGRAVER = ImageFont.load_default()

def convert_to_text_ascii(img_data, target_width=60):
    w, h = img_data.size
    target_height = int(target_width * (h / w) * 0.55)
    img_data = img_data.resize((target_width, target_height)).convert("L")
    
    pixels = img_data.getdata()
    num_chars = len(ASCII_CHARS)
    
    ascii_str = "".join([ASCII_CHARS[int((p / 255) * (num_chars - 1))] for p in pixels])
    lines = [ascii_str[i:(i + target_width)] for i in range(0, len(ascii_str), target_width)]
    return lines

def create_gif_from_ascii_lines(all_frames_lines, width_chars, height_chars, bg_color="black", text_color="green"):
    char_w, char_h = 14, 24
    img_w = width_chars * char_w + 20
    img_h = height_chars * char_h + 20
    
    gif_frames = []
    for lines in all_frames_lines:
        frame_img = Image.new("RGB", (img_w, img_h), color=bg_color)
        draw = ImageDraw.Draw(frame_img)
        
        y_offset = 10
        for line in lines:
            draw.text((10, y_offset), line, fill=text_color, font=FONT_ENGRAVER)
            y_offset += char_h
            
        gif_frames.append(frame_img)
        
    out_stream = io.BytesIO()
    if gif_frames:
        gif_frames[0].save(
            out_stream, format="GIF", save_all=True,
            append_images=gif_frames[1:], duration=120, loop=0
        )
    out_stream.seek(0)
    return out_stream

async def setup(bot):
    # Menyediakan kelas kosong agar sistem registrasi extension tidak error
    pass