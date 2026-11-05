"""生成微信分享卡片缩略图 v4：圆角方形 + 圆润饱满的「直播贴片」文字标。"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 800
FONT = "C:/Windows/Fonts/msyhbd.ttc"
INK = (43, 27, 5)
OUTER = (250, 245, 234)
RADIUS = 172


def glow(size, color, center, radius, alpha):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=color + (alpha,),
    )
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.62))


def plate():
    g = Image.new("RGBA", (S, S), (246, 183, 12, 255))
    g = Image.alpha_composite(g, glow(S, (255, 210, 77), (int(S * 0.32), int(S * 0.26)), 400, 168))
    g = Image.alpha_composite(g, glow(S, (255, 224, 128), (int(S * 0.5), int(S * 0.48)), 310, 72))
    g = Image.alpha_composite(g, glow(S, (232, 156, 0), (int(S * 0.92), int(S * 0.95)), 340, 98))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=RADIUS, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    return g, mask


def text_mask():
    layer = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, 246)
    cells = [((264, 250), "直"), ((536, 250), "播"), ((264, 550), "贴"), ((536, 550), "片")]
    for (cx, cy), ch in cells:
        d.text((cx, cy), ch, font=font, fill=255, anchor="mm")

    layer = layer.filter(ImageFilter.MaxFilter(3))
    layer = layer.filter(ImageFilter.GaussianBlur(5.0))
    layer = layer.point(lambda v: 255 if v >= 130 else 0)
    layer = layer.filter(ImageFilter.GaussianBlur(1.5))
    return layer


card = Image.new("RGBA", (S, S), OUTER + (255,))
g, mask = plate()
card.paste(g, (0, 0), mask)

ink_layer = Image.new("RGBA", (S, S), INK + (255,))
card = Image.alpha_composite(card, Image.composite(ink_layer, Image.new("RGBA", (S, S), (0, 0, 0, 0)), text_mask()))

out = os.path.join(ROOT, "assets", "share-card-v4.jpg")
card.convert("RGB").save(out, "JPEG", quality=93, optimize=True, progressive=True)
card.convert("RGB").resize((66, 66), Image.LANCZOS).save(os.path.join(ROOT, "tools", "prev-v4.png"))
print("saved", os.path.getsize(out), "bytes")
