#!/usr/bin/env python3
"""
一键部署脚本
快速创建可发送给同事的完整部署包
"""

import os
import sys
import shutil
import subprocess
import zipfile
from datetime import datetime

def quick_deploy():
    print("🚀 MySQL-SeaTable 同步工具一键部署")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ["main.py", "requirements.txt"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    # 1. 运行独立打包
    print("📦 开始创建独立部署包...")
    try:
        result = subprocess.run([sys.executable, "build_standalone.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ 部署包创建成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署包创建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    # 2. 创建压缩包
    deploy_dir = "mysql-seatable-sync-deploy"
    if not os.path.exists(deploy_dir):
        print(f"❌ 找不到部署目录: {deploy_dir}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"mysql-seatable-sync_{timestamp}.zip"
    
    print(f"📁 创建压缩包: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    # 3. 显示完成信息
    zip_size = os.path.getsize(zip_name) / (1024 * 1024)  # MB
    
    print("\n🎉 一键部署完成！")
    print("=" * 50)
    print(f"📦 压缩包: {zip_name}")
    print(f"📏 文件大小: {zip_size:.1f} MB")
    print(f"📂 部署目录: {deploy_dir}/")
    print("\n📋 发送给同事的文件:")
    print(f"   → {zip_name} (推荐：直接发送压缩包)")
    print(f"   → 或整个 {deploy_dir}/ 文件夹")
    
    print("\n📝 同事使用步骤:")
    print("   1. 解压缩文件")
    print("   2. 复制 .env.example 为 .env")
    print("   3. 编辑 .env 填入数据库信息")
    print("   4. 运行可执行文件")
    
    print("\n💡 提示:")
    print("   - 压缩包包含所有必要文件")
    print("   - 无需安装 Python 或依赖包")
    print("   - 支持 Windows、macOS、Linux")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = quick_deploy()
    if not success:
        print("\n❌ 部署失败，请检查错误信息")
        sys.exit(1)
    else:
        print("\n✅ 部署成功完成！")