# 直播间贴片生成器 · 迷人秀

输入手机号 / 微信号，在浏览器本地生成 **1920×3414 透明 PNG** 直播间贴片，长按即可保存到相册。

## 功能

- 5 种模板：微信号、不运动不挨饿、减脂塑形（气泡）、身高体重年龄、月减 8-15 斤
- 文字颜色 8 色、底色 8 色，按模板分别记忆
- 笔刷底纹随机生成，可「换个笔刷」
- 输出原始分辨率 1920×3414，带完整透明通道
- 可选紧凑裁切

## 技术

纯静态页面，无后端。Canvas 2D 渲染，字体为 Noto Sans SC Black 子集（内嵌 base64，约 97KB）。

- `index.html` 页面与渲染引擎
- `assets/font.css` 内嵌字体
- `assets/logo.png` 品牌标识
- `tools/mkfont.py` 字体重建脚本

## 调试参数

```
?probe=phone:13800000000   直接输出画布（截图用）
?metrics=1                 输出字体度量
?probe=bubble:减脂塑形&color=%23FFFFFF&bg=%23D18CFF&seed=11&crop=1
```

## 许可

字体 Noto Sans SC 遵循 SIL Open Font License 1.1。
