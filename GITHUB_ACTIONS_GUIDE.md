# GitHub Actions 自动构建完整指南

## 1. 创建GitHub仓库

### 1.1 在GitHub上创建新仓库
1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `mysql-sea-sync` (或其他名称)
   - **Description**: `MySQL to SeaTable 数据同步工具`
   - **Public/Private**: 根据需要选择
   - **Initialize with README**: 可选择，但我们会覆盖
4. 点击 "Create repository"

### 1.2 记录仓库信息
创建后，记录仓库的克隆地址，格式如：
```
https://github.com/yourusername/mysql-sea-sync.git
```

## 2. 初始化本地Git仓库并推送

### 2.1 初始化本地仓库
在项目目录下执行：
```bash
cd /Users/zhanghui/Sync/mysql-sea-sync
git init
```

### 2.2 添加远程仓库
```bash
git remote add origin https://github.com/yourusername/mysql-sea-sync.git
```

### 2.3 添加文件并提交
```bash
# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: MySQL SeaTable sync tool with GitHub Actions"

# 推送到GitHub
git push -u origin main
```

**注意**：如果提示分支名称问题，可能需要：
```bash
git branch -M main
git push -u origin main
```

## 3. GitHub Actions 工作流说明

### 3.1 工作流文件位置
```
.github/workflows/build.yml
```

### 3.2 触发条件
工作流会在以下情况自动运行：
- 推送代码到 `main` 或 `master` 分支
- 创建 Pull Request
- 创建 Release

### 3.3 构建矩阵
同时构建3个平台：
- **Ubuntu (Linux)**: 生成 `mysql-sea-sync-linux`
- **Windows**: 生成 `mysql-sea-sync-windows.exe`
- **macOS**: 生成 `mysql-sea-sync-macos`

### 3.4 构建步骤
1. **检出代码**: 下载仓库代码
2. **设置Python**: 安装Python 3.9环境
3. **安装依赖**: 执行 `pip install -r requirements.txt`
4. **构建可执行文件**: 使用PyInstaller打包
5. **测试可执行文件**: 简单测试是否能启动
6. **上传产物**: 保存构建结果

## 4. 查看和下载构建结果

### 4.1 查看构建状态
1. 进入GitHub仓库
2. 点击顶部的 "Actions" 标签
3. 可以看到所有的工作流运行记录
4. 绿色✅表示成功，红色❌表示失败

### 4.2 下载Artifacts（构建产物）
1. 点击具体的工作流运行记录
2. 滚动到页面底部的 "Artifacts" 部分
3. 可以看到3个下载链接：
   - `mysql-sea-sync-linux`
   - `mysql-sea-sync-windows.exe`
   - `mysql-sea-sync-macos`
4. 点击下载对应平台的可执行文件

**注意**: Artifacts会在90天后自动删除

## 5. 通过Release进行正式分发

### 5.1 创建Release
1. 在GitHub仓库主页，点击右侧的 "Releases"
2. 点击 "Create a new release"
3. 填写信息：
   - **Tag version**: 如 `v1.0.0`
   - **Release title**: 如 `MySQL SeaTable Sync v1.0.0`
   - **Description**: 版本说明
4. 点击 "Publish release"

### 5.2 自动附加可执行文件
创建Release后，GitHub Actions会自动：
1. 触发构建工作流
2. 将3个平台的可执行文件自动附加到Release
3. 用户可以直接从Release页面下载

### 5.3 Release的优势
- **永久保存**: 不会像Artifacts那样过期
- **版本管理**: 可以发布多个版本
- **公开下载**: 用户可以直接访问下载链接
- **变更日志**: 可以记录每个版本的更新内容

## 6. 日常开发工作流

### 6.1 修改代码后的操作
```bash
# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改内容"

# 推送到GitHub
git push
```

### 6.2 自动构建
推送后，GitHub Actions会自动：
1. 检测到代码变更
2. 启动构建工作流
3. 生成新的可执行文件
4. 上传为Artifacts

### 6.3 查看构建日志
如果构建失败：
1. 进入Actions页面
2. 点击失败的工作流
3. 点击具体的Job（如"build (windows-latest)"）
4. 查看详细的错误日志
5. 根据错误信息修复代码

## 7. 分发给最终用户

### 7.1 通过Artifacts分发（临时）
- 开发者从Actions页面下载
- 适合测试版本
- 90天后自动删除

### 7.2 通过Release分发（正式）
- 用户从Release页面下载
- 适合正式版本
- 永久保存

### 7.3 用户下载步骤
1. 访问GitHub仓库
2. 点击右侧的 "Releases"
3. 选择最新版本
4. 在 "Assets" 部分下载对应平台的文件：
   - Windows用户下载 `.exe` 文件
   - Linux用户下载 `linux` 文件
   - macOS用户下载 `macos` 文件

## 8. 故障排除

### 8.1 常见问题

**问题**: 推送代码后没有触发构建
**解决**: 检查分支名称是否为 `main` 或 `master`

**问题**: 构建失败，提示依赖安装错误
**解决**: 检查 `requirements.txt` 文件格式和内容

**问题**: PyInstaller打包失败
**解决**: 检查代码中是否有相对路径或缺少导入

**问题**: 可执行文件无法运行
**解决**: 检查目标平台的系统要求和依赖

### 8.2 调试技巧
- 查看Actions日志的每个步骤
- 本地测试PyInstaller命令
- 在不同平台上测试可执行文件

## 9. 高级配置

### 9.1 自定义构建参数
可以修改 `.github/workflows/build.yml` 中的PyInstaller参数：
```yaml
pyinstaller --onefile --console --name mysql-sea-sync main.py
```

常用参数：
- `--windowed`: 不显示控制台窗口（适合GUI程序）
- `--icon=icon.ico`: 设置程序图标
- `--add-data`: 包含额外的数据文件

### 9.2 环境变量配置
可以在GitHub仓库设置中添加Secrets，用于构建时的敏感信息。

### 9.3 定时构建
可以添加cron触发器，定期自动构建：
```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日凌晨2点
```

## 10. 最佳实践

1. **版本标签**: 使用语义化版本号（如v1.0.0）
2. **变更日志**: 在Release中详细描述更新内容
3. **测试**: 在发布前在各平台测试可执行文件
4. **文档**: 保持README和文档的及时更新
5. **依赖管理**: 定期更新requirements.txt中的版本

通过以上配置，你就可以在macOS上开发，然后自动构建出Windows、Linux和macOS三个平台的可执行文件，并通过GitHub进行分发。