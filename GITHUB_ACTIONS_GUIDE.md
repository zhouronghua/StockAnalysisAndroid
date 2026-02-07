# 使用GitHub Actions自动构建APK

## 优势

- ✅ 完全在云端构建，不占用本地资源
- ✅ 不需要安装WSL2或Linux
- ✅ 免费使用（每月2000分钟构建时间）
- ✅ 自动构建，提交代码即可
- ✅ 支持多人协作

## 使用步骤

### 1. 创建GitHub仓库

```bash
# 在项目目录（StockAnalysisAndroid）执行
git init
git add .
git commit -m "Initial commit"

# 在GitHub上创建新仓库，然后：
git remote add origin https://github.com/你的用户名/StockAnalysisAndroid.git
git branch -M main
git push -u origin main
```

### 2. 等待自动构建

- 推送代码后，GitHub Actions会自动开始构建
- 访问: https://github.com/你的用户名/StockAnalysisAndroid/actions
- 查看构建进度（首次约40-60分钟）

### 3. 下载APK

构建完成后：

1. 进入Actions页面
2. 点击最新的工作流运行
3. 在"Artifacts"区域下载`stockanalysis-apk`
4. 解压ZIP文件，获得APK

### 4. 手动触发构建（可选）

1. 访问Actions页面
2. 选择"Build Android APK"工作流
3. 点击"Run workflow"
4. 选择分支，点击"Run workflow"

## 本地修改代码后的流程

```bash
# 1. 修改代码
# 编辑main.py或其他文件

# 2. 提交并推送
git add .
git commit -m "更新功能"
git push

# 3. 查看GitHub Actions自动构建
# 访问仓库的Actions页面

# 4. 构建完成后下载APK
```

## 配置说明

### 触发条件

当前配置会在以下情况自动构建：

- 推送到main或master分支
- 创建Pull Request
- 手动触发

### 修改触发条件

编辑`.github/workflows/build-apk.yml`：

```yaml
on:
  push:
    branches: [ main ]  # 只在推送到main时构建
  # 移除其他触发条件
```

### 定时构建（可选）

每天自动构建：

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 每天UTC时间2:00（北京时间10:00）
```

## 查看构建日志

1. 访问Actions页面
2. 点击工作流运行
3. 点击"build"任务
4. 展开各个步骤查看详细日志

## 加速构建

### 使用缓存

已在workflow中配置缓存，第二次构建会快很多（约15-20分钟）。

### 仅在需要时构建

在commit信息中添加`[skip ci]`可跳过构建：

```bash
git commit -m "更新文档 [skip ci]"
```

## 发布Release

### 自动发布

创建标签时自动创建Release：

```bash
git tag -a v1.0.0 -m "首个正式版本"
git push origin v1.0.0
```

GitHub Actions会自动：
1. 构建APK
2. 创建Release
3. 上传APK到Release

### 手动发布

1. 访问仓库的"Releases"页面
2. 点击"Draft a new release"
3. 上传下载的APK
4. 填写版本信息
5. 发布

## 故障排除

### 问题1: 构建失败

查看日志，常见原因：
- buildozer.spec配置错误
- 依赖版本冲突
- 代码语法错误

### 问题2: 找不到Artifacts

- 只有构建成功才会上传APK
- Artifacts保留30天后自动删除
- 检查构建日志是否有错误

### 问题3: 构建时间过长

首次构建需要下载所有依赖（约40-60分钟），后续构建会使用缓存（约15-20分钟）。

## 私有仓库

如果使用私有仓库：
- 免费账号每月2000分钟构建时间
- Pro账号每月3000分钟
- 超出后需要付费或等待下月

## 进阶配置

### 多个构建变体

```yaml
strategy:
  matrix:
    arch: [armeabi-v7a, arm64-v8a]
```

### 构建发布版

```yaml
- name: 构建Release APK
  run: buildozer -v android release
```

### 发送通知

构建完成后发送邮件或Slack通知（需配置）。

---

**推荐**: 这是最简单、最省心的Windows用户构建APK的方法！
