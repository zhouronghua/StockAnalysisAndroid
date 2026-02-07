# GitHub Actions 构建失败修复说明

## 问题原因

构建失败的错误信息：
```
This request has been automatically failed because it uses a deprecated version of 
`actions/upload-artifact: v3`. Learn more: 
https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/
```

**原因**：GitHub在2024年4月宣布废弃 `actions/upload-artifact@v3`，必须升级到v4版本。

## 已修复的内容

已将以下Actions升级到最新版本：

| Action | 旧版本 | 新版本 |
|--------|-------|--------|
| actions/cache | v3 | v4 |
| actions/upload-artifact | v3 | v4 |
| softprops/action-gh-release | v1 | v2 |

## 如何应用修复

### 方式1: 直接提交更新（推荐）

```bash
cd E:\code\TradeAnalytics\StockAnalysisAndroid

# 提交修复
git add .github/workflows/build-apk.yml
git commit -m "Fix: 升级GitHub Actions到最新版本"
git push
```

### 方式2: 查看差异后再提交

```bash
# 查看修改
git diff .github/workflows/build-apk.yml

# 如果确认无误，提交
git add .github/workflows/build-apk.yml
git commit -m "Fix: 升级GitHub Actions到最新版本"
git push
```

## 提交后

1. 访问：https://github.com/zhouronghua/StockAnalysisAndroid/actions
2. 新的构建会自动开始
3. 等待构建完成（约40-60分钟）
4. 在Artifacts区域下载APK

## 验证修复

推送后，访问Actions页面，应该看到：
- ✅ 新的workflow运行
- ✅ "build"步骤成功
- ✅ "上传APK"步骤成功
- ✅ Artifacts中有可下载的APK

## v3到v4的主要变更

### upload-artifact@v4

**重要变更**：
- Artifact名称在同一workflow中必须唯一
- 上传性能提升3-5倍
- 更好的错误处理

**不需要修改代码**，我们的配置已经兼容。

### 参考链接

- [GitHub官方公告](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/)
- [upload-artifact@v4文档](https://github.com/actions/upload-artifact)
- [cache@v4文档](https://github.com/actions/cache)

## 故障排除

### 如果还是失败

1. **检查workflow语法**
   ```bash
   # 在本地验证YAML语法
   python -c "import yaml; yaml.safe_load(open('.github/workflows/build-apk.yml'))"
   ```

2. **查看详细日志**
   - 访问失败的workflow运行
   - 展开每个步骤查看详细日志
   - 搜索"error"关键词

3. **清除缓存**
   - 访问：https://github.com/zhouronghua/StockAnalysisAndroid/actions/caches
   - 删除所有缓存
   - 重新运行workflow

### 常见错误

#### 错误1: "Artifact name conflict"

**原因**：Artifact名称重复

**解决**：确保每个上传步骤的name唯一（已修复）

#### 错误2: "buildozer: command not found"

**原因**：Python依赖安装失败

**解决**：检查"安装Buildozer"步骤的日志

#### 错误3: "Out of disk space"

**原因**：GitHub Runner磁盘空间不足

**解决**：添加清理步骤（通常不需要）

## 预期构建时间

- **首次构建**: 40-60分钟（下载SDK/NDK）
- **后续构建**: 15-20分钟（使用缓存）

## 下一步

修复提交后，您可以：

1. ✅ 继续开发功能
2. ✅ 每次推送自动构建
3. ✅ 下载最新的APK测试
4. ✅ 创建Release发布版本

---

**修复已完成！现在提交更新即可。**
