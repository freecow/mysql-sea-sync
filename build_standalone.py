#!/usr/bin/env python3
"""
独立打包脚本
创建完全自包含的可执行文件，包含所有配置文件
"""

import os
import sys
import shutil
import subprocess
import json

def create_standalone_build():
    print("====================================")
    print("   创建独立自包含部署包")
    print("====================================")
    
    # 1. 安装依赖
    print("1. 安装依赖包...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # 2. 清理旧文件
    print("\n2. 清理之前的构建文件...")
    for folder in ["dist", "build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    for file in os.listdir("."):
        if file.endswith(".spec"):
            os.remove(file)
    
    # 3. 收集所有JSON配置文件
    json_files = [f for f in os.listdir(".") if f.endswith(".json")]
    print(f"\n3. 找到配置文件: {', '.join(json_files)}")
    
    # 4. 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name", "mysql-seatable-sync",
        "--hidden-import", "seatable_api",
        "--hidden-import", "pymysql", 
        "--hidden-import", "decimal",
        "--hidden-import", "datetime",
        "--hidden-import", "json",
        "--hidden-import", "dotenv"
    ]
    
    # 添加所有JSON文件
    for json_file in json_files:
        cmd.extend(["--add-data", f"{json_file}:."])
    
    # 添加.env.example
    cmd.extend(["--add-data", ".env.example:."])
    
    # 添加主文件
    cmd.append("main.py")
    
    print(f"\n4. 执行打包命令...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ 打包成功！")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败: {e}")
        return False
    
    # 5. 创建部署包
    print("\n5. 创建部署包...")
    
    # 创建部署目录
    deploy_dir = "mysql-seatable-sync-deploy"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # 复制可执行文件
    exe_name = "mysql-seatable-sync.exe" if sys.platform.startswith("win") else "mysql-seatable-sync"
    src_exe = os.path.join("dist", exe_name)
    dst_exe = os.path.join(deploy_dir, exe_name)
    
    if os.path.exists(src_exe):
        shutil.copy2(src_exe, dst_exe)
        print(f"✅ 复制可执行文件: {exe_name}")
    else:
        print(f"❌ 找不到可执行文件: {src_exe}")
        return False
    
    # 复制配置文件示例
    shutil.copy2(".env.example", os.path.join(deploy_dir, ".env.example"))
    
    # 创建使用说明
    readme_content = """# MySQL-SeaTable 同步工具部署包

## 使用步骤：

1. 复制 .env.example 为 .env
2. 编辑 .env 文件，填入正确的数据库连接信息
3. 运行可执行文件开始同步

## 配置说明：

- 该可执行文件已包含所有配置文件和依赖
- 首次使用需要配置 .env 文件中的数据库连接信息
- 支持多个数据库连接和多种同步任务

## 注意事项：

- 确保网络能访问MySQL数据库和SeaTable服务
- 确保数据库用户有相应的读取权限
- 首次运行可能需要管理员权限（某些系统）
"""
    
    with open(os.path.join(deploy_dir, "README.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("\n====================================")
    print("🎉 部署包创建完成！")
    print(f"📁 部署包位置: {deploy_dir}/")
    print(f"🚀 可执行文件: {deploy_dir}/{exe_name}")
    print("📋 请将整个文件夹发送给同事")
    print("====================================")
    
    return True

if __name__ == "__main__":
    success = create_standalone_build()
    if not success:
        sys.exit(1)