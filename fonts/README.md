# 字体文件说明

## 中文字体支持

为了在Android应用中正确显示中文，需要在此目录下放置中文字体文件。

### 推荐字体（选择其一）

1. **Noto Sans CJK SC** (推荐，开源免费)
   - 下载地址: https://github.com/notofonts/noto-cjk/releases
   - 下载文件: NotoSansCJKsc-Regular.otf 或 NotoSansSC-Regular.ttf
   - 重命名为: `NotoSansSC-Regular.ttf`

2. **思源黑体 (Source Han Sans)** (开源免费)
   - 下载地址: https://github.com/adobe-fonts/source-han-sans/releases
   - 下载文件: SourceHanSansSC-Regular.otf
   - 重命名为: `SourceHanSansSC-Regular.ttf`

3. **文泉驿微米黑** (开源免费)
   - 下载地址: http://wenq.org/wqy2/index.cgi?FontGuide
   - 文件名: wqy-microhei.ttc

### 使用说明

1. 下载上述任一字体文件
2. 将字体文件放在此目录下
3. 确保文件名为: `NotoSansSC-Regular.ttf` 或修改main.py中的字体文件名
4. 重新构建APK

### 当前配置

应用会自动查找以下字体文件（按优先级）：
- fonts/NotoSansSC-Regular.ttf
- fonts/SourceHanSansSC-Regular.ttf
- fonts/wqy-microhei.ttc
- 系统字体: /system/fonts/DroidSansFallback.ttf (Android系统自带)
