# 构建说明

## 自动构建（推荐）

本项目已配置GitHub Actions自动构建，支持三个平台：

### 触发构建
1. 推送代码到main/master分支
2. 创建Pull Request 
3. 创建Release

### 下载构建产物
1. 访问GitHub仓库的Actions页面
2. 选择最新的构建任务
3. 下载对应平台的artifact：
   - `mysql-sea-sync-windows.exe` - Windows可执行文件
   - `mysql-sea-sync-linux` - Linux可执行文件  
   - `mysql-sea-sync-macos` - macOS可执行文件

### 通过Release分发
1. 在GitHub上创建Release
2. 系统会自动将可执行文件附加到Release中
3. 用户可直接从Release页面下载

## 本地构建

如果需要本地构建：

### Windows
```bash
pip install -r requirements.txt
pyinstaller --onefile --console --name mysql-sea-sync-windows main.py
```

### Linux/macOS
```bash
pip install -r requirements.txt
pyinstaller --onefile --console --name mysql-sea-sync main.py
```

## 交叉编译

要在macOS上构建Windows版本，可以使用：
1. 虚拟机（VMware/VirtualBox + Windows）
2. Docker（需要Windows容器支持）
3. GitHub Actions（推荐，本项目已配置）

## 部署文件

构建完成后，用户需要的文件：
- 可执行文件（mysql-sea-sync.exe等）
- 配置文件模板（*.json）
- .env文件模板
- README.md说明文档