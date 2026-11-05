"""生成微信分享卡片缩略图 v3：黄底 + 「直播贴片」大字图标。"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 800
FONT = "C:/Windows/Fonts/msyhbd.ttc"
INK = (43, 27, 5)


def glow(size, color, center, radius, alpha):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=color + (alpha,),
    )
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.62))


bg = Image.new("RGBA", (S, S), (246, 183, 12, 255))
bg = Image.alpha_composite(bg, glow(S, (255, 210, 77), (int(S * 0.32), int(S * 0.28)), 400, 165))
bg = Image.alpha_composite(bg, glow(S, (255, 222, 120), (int(S * 0.5), int(S * 0.5)), 320, 70))
bg = Image.alpha_composite(bg, glow(S, (232, 156, 0), (int(S * 0.92), int(S * 0.94)), 340, 95))

d = ImageDraw.Draw(bg)
font = ImageFont.truetype(FONT, 268)

cells = [((268, 262), "直"), ((532, 262), "播"), ((268, 538), "贴"), ((532, 538), "片")]
for (cx, cy), ch in cells:
    d.text((cx, cy), ch, font=font, fill=INK + (255,), anchor="mm")

out = os.path.join(ROOT, "assets", "share-card-v3.jpg")
bg.convert("RGB").save(out, "JPEG", quality=92, optimize=True, progressive=True)
bg.convert("RGB").resize((66, 66), Image.LANCZOS).save(os.path.join(ROOT, "tools", "prev-v3.png"))
print("saved", os.path.getsize(out), "bytes")
