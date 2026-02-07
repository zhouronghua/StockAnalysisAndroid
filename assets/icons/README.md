# 应用图标说明

## 图标要求

### icon.png
- **用途**: 应用图标
- **尺寸**: 512x512 像素
- **格式**: PNG, 透明背景
- **设计建议**: 简洁的股票/图表图标

### presplash.png
- **用途**: 启动画面
- **尺寸**: 1920x1080 像素（或同比例）
- **格式**: PNG
- **设计建议**: 应用名称+图标+加载提示

## 临时方案

在正式设计完成前，可以使用在线工具生成图标：

1. 访问: https://www.canva.com/
2. 选择"应用图标"模板
3. 添加股票相关元素（K线、箭头等）
4. 导出为PNG格式

## 自动生成脚本

如果安装了ImageMagick，可以运行：

```bash
# 生成简单的纯色图标（临时使用）
convert -size 512x512 xc:#4CAF50 -pointsize 100 -draw "text 100,300 'Stock'" icon.png
convert -size 1920x1080 xc:#4CAF50 -pointsize 150 -draw "text 700,600 '股票分析'" presplash.png
```

## 注意事项

- 构建APK时，如果缺少图标文件，Buildozer会使用默认图标
- 默认图标为Kivy的logo
- 建议在正式发布前替换为自定义图标
