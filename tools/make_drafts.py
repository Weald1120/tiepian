"""本地候选稿：8 个方向的分享卡片图标。只生成，不上线。"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "_draft")
os.makedirs(OUT, exist_ok=True)
S = 800
VF = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
LABEL = "C:/Windows/Fonts/msyh.ttc"
WHITE = (255, 255, 255)
WARM = (255, 250, 232)
CREAM = (251, 246, 234)


def font(size, weight="Black"):
    f = ImageFont.truetype(VF, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def rmask(box, radius, blur=1.5):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=radius, fill=255)
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    return m


def solid(box, radius, color, blur=1.5):
    layer = Image.new("RGBA", (S, S), color + (255,))
    layer.putalpha(rmask(box, radius, blur))
    return layer


def glow(color, center, radius, alpha):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=color + (alpha,),
    )
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.62))


def yellow(base, lights=True):
    g = Image.new("RGBA", (S, S), base + (255,))
    if lights:
        g = Image.alpha_composite(g, glow((255, 228, 110), (int(S * .3), int(S * .24)), 420, 120))
        g = Image.alpha_composite(g, glow((255, 240, 160), (int(S * .5), int(S * .48)), 320, 48))
        g = Image.alpha_composite(g, glow((255, 190, 30), (int(S * .94), int(S * .96)), 340, 34))
    return g


def base_plate(base, radius=182, lights=True, outer=CREAM, box=None):
    """黄块（含柔光）先裁进圆角，再贴到外底，避免光晕污染四角。"""
    box = box or [0, 0, S - 1, S - 1]
    m = rmask(box, radius, 1.5)
    card = Image.new("RGBA", (S, S), outer + (255,))
    card.paste(yellow(base, lights), (0, 0), m)
    return card


def text(cells, size, color=WHITE, soften=1.1, weight="Black"):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    f = font(size, weight)
    for (cx, cy), ch in cells:
        d.text((cx, cy), ch, font=f, fill=255, anchor="mm")
    if soften:
        m = m.filter(ImageFilter.GaussianBlur(soften))
    layer = Image.new("RGBA", (S, S), color + (255,))
    layer.putalpha(m)
    return layer


def finish(name, card):
    p = os.path.join(OUT, name + ".jpg")
    card.convert("RGB").save(p, "JPEG", quality=93, optimize=True, progressive=True)
    print("  ", name, os.path.getsize(p))


G2 = [((264, 252), "直"), ((536, 252), "播"), ((264, 548), "贴"), ((536, 548), "片")]

# A 纯色极简
c = base_plate((255, 205, 44), lights=False)
c = Image.alpha_composite(c, text(G2, 238))
finish("A-纯色极简", c)

# B 奶油留白
c = Image.new("RGBA", (S, S), CREAM + (255,))
c.paste(yellow((255, 214, 70), False), (0, 0), rmask([78, 78, 722, 722], 158))
small = [((288, 290), "直"), ((512, 290), "播"), ((288, 510), "贴"), ((512, 510), "片")]
c = Image.alpha_composite(c, text(small, 208))
finish("B-奶油留白", c)

# C 四宫格
c = base_plate((255, 212, 72), lights=False)
for x, y in [(104, 104), (436, 104), (104, 436), (436, 436)]:
    c = Image.alpha_composite(c, solid([x, y, x + 260, y + 260], 68, (240, 158, 6)))
quad = [((234, 234), "直"), ((566, 234), "播"), ((234, 566), "贴"), ((566, 566), "片")]
c = Image.alpha_composite(c, text(quad, 196))
finish("C-四宫格", c)

# D 柔光玻璃
c = base_plate((255, 205, 44), lights=True)
panel = Image.new("RGBA", (S, S), (216, 134, 0, 72))
panel.putalpha(rmask([96, 96, 704, 704], 132).point(lambda v: int(v * 0.30)))
c = Image.alpha_composite(c, panel)
c = Image.alpha_composite(c, text(G2, 232))
finish("D-柔光玻璃", c)

# E 横排
c = base_plate((255, 205, 44), lights=False)
c = Image.alpha_composite(c, text([((400, 370), "直播贴片")], 168))
c = Image.alpha_composite(c, solid([340, 506, 460, 522], 8, WHITE, 0.8))
finish("E-横排", c)

# F 大字撑满
c = base_plate((255, 198, 28), lights=True)
big = [((260, 250), "直"), ((540, 250), "播"), ((260, 550), "贴"), ((540, 550), "片")]
c = Image.alpha_composite(c, text(big, 276))
finish("F-大字撑满", c)

# G 暖白字 + 软浮影
c = base_plate((255, 202, 34), lights=False)
shadow_mask = text(G2, 238, color=(255, 255, 255)).getchannel("A").filter(ImageFilter.GaussianBlur(12))
shadow = Image.new("RGBA", (S, S), (196, 118, 0, 120))
shadow.putalpha(shadow_mask.point(lambda v: int(v * 0.5)))
c = Image.alpha_composite(c, shadow)
c = Image.alpha_composite(c, text(G2, 238, color=WARM))
finish("G-暖白柔字", c)

# H 内描边印章
c = base_plate((255, 205, 44), lights=False)
ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(ring).rounded_rectangle([88, 88, 712, 712], radius=140, outline=(255, 255, 255, 165), width=7)
c = Image.alpha_composite(c, ring)
c = Image.alpha_composite(c, text(G2, 218))
finish("H-内描边", c)

# 拼版对比
names = ["A-纯色极简", "B-奶油留白", "C-四宫格", "D-柔光玻璃", "E-横排", "F-大字撑满", "G-暖白柔字", "H-内描边"]
cell, gap, pad, cap = 300, 22, 32, 38
W = pad * 2 + cell * 4 + gap * 3
H = pad * 2 + (cell + cap) * 2 + gap
sheet = Image.new("RGB", (W, H), (245, 244, 240))
sd = ImageDraw.Draw(sheet)
lf = ImageFont.truetype(LABEL, 19)
for i, n in enumerate(names):
    r, col = divmod(i, 4)
    x = pad + col * (cell + gap)
    y = pad + r * (cell + cap + gap)
    im = Image.open(os.path.join(OUT, n + ".jpg")).convert("RGB").resize((cell, cell), Image.LANCZOS)
    sheet.paste(im, (x, y))
    sd.text((x + 2, y + cell + 9), f"{chr(65 + i)}  {n.split('-', 1)[1]}", font=lf, fill=(60, 55, 48))
p = os.path.join(OUT, "00-八版对比.jpg")
sheet.save(p, "JPEG", quality=93, optimize=True)
print("  contact sheet", os.path.getsize(p))
