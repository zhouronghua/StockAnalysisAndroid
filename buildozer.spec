[app]

# 应用基本信息
title = 股票分析
package.name = stockanalysis
package.domain = com.tradeanalytics

# 源代码配置
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.exclude_dirs = tests, bin, .buildozer, src/core, src/storage, src/scheduler, src/ui

# 版本信息
version = 1.0.0
# version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# Python依赖（最小化版本，避免编译错误）
requirements = python3,kivy==2.3.0,pillow,requests

# 安卓权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,ACCESS_NETWORK_STATE

# 安卓API级别
android.api = 31
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# 应用图标和启动屏幕（暂时注释，使用默认）
#icon.filename = %(source.dir)s/assets/icons/icon.png
#presplash.filename = %(source.dir)s/assets/icons/presplash.png

# 方向设置
orientation = portrait
fullscreen = 0

# 启用后台服务（暂时禁用）
#services = stockservice:service.py

# 架构支持（使用新配置格式）
android.archs = arm64-v8a

# 打包选项
android.gradle_dependencies = 

# 应用元数据
android.meta_data = 

[buildozer]

# 日志级别 (0 = error only, 1 = info, 2 = debug)
log_level = 2

# 警告根用户
warn_on_root = 1

# 构建目录
bin_dir = ./bin

# 使用稳定的python-for-android版本
p4a.branch = master
p4a.source_dir = 
p4a.local_recipes = 
p4a.hook = 
p4a.bootstrap = sdl2
p4a.port = 
