# 开源安全配置指南

## 🔐 环境配置安全设置

### 1. 创建环境变量文件

```bash
# 复制模板文件
cp .env.example .env

# 编辑配置文件（替换为真实信息）
nano .env
```

### 2. 配置数据库连接信息

```env
# 第一个MySQL数据库连接
MYSQL_HOST=your_actual_mysql_host
MYSQL_PORT=3306
MYSQL_USER=your_actual_mysql_user
MYSQL_PASSWORD=your_actual_mysql_password
MYSQL_DB=your_actual_database_name

# 第二个MySQL数据库连接
MYSQL_HOST_2=your_actual_mysql_host_2
MYSQL_PORT_2=3306
MYSQL_USER_2=your_actual_mysql_user_2
MYSQL_PASSWORD_2=your_actual_mysql_password_2
MYSQL_DB_2=your_actual_database_name_2
```

### 3. 配置SeaTable API Tokens

为每个同步任务配置对应的API Token：

```env
# SeaTable API Tokens
SEATABLE_TOKEN_CONTRACT=your_actual_contract_token
SEATABLE_TOKEN_OS=your_actual_os_token
SEATABLE_TOKEN_PROGRESS=your_actual_progress_token
SEATABLE_TOKEN_RD=your_actual_rd_token
SEATABLE_TOKEN_WORKTIME=your_actual_worktime_token
SEATABLE_TOKEN_PAYIN=your_actual_payin_token
SEATABLE_TOKEN_PI=your_actual_pi_token
SEATABLE_TOKEN_PROJECT=your_actual_project_token
SEATABLE_TOKEN_GSSALES=your_actual_gssales_token
SEATABLE_TOKEN_YZWQ=your_actual_yzwq_token
SEATABLE_TOKEN_OUTSOURCE=your_actual_outsource_token
SEATABLE_TOKEN_PURCHASE=your_actual_purchase_token
```

## 🛡️ 安全最佳实践

### 环境变量管理
- ✅ 使用 `.env` 文件存储敏感信息
- ✅ `.env` 文件已在 `.gitignore` 中排除
- ✅ 提供 `.env.example` 模板文件
- ❌ 永远不要将真实的 `.env` 文件提交到Git

### API Token安全
- 🔄 定期更换SeaTable API Tokens
- 👥 为不同环境使用不同的tokens
- 📋 记录token的用途和权限范围
- 🚫 避免在多个系统中共享同一token

### 数据库安全
- 🔒 使用最小权限原则的数据库用户
- 🌐 限制数据库访问的IP地址
- 📊 仅给予必要的读取权限
- 🔐 使用强密码和加密连接

## 📋 部署检查清单

### 开发环境
- [ ] 创建并配置 `.env` 文件
- [ ] 验证所有环境变量都已设置
- [ ] 测试数据库连接
- [ ] 测试SeaTable API连接
- [ ] 确认 `.env` 文件未被Git跟踪

### 生产部署
- [ ] 使用生产环境的数据库配置
- [ ] 使用生产环境的SeaTable tokens
- [ ] 验证网络连接和防火墙设置
- [ ] 配置日志级别和监控
- [ ] 设置自动备份和恢复流程

### 团队协作
- [ ] 分享 `.env.example` 文件
- [ ] 提供安全配置文档
- [ ] 通过安全渠道分享真实配置
- [ ] 定期审核访问权限

## 🚨 安全事件响应

### 如果token泄露
1. **立即更换**所有相关的SeaTable API tokens
2. **检查访问日志**确认是否有异常访问
3. **通知团队成员**更新本地配置
4. **审查代码**确保没有其他硬编码信息

### 如果数据库信息泄露
1. **更改数据库密码**
2. **限制数据库访问IP**
3. **检查数据库访问日志**
4. **评估数据安全影响**

## 📞 获取帮助

如果在配置过程中遇到问题：

1. **检查环境变量**：确保所有必需的变量都已设置
2. **验证网络连接**：确保能访问数据库和SeaTable服务
3. **查看错误日志**：程序会显示具体的配置错误信息
4. **参考文档**：查看README.md中的详细说明

## 🔗 相关文档

- [README.md](README.md) - 项目总体说明
- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - 自动构建指南
- [.env.example](.env.example) - 环境变量模板

---

**重要提醒**: 开源项目的安全性依赖于正确的配置管理。请务必遵循本指南，确保敏感信息不会泄露。