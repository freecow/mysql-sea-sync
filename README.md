# MySQL-SeaTable 数据同步工具

一个用于将MySQL数据库数据同步到SeaTable表格的自动化工具，支持多种同步任务和数据映射。

## 🎯 功能特点

- **多数据源支持**：支持连接多个MySQL数据库
- **丰富的同步类型**：合同、预算、工时、项目进度等12种同步任务
- **智能数据映射**：自动处理字段映射和数据类型转换
- **批量处理**：支持大数据量分批同步
- **交互式菜单**：循环菜单设计，可连续执行多个任务

## 📋 支持的同步任务

1. **合同同步** - 合同相关数据同步
2. **自有软件同步** - 软件项目数据同步  
3. **项目进度同步** - 项目进度跟踪数据
4. **预算同步** - 预算管理数据
5. **工时数据同步** - 工时统计数据
6. **回款信息同步** - 财务回款数据
7. **OA项目编号同步** - OA系统项目编号
8. **OA立项编号同步** - OA系统立项编号
9. **OA销售团队同步** - 销售团队信息
10. **已中未签同步** - 中标未签约项目
11. **立项研发同步** - 研发项目立项数据
12. **外包同步** - 外包项目数据

## 🚀 快速开始

### 开发环境运行

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入数据库连接信息
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

### 生产部署（推荐）

1. **一键打包**
   ```bash
   python quick_deploy.py
   ```

2. **发送部署包**
   - 将生成的压缩文件发送给使用者
   - 或发送整个 `mysql-seatable-sync-deploy` 文件夹

3. **使用者操作**
   ```bash
   # 解压并配置
   cp .env.example .env
   # 编辑 .env 填入数据库信息
   
   # 运行（Windows）
   mysql-seatable-sync.exe
   
   # 运行（macOS/Linux）
   ./mysql-seatable-sync
   ```

## ⚙️ 配置说明

### 环境变量配置 (.env)

```env
# 第一个MySQL数据库连接
MYSQL_HOST=your_mysql_host_1
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user_1
MYSQL_PASSWORD=your_mysql_password_1

# 第二个MySQL数据库连接  
MYSQL_HOST_2=your_mysql_host_2
MYSQL_PORT_2=3306
MYSQL_USER_2=your_mysql_user_2
MYSQL_PASSWORD_2=your_mysql_password_2

# SeaTable服务器配置
SEATABLE_SERVER_URL=https://cloud.seatable.io
```

### 任务配置文件

每个同步任务对应一个JSON配置文件：

- `memo-contract.json` - 合同同步配置
- `memo-os.json` - 自有软件同步配置
- `memo-progress.json` - 项目进度同步配置
- 等等...

配置文件包含：
- SeaTable表格映射信息
- 数据字段映射规则
- SQL查询语句
- 数据合并规则

## 🔧 技术架构

### 核心组件

- **数据连接层**：pymysql + seatable-api
- **配置管理**：python-dotenv + JSON配置
- **数据处理**：支持Decimal、日期格式转换
- **错误处理**：自动重试机制

### 数据流程

1. **连接数据源**：根据任务类型连接对应MySQL数据库
2. **执行查询**：根据配置文件执行SQL查询
3. **数据映射**：按照字段映射规则转换数据
4. **清空目标表**：清空SeaTable目标表格
5. **批量插入**：分批插入处理后的数据
6. **数据合并**：如需要，执行数据合并操作

## 📁 项目结构

```
mysql-sea-sync/
├── main.py                    # 主程序文件
├── requirements.txt           # Python依赖
├── .env.example              # 环境变量模板
├── memo-*.json               # 各任务配置文件
├── build_standalone.py       # 独立打包脚本
├── quick_deploy.py           # 一键部署脚本
├── DEPLOYMENT.md             # 部署指南
└── README.md                 # 本说明文件
```

## 🛠️ 开发说明

### 添加新的同步任务

1. **创建配置文件**
   ```json
   {
     "seatable": {
       "table_name": "目标表名",
       "name_column": "主键列名"
     },
     "chunk_size": 300,
     "data_mappings": [...]
   }
   ```

2. **在main.py中添加选项**
   ```python
   config_options = {
     # 添加新的任务选项
     13: {
       "name": "新任务同步",
       "db": "数据库名",
       "token": "SeaTable API Token",
       "config_file": "配置文件名.json",
       "mysql_config": mysql_config_1
     }
   }
   ```

### 字段映射配置

```json
"field_mappings": {
  "mysql_column_name": "seatable_column_name",
  "contract_code": "合同编号",
  "contract_amount": "合同金额"
}
```

### 数据合并规则

```json
"merge_rules": {
  "merge_into": "主表数据",
  "on": "关联字段",
  "target_field": "目标字段"
}
```

## 🔒 安全注意事项

1. **数据库权限**：确保数据库用户只有必要的读取权限
2. **网络安全**：建议使用VPN或专网连接数据库
3. **配置安全**：不要将 .env 文件提交到版本控制
4. **API令牌**：定期更换SeaTable API令牌

## 📞 技术支持

如遇到问题，请检查：

1. **网络连接**：确保能访问MySQL数据库和SeaTable服务
2. **权限配置**：验证数据库用户权限和SeaTable API权限
3. **配置文件**：检查 .env 文件和JSON配置文件格式
4. **日志信息**：查看程序运行时的错误提示

---

**作者**: Zhanghui  
**版本**: 2025-08-05  
**许可**: 企业内部使用