# MySQL to SeaTable 数据同步工具

## 项目说明

本项目为数据分析项目，通过本程序将MySQL数据库中的数据同步到SeaTable表格中，用于进一步的数据分析和报表生成。支持多个数据源和多个同步任务配置。

## 项目依赖

* python3.6+
* python-dotenv
* seatable-api-python-client
* pymysql

## 项目运行

```bash
python main.py
```

运行后会显示菜单，用户可以选择要执行的同步任务（1-12），执行完成后可以选择继续执行其他任务或退出。

## 环境配置

### .env 文件配置

在项目根目录创建 `.env` 文件，配置以下环境变量：

```env
# MySQL 数据库配置（第一个数据源）
MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password

# MySQL 数据库配置（第二个数据源）
MYSQL_HOST_2=your_mysql_host_2
MYSQL_PORT_2=3306
MYSQL_USER_2=your_mysql_user_2
MYSQL_PASSWORD_2=your_mysql_password_2

# SeaTable 服务器配置
SEATABLE_SERVER_URL=https://your_seatable_server.com
```

## 同步任务配置

程序支持12个不同的同步任务，每个任务对应不同的业务数据：

### 1. 合同同步 (memo-contract.json)
- **数据库**: chpm_v2
- **目标表**: 确认收入
- **功能**: 同步合同相关数据，包括合同基本信息、项目信息、客户信息等
- **主要字段**: 合同编号、项目名称、合同金额、项目经理、客户单位等

### 2. 预算同步 (memo-purchase.json)
- **数据库**: projectmng
- **目标表**: 预算信息
- **功能**: 同步项目预算数据
- **主要字段**: 合同编号、预算编号、设备金额、辅材金额、预算金额等

### 3. 外包同步 (memo-outsource.json)
- **数据库**: chpm_v2
- **目标表**: 外包合同
- **功能**: 同步外包合同和外包商信息
- **主要字段**: 项目编号、外包商名称、外包合同额、外包内容等

### 4. 立项研发同步 (memo-rd.json)
- **数据库**: chpm_v2
- **目标表**: 立项研发项目
- **功能**: 同步研发项目立项信息
- **主要字段**: 立项编号、项目全称、项目周期、项目经理、项目预算等

### 5. 自有软件同步 (memo-os.json)
- **数据库**: chpm_v2
- **目标表**: 自有软件项目
- **功能**: 同步自有软件项目信息

### 6. 已中未签同步 (memo-yzwq.json)
- **数据库**: v9
- **目标表**: 已中未签项目
- **功能**: 同步已中标但未签约的项目信息

### 7. 项目进度同步 (memo-progress.json)
- **数据库**: chpm_v2
- **目标表**: 项目进度
- **功能**: 同步项目进度信息

### 8. 工时数据同步 (memo-worktime.json)
- **数据库**: chpm_v2
- **目标表**: 工时数据
- **功能**: 同步工时统计信息

### 9. OA项目编号同步 (memo-project.json)
- **数据库**: v9
- **目标表**: OA项目编号
- **功能**: 同步OA系统中的项目编号信息

### 10. OA立项编号同步 (memo-pi.json)
- **数据库**: v9
- **目标表**: OA立项编号
- **功能**: 同步OA系统中的立项编号信息

### 11. OA销售团队同步 (memo-gssales.json)
- **数据库**: v9
- **目标表**: OA销售团队
- **功能**: 同步OA系统中的销售团队信息

### 12. 回款信息同步 (memo-payin.json)
- **数据库**: projectmng
- **目标表**: 回款信息
- **功能**: 同步项目回款相关信息

## JSON 配置文件结构

每个同步任务对应一个 JSON 配置文件，配置文件包含以下结构：

```json
{
  "seatable": {
    "table_name": "目标表名",
    "name_column": "主键字段名"
  },
  "chunk_size": 300,
  "data_mappings": [
    {
      "description": "数据映射描述",
      "sql_query": [
        "SELECT 语句片段",
        "FROM 表名",
        "WHERE 条件等"
      ],
      "field_mappings": {
        "MySQL字段名": "SeaTable字段名"
      },
      "merge_rules": {
        "on": "关联字段",
        "target_field": "目标字段"
      }
    }
  ]
}
```

### 配置项说明

- **seatable**: SeaTable 表配置
  - `table_name`: 目标表名
  - `name_column`: 主键字段名
- **chunk_size**: 数据分批处理的大小
- **data_mappings**: 数据映射配置数组
  - `description`: 映射描述
  - `sql_query`: SQL查询语句（数组形式）
  - `field_mappings`: 字段映射关系
  - `merge_rules`: 数据合并规则（可选）

## 程序特性

1. **循环菜单**: 支持连续执行多个同步任务
2. **自动清空**: 每次同步前自动清空目标表
3. **分批处理**: 支持大数据量的分批处理
4. **错误处理**: 完善的错误处理和重试机制
5. **数据转换**: 自动处理 Decimal 和日期格式转换
6. **字典映射**: 支持数据字典的自动转换

## 使用流程

1. 配置 `.env` 文件中的数据库连接信息
2. 在 SeaTable 中创建对应的目标表
3. 运行 `python main.py`
4. 选择要执行的同步任务
5. 等待同步完成
6. 选择是否继续执行其他任务

## 注意事项

1. 确保 MySQL 数据库连接正常
2. 确保 SeaTable API Token 有效
3. 确保目标表在 SeaTable 中已创建
4. 同步前会自动清空目标表，请注意数据备份
5. 大量数据同步可能需要较长时间，请耐心等待

## Git 同步注意

忽略 Memo.*，memo.* 文件，避免配置文件被意外提交。
