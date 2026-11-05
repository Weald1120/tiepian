"""生成微信分享卡片缩略图 v5：亮黄圆角方形 + 白色圆润饱满「直播贴片」。"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 800
FONT = "C:/Windows/Fonts/msyhbd.ttc"
OUTER = (252, 248, 238)
RADIUS = 176


def glow(size, color, center, radius, alpha):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=color + (alpha,),
    )
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.62))


def plate():
    g = Image.new("RGBA", (S, S), (255, 200, 26, 255))
    g = Image.alpha_composite(g, glow(S, (255, 226, 96), (int(S * 0.32), int(S * 0.26)), 420, 150))
    g = Image.alpha_composite(g, glow(S, (255, 238, 150), (int(S * 0.5), int(S * 0.46)), 320, 70))
    g = Image.alpha_composite(g, glow(S, (255, 186, 20), (int(S * 0.92), int(S * 0.95)), 340, 60))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=RADIUS, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    return g, mask


def text_mask():
    layer = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, 252)
    cells = [((262, 250), "直"), ((538, 250), "播"), ((262, 550), "贴"), ((538, 550), "片")]
    for (cx, cy), ch in cells:
        d.text((cx, cy), ch, font=font, fill=255, anchor="mm")

    layer = layer.filter(ImageFilter.MaxFilter(5))
    layer = layer.filter(ImageFilter.GaussianBlur(5.2))
    layer = layer.point(lambda v: 255 if v >= 128 else 0)
    layer = layer.filter(ImageFilter.GaussianBlur(1.5))
    return layer


card = Image.new("RGBA", (S, S), OUTER + (255,))
g, mask = plate()
card.paste(g, (0, 0), mask)

tm = text_mask()
soft = tm.filter(ImageFilter.GaussianBlur(3.4))
halo = Image.new("RGBA", (S, S), (238, 152, 0, 92))
card = Image.alpha_composite(card, Image.composite(halo, Image.new("RGBA", (S, S), (0, 0, 0, 0)), soft))

ink = Image.new("RGBA", (S, S), (255, 255, 255, 255))
card = Image.alpha_composite(card, Image.composite(ink, Image.new("RGBA", (S, S), (0, 0, 0, 0)), tm))

out = os.path.join(ROOT, "assets", "share-card-v5.jpg")
card.convert("RGB").save(out, "JPEG", quality=93, optimize=True, progressive=True)
card.convert("RGB").resize((66, 66), Image.LANCZOS).save(os.path.join(ROOT, "tools", "prev-v5.png"))
print("saved", os.path.getsize(out), "bytes")
