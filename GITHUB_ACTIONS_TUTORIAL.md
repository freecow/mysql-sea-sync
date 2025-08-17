# GitHub Actions 自动构建教程

## 概述

本教程将以 `mysql-sea-sync` 项目为例，详细讲解如何从零开始编写GitHub Actions工作流文件，实现Python项目的跨平台自动构建。

## 🎯 教程目标

学完本教程，你将能够：
- 理解GitHub Actions的基本概念和工作原理
- 从零开始编写完整的构建工作流
- 实现Python项目的跨平台打包（Windows/Linux/macOS）
- 配置自动化的文件分发机制

## 📚 前置知识

- 基本的Git操作
- Python项目结构
- PyInstaller打包工具
- YAML文件格式

## 🚀 步骤1：理解项目需求

### 项目背景
- **项目类型**: Python命令行工具
- **依赖**: pymysql, seatable-api, python-dotenv
- **目标**: 生成跨平台可执行文件
- **分发方式**: GitHub Releases + Artifacts

### 构建需求分析
1. **多平台支持**: Windows (.exe)、Linux、macOS
2. **自动触发**: 代码推送和Release创建时
3. **依赖管理**: 自动安装requirements.txt
4. **文件命名**: 平台特定的文件名
5. **权限配置**: 支持上传到Release

## 🔧 步骤2：创建工作流目录

### 2.1 创建目录结构
```bash
mkdir -p .github/workflows
```

### 2.2 理解目录作用
- `.github/`: GitHub特殊目录
- `workflows/`: 存放工作流文件
- `build.yml`: 我们的构建工作流文件

## 📝 步骤3：编写基础工作流文件

### 3.1 创建文件并写入基本结构

```yaml
# .github/workflows/build.yml
name: Build Executables

# Auto-build for multiple platforms
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  release:
    types: [created, published]
```

**解释**:
- `name`: 工作流的显示名称
- `on`: 定义触发条件
  - `push`: 推送到main/master分支时触发
  - `pull_request`: 创建PR时触发
  - `release`: 创建或发布Release时触发

### 3.2 添加权限配置

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

**解释**:
- `contents: write`: 允许上传文件到Release
- `issues: write`: 允许操作Issues（可选）
- `pull-requests: write`: 允许操作PR（可选）

## 🏗️ 步骤4：配置构建矩阵

### 4.1 定义构建任务

```yaml
jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            output-name: mysql-sea-sync-linux
            output-path: dist/mysql-sea-sync-linux
          - os: windows-latest
            output-name: mysql-sea-sync-windows.exe
            output-path: dist/mysql-sea-sync-windows.exe
          - os: macos-latest
            output-name: mysql-sea-sync-macos
            output-path: dist/mysql-sea-sync-macos
```

**解释**:
- `runs-on`: 指定运行环境（从matrix动态选择）
- `strategy.matrix`: 定义构建矩阵，并行运行多个配置
- `include`: 为每个平台定义特定的配置
  - `os`: 操作系统
  - `output-name`: 最终文件名
  - `output-path`: 文件路径

### 4.2 矩阵配置的优势

1. **并行执行**: 3个平台同时构建，节省时间
2. **配置复用**: 相同的步骤在不同平台上执行
3. **灵活配置**: 每个平台可以有不同的参数

## ⚙️ 步骤5：编写构建步骤

### 5.1 代码检出

```yaml
steps:
- name: Checkout code
  uses: actions/checkout@v4
```

**解释**:
- 使用官方action下载仓库代码
- `@v4`是版本号，使用最新稳定版

### 5.2 Python环境设置

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.9'
```

**解释**:
- 安装指定版本的Python
- `with`参数传递给action

### 5.3 依赖安装

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

**解释**:
- `run`: 执行shell命令
- `|`: YAML多行字符串语法
- 先升级pip，再安装项目依赖

### 5.4 PyInstaller构建

```yaml
- name: Build executable with PyInstaller
  run: |
    pyinstaller --onefile --console --name main main.py
```

**解释**:
- `--onefile`: 打包成单个可执行文件
- `--console`: 保留控制台窗口
- `--name main`: 指定输出文件名

### 5.5 文件重命名和权限设置

```yaml
- name: Rename executable for release
  run: |
    if [ "${{ runner.os }}" = "Windows" ]; then
      mv dist/main.exe dist/${{ matrix.output-name }}
    else
      mv dist/main dist/${{ matrix.output-name }}
      chmod +x dist/${{ matrix.output-name }}
    fi
  shell: bash
```

**解释**:
- `${{ runner.os }}`: GitHub提供的环境变量
- `${{ matrix.output-name }}`: 引用矩阵配置
- `chmod +x`: 为Linux/macOS添加执行权限
- `shell: bash`: 指定shell类型（Windows也能用bash）

## 📦 步骤6：配置文件上传

### 6.1 Artifacts上传（临时文件）

```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: ${{ matrix.output-name }}
    path: ${{ matrix.output-path }}
    retention-days: 90
```

**解释**:
- Artifacts是临时构建产物
- `retention-days`: 保留天数
- 用于测试和调试

### 6.2 Release上传（正式发布）

```yaml
- name: Upload to release (if release)
  if: github.event_name == 'release'
  uses: softprops/action-gh-release@v2
  with:
    files: ${{ matrix.output-path }}
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**解释**:
- `if`: 条件执行，只在Release时运行
- `softprops/action-gh-release`: 第三方action，功能更强大
- `GITHUB_TOKEN`: GitHub自动提供的认证token

## 📋 步骤7：完整的工作流文件

### 完整的 `.github/workflows/build.yml`

```yaml
name: Build Executables

# Auto-build for multiple platforms
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  release:
    types: [created, published]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            output-name: mysql-sea-sync-linux
            output-path: dist/mysql-sea-sync-linux
          - os: windows-latest
            output-name: mysql-sea-sync-windows.exe
            output-path: dist/mysql-sea-sync-windows.exe
          - os: macos-latest
            output-name: mysql-sea-sync-macos
            output-path: dist/mysql-sea-sync-macos
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Build executable with PyInstaller
      run: |
        pyinstaller --onefile --console --name main main.py
        
    - name: Rename executable for release
      run: |
        if [ "${{ runner.os }}" = "Windows" ]; then
          mv dist/main.exe dist/${{ matrix.output-name }}
        else
          mv dist/main dist/${{ matrix.output-name }}
          chmod +x dist/${{ matrix.output-name }}
        fi
      shell: bash
        
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: ${{ matrix.output-name }}
        path: ${{ matrix.output-path }}
        retention-days: 90
        
    - name: Upload to release (if release)
      if: github.event_name == 'release'
      uses: softprops/action-gh-release@v2
      with:
        files: ${{ matrix.output-path }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 🚀 步骤8：测试和部署

### 8.1 提交工作流文件

```bash
git add .github/workflows/build.yml
git commit -m "Add GitHub Actions build workflow"
git push origin main
```

### 8.2 观察构建过程

1. **访问Actions页面**: `https://github.com/用户名/仓库名/actions`
2. **查看运行状态**: 绿色✅成功，红色❌失败
3. **查看详细日志**: 点击具体的运行记录

### 8.3 下载构建产物

#### 方式1：从Artifacts下载
1. 进入具体的工作流运行页面
2. 滚动到底部的"Artifacts"部分
3. 下载对应平台的文件

#### 方式2：从Release下载
1. 创建Release: `https://github.com/用户名/仓库名/releases/new`
2. 系统自动触发构建并上传文件
3. 用户可直接从Release页面下载

## 🔧 步骤9：常见优化和扩展

### 9.1 添加构建缓存

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 9.2 添加测试步骤

```yaml
- name: Run tests
  run: |
    python -m pytest tests/
```

### 9.3 条件构建

```yaml
- name: Build only on main branch
  if: github.ref == 'refs/heads/main'
  run: |
    echo "Building on main branch"
```

### 9.4 环境变量配置

```yaml
env:
  BUILD_VERSION: ${{ github.sha }}
  PYTHONPATH: ${{ github.workspace }}
```

### 9.5 自定义PyInstaller参数

```yaml
- name: Build with custom options
  run: |
    pyinstaller \
      --onefile \
      --windowed \
      --icon=icon.ico \
      --add-data="config:config" \
      main.py
```

## 🛠️ 步骤10：故障排除

### 10.1 常见问题和解决方案

#### 权限错误
```
Error: Resource not accessible by integration
```
**解决**: 在仓库Settings → Actions → General中设置"Read and write permissions"

#### 依赖安装失败
```
ERROR: Could not find a version that satisfies the requirement
```
**解决**: 检查requirements.txt格式，确保包名正确

#### PyInstaller打包失败
```
ModuleNotFoundError: No module named 'xxx'
```
**解决**: 添加隐式导入或检查相对路径问题

#### 文件路径错误
```
mv: cannot stat 'dist/main': No such file or directory
```
**解决**: 检查PyInstaller输出路径，确保文件确实生成

### 10.2 调试技巧

1. **添加调试输出**:
```yaml
- name: List dist directory
  run: ls -la dist/
```

2. **保留失败的构建**:
```yaml
- name: Upload failed build logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: build-logs
    path: build/
```

3. **使用tmate进行远程调试**:
```yaml
- name: Setup tmate session
  if: failure()
  uses: mxschmitt/action-tmate@v3
```

## 🎯 步骤11：最佳实践

### 11.1 版本管理
- 使用语义化版本号 (v1.0.0, v1.1.0)
- 避免重复使用同一版本号
- 为重要版本创建Release

### 11.2 安全考虑
- 不要在工作流中硬编码敏感信息
- 使用GitHub Secrets存储密钥
- 限制工作流权限到最小必要

### 11.3 性能优化
- 使用缓存减少构建时间
- 并行执行独立任务
- 只在必要时触发构建

### 11.4 文档维护
- 保持README更新
- 记录配置变更
- 提供清晰的使用说明

## 📚 总结

通过本教程，你学会了：

1. **理解GitHub Actions核心概念**
   - 工作流、任务、步骤的层级关系
   - 触发条件和权限配置

2. **掌握构建矩阵的使用**
   - 多平台并行构建
   - 灵活的参数配置

3. **学会编写完整的构建流程**
   - 环境准备、依赖安装、代码构建
   - 文件处理、上传分发

4. **了解故障排除和优化方法**
   - 常见问题的解决方案
   - 性能优化和最佳实践

现在你可以为任何Python项目创建类似的自动构建工作流，实现跨平台的自动化发布！

## 🔗 相关资源

- [GitHub Actions官方文档](https://docs.github.com/en/actions)
- [PyInstaller文档](https://pyinstaller.readthedocs.io/)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [YAML语法参考](https://yaml.org/spec/1.2.2/)

---

**作者**: 基于mysql-sea-sync项目实践总结  
**日期**: 2025-08-17  
**适用**: Python项目自动构建