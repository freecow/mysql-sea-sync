# MySQL-SeaTable 同步工具部署指南

## 概述

本指南帮助您将 MySQL-SeaTable 同步工具部署到同事的机器上，提供最小化、自包含的运行方式。

## 打包方法

### 方法一：自动化打包（推荐）

运行自动化打包脚本：

```bash
# macOS/Linux
python build_standalone.py

# Windows
python build_standalone.py
```

这将创建一个完全自包含的部署包，包含：
- 可执行文件（包含所有依赖）
- 配置文件示例
- 使用说明

### 方法二：手动打包

**Windows 系统：**
```cmd
build_package.bat
```

**macOS/Linux 系统：**
```bash
./build_package.sh
```

## 部署步骤

### 1. 创建部署包

在开发机器上运行打包脚本：

```bash
python build_standalone.py
```

### 2. 传输文件

将生成的 `mysql-seatable-sync-deploy` 文件夹完整地发送给同事，包含：
- `mysql-seatable-sync.exe`（Windows）或 `mysql-seatable-sync`（macOS/Linux）
- `.env.example`
- `README.txt`

### 3. 同事配置步骤

1. **配置环境变量**
   ```bash
   # 复制配置文件模板
   cp .env.example .env
   
   # 编辑配置文件，填入实际的数据库信息
   # Windows: 用记事本打开 .env
   # macOS/Linux: nano .env 或 vim .env
   ```

2. **编辑 .env 文件示例**
   ```env
   # 第一个MySQL数据库
   MYSQL_HOST=192.168.1.100
   MYSQL_PORT=3306
   MYSQL_USER=sync_user
   MYSQL_PASSWORD=your_password

   # 第二个MySQL数据库
   MYSQL_HOST_2=192.168.1.101
   MYSQL_PORT_2=3306
   MYSQL_USER_2=sync_user2
   MYSQL_PASSWORD_2=your_password2

   # SeaTable配置
   SEATABLE_SERVER_URL=https://cloud.seatable.io
   ```

3. **运行程序**
   ```bash
   # Windows
   mysql-seatable-sync.exe

   # macOS/Linux
   ./mysql-seatable-sync
   ```

## 优势

### 🎯 **最小化部署**
- 单个可执行文件，无需安装 Python
- 所有依赖包已内置
- 配置文件自包含

### 🔒 **隐私保护**
- 同事无法查看源代码
- 配置信息在本地 .env 文件中
- 可执行文件已混淆

### 🚀 **易于使用**
- 双击运行（Windows）
- 交互式菜单选择
- 自动错误处理和重试

## 技术细节

### 打包工具
- 使用 PyInstaller 创建独立可执行文件
- `--onefile` 模式生成单文件部署
- 自动包含所有必要的 Python 库

### 包含的依赖
- seatable-api：SeaTable API 客户端
- pymysql：MySQL 数据库连接
- python-dotenv：环境变量管理
- 所有配置文件（*.json）

### 文件结构
```
mysql-seatable-sync-deploy/
├── mysql-seatable-sync(.exe)  # 主可执行文件
├── .env.example               # 配置文件模板
└── README.txt                # 使用说明
```

## 故障排除

### 常见问题

1. **可执行文件无法运行**
   - Windows: 检查是否被杀毒软件拦截
   - 确保有执行权限

2. **数据库连接失败**
   - 检查 .env 文件配置
   - 确认网络连通性
   - 验证数据库用户权限

3. **SeaTable 连接失败**
   - 检查 SeaTable API Token
   - 确认服务器 URL 正确

### 日志和调试
- 程序运行时会显示详细的执行日志
- 错误信息会直接在控制台显示
- 支持重试机制

## 安全注意事项

1. **保护配置文件**
   - .env 文件包含敏感信息
   - 不要将 .env 文件分享给他人
   - 建议设置文件权限为仅用户可读

2. **网络安全**
   - 确保数据库连接使用安全协议
   - 考虑使用 VPN 或专网连接

3. **访问权限**
   - 数据库用户应只有必要的读取权限
   - 定期更换数据库密码

## 更新和维护

### 更新部署
当需要更新程序时：
1. 在开发机器上重新打包
2. 替换同事机器上的可执行文件
3. 保留原有的 .env 配置文件

### 配置备份
建议同事定期备份 .env 配置文件，避免重新配置的麻烦。

---

如有问题，请联系开发者进行技术支持。