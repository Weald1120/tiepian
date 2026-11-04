# -*- coding: utf-8 -*-
"""生成贴片专用字体子集（Noto Sans SC Black 900 -> woff2 -> base64）"""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset
import base64, io, os

SRC = 'C:/Windows/Fonts/NotoSansSC-VF.ttf'
OUT = 'font_subset.woff2'
CSS_OUT = 'assets/font.css'

templates = [
    "微", "不运动，不挨饿", "减脂塑形", "身高体重年龄打出来", "月减8-15斤",
]

extra = (
    "的了我你他她是在有和就不人都一上下大中小多多少想要瘦掉肉腰腿肚脸全"
    "排毒代谢调理质产宝妈男女性别秤食餐早午晚主食蔬菜果蛋白热量卡里"
    "健康跑跳绳游泳瑜伽普拉提燃紧致皮肤松弛垂抗衰轻岁数准开始坚持成逆袭"
    "蜕变自律部间关注点赞分享评论留言客服老师专业对指导方案方法技巧干货"
    "知识案例真实反馈效果比图前后化名额外优惠价格钱免费领取咨询了解情报名"
    "课程减到天周月年每目标达标成功瘦身肥胖基数掉称掉秤反弹容易难慢快"
    "男女老少上班族学生族产后修复塑型美体美容院项目体验价仅限今日"
    "微信电话手机号码加好友私信发送领取资料食谱免费送福利"
    "不运动不节食不挨饿不反弹安全有效简单轻松躺着也能"
    "零一二三四五六七八九十百千万亿个次份款号岁元块角毛"
    "早晚上下左右前后高低长短快慢真假新旧男女老少"
    "吃东西瘦胖增减肌打卡记录每日更新直播间粉丝团队"
    "关注私信领取资料免费送福利优惠名额有限抓紧时间"
    "想要就来点进下方小黄车链接购买咨询客服老师"
    "第一第二第三第一名前十名限时特价秒杀抢购"
)

chars = set(''.join(templates) + extra)
chars |= set(chr(c) for c in range(0x20, 0x7F))
chars |= set('，。！？、：；（）【】《》“”‘’—…～·℃')
chars.discard('\n')

print('glyph chars:', len(chars))

font = TTFont(SRC)
inst = instantiateVariableFont(font, {'wght': 900}, inplace=False, updateFontNames=True)

opts = subset.Options()
opts.flavor = 'woff2'
opts.layout_features = ['kern', 'liga', 'locl', 'ccmp', 'palt', 'halt']
opts.name_IDs = ['*']
opts.notdef_outline = True
opts.recalc_bounds = True
opts.drop_tables += ['DSIG']

sub = subset.Subsetter(options=opts)
sub.populate(text=''.join(chars))
sub.subset(inst)
inst.save(OUT)

size = os.path.getsize(OUT)
print('woff2 size:', size, 'bytes')
b64 = base64.b64encode(open(OUT, 'rb').read()).decode()
css = (
    "/* Noto Sans SC Black (SIL Open Font License 1.1) - 子集，仅用于贴片渲染 */\n"
    "@font-face{\n  font-family:'StickerBlack';\n  font-style:normal;\n"
    "  font-weight:100 900;\n  font-display:block;\n"
    "  src:url(data:font/woff2;base64,%s) format('woff2');\n}\n" % b64
)
open(CSS_OUT, 'w', encoding='utf-8').write(css)
os.remove(OUT)
print('css bytes:', len(css))
