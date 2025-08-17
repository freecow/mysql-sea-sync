@echo off
echo ====================================
echo    MySQL-SeaTable 同步工具打包脚本
echo ====================================

echo 1. 安装依赖包...
pip install -r requirements.txt

echo.
echo 2. 清理之前的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo 3. 开始打包...
pyinstaller --onefile --console --name "mysql-seatable-sync" ^
  --add-data "*.json;." ^
  --add-data ".env.example;." ^
  --hidden-import seatable_api ^
  --hidden-import pymysql ^
  --hidden-import decimal ^
  --hidden-import datetime ^
  main.py

echo.
echo 4. 复制配置文件到dist目录...
if not exist "dist\config" mkdir "dist\config"
copy "*.json" "dist\config\"
copy ".env.example" "dist\"

echo.
echo ====================================
echo 打包完成！
echo 可执行文件位置：dist\mysql-seatable-sync.exe
echo 请将整个dist文件夹复制给同事使用
echo ====================================
pause