"""Create top10.lk logo with copper gradient on black background."""
from PIL import Image, ImageDraw, ImageFont
import math

W = 500
H = 500

# Deep black background
img = Image.new('RGBA', (W, H), (4, 3, 3, 255))
draw = ImageDraw.Draw(img)

# Load fonts
font_bold = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 280)
font_small = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 70)

# Copper gradient colors (dark to bright metallic)
colors = [
    (139, 90, 43),   # dark copper
    (166, 108, 54),  # medium copper  
    (184, 115, 51),  # classic copper
    (201, 135, 65),  # warm copper
    (212, 148, 106), # light copper
    (222, 165, 125), # bright copper
    (232, 184, 138), # lightest copper
]

def make_copper_gradient(w, h, colors):
    """Create a smooth vertical copper gradient."""
    grad = Image.new('RGBA', (w, h))
    gdraw = ImageDraw.Draw(grad)
    segments = len(colors) - 1
    seg_h = h / segments
    for i in range(segments):
        c1 = colors[i]
        c2 = colors[i + 1]
        y0 = int(i * seg_h)
        y1 = int((i + 1) * seg_h)
        for y in range(y0, y1):
            t = (y - y0) / (y1 - y0) if y1 > y0 else 0
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            gdraw.line([(0, y), (w, y)], fill=(r, g, b, 255))
    return grad

# Create copper gradient
copper = make_copper_gradient(W, H, colors)

# --- Render the text ---
# "10" large and bold in center
text_10 = "10"
# "top" above and ".lk" below
text_top = "top"
text_lk = ".lk"

# Get bounding boxes
bb_10 = draw.textbbox((0, 0), text_10, font=font_bold)
bb_top = draw.textbbox((0, 0), text_top, font=font_small)
bb_lk = draw.textbbox((0, 0), text_lk, font=font_small)

w_10 = bb_10[2] - bb_10[0]
h_10 = bb_10[3] - bb_10[1]
w_top = bb_top[2] - bb_top[0]
h_top = bb_top[3] - bb_top[1]
w_lk = bb_lk[2] - bb_lk[0]
h_lk = bb_lk[3] - bb_lk[1]

# Layout: top centered above 10, 10 centered, .lk centered below 10
total_h = h_top + h_10 + h_lk + 20  # 20px spacing
start_y = (H - total_h) // 2

# Positions (centered horizontally)
x_10 = (W - w_10) // 2
x_top = (W - w_top) // 2
x_lk = (W - w_lk) // 2

y_top = start_y
y_10 = y_top + h_top + 10
y_lk = y_10 + h_10 + 10

# --- Apply copper gradient to text via mask ---
def apply_gradient_to_text(draw, text, font, x, y, copper_grad):
    """Create a mask for text and apply gradient colors."""
    # Create a temp image for this text
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    
    mask = Image.new('L', (tw, th), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.text((-bb[0], -bb[1]), text, font=font, fill=255)
    
    # Create colored version
    colored = Image.new('RGBA', (tw, th))
    for py in range(th):
        for px in range(tw):
            if mask.getpixel((px, py)) > 128:
                # Sample copper gradient at this position (relative to overall image)
                img_y = y + py
                c = copper.getpixel((x + px, img_y))
                colored.putpixel((px, py), c)
    
    img.paste(colored, (x, y), mask)

# Render "10" larger and more prominent
# Use the same font but make it bigger through scaling approach
# Actually let's use a two-row approach: 
# "top" on the left of "10" maybe? Or keep vertical stacking.

# Let me try a different layout: "top" above "10" + ".lk" to the right of "10"
# Actually, the classic logo layout is:
#   top
#   10
#   .lk

# Let's make the "10" really big and bold
font_10 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 260)
font_top = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 75)
font_lk = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 75)

bb_10 = draw.textbbox((0, 0), "10", font=font_10)
bb_top = draw.textbbox((0, 0), "top", font=font_top)
bb_lk = draw.textbbox((0, 0), ".lk", font=font_lk)

w_10 = bb_10[2] - bb_10[0]
h_10 = bb_10[3] - bb_10[1]
w_top = bb_top[2] - bb_top[0]
h_top = bb_top[3] - bb_top[1]
w_lk = bb_lk[2] - bb_lk[0]
h_lk = bb_lk[3] - bb_lk[1]

spacing = 8
total_h = h_top + spacing + h_10 + spacing + h_lk
start_y = (H - total_h) // 2 + 10  # slight downward offset

x_10 = (W - w_10) // 2
x_top = (W - w_top) // 2
x_lk = (W - w_lk) // 2

y_top = start_y
y_10 = y_top + h_top + spacing
y_lk = y_10 + h_10 + spacing

# --- Render with gradient texture ---
def render_gradient_text(draw_obj, text, font, x, y, copper_grad, img_target):
    bb = draw_obj.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    
    mask = Image.new('L', (max(tw, 1), max(th, 1)), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.text((-bb[0], -bb[1]), text, font=font, fill=255)
    
    colored = Image.new('RGBA', (max(tw, 1), max(th, 1)))
    for py in range(th):
        for px in range(tw):
            if px < mask.width and py < mask.height and mask.getpixel((px, py)) > 128:
                c = copper_grad.getpixel(((x + px) % W, (y + py) % H))
                colored.putpixel((px, py), c)
    
    img_target.paste(colored, (x, y), mask)

render_gradient_text(draw, "top", font_top, x_top, y_top, copper, img)
render_gradient_text(draw, "10", font_10, x_10, y_10, copper, img)
render_gradient_text(draw, ".lk", font_lk, x_lk, y_lk, copper, img)

# Save as JPEG (convert to RGB)
img_rgb = img.convert('RGB')
img_rgb.save('/opt/data/top10.lk/static/img/logo.jpg', quality=92)
print("Logo created: 500x500")
print(f"File size: {__import__('os').path.getsize('/opt/data/top10.lk/static/img/logo.jpg') / 1024:.0f} KB")
