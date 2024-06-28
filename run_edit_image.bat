@echo off
chcp 936
setlocal enabledelayedexpansion

rem 设置 OpenMP 环境变量
set KMP_DUPLICATE_LIB_OK=TRUE

rem 设置 CUDA 环境变量
set CUDA_VISIBLE_DEVICES=0

rem 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"

rem 设置 Anaconda 路径（请根据您的实际安装路径进行修改）
set "ANACONDA_PATH=C:\ProgramData\Anaconda3"

rem 激活 Conda 环境
call "%ANACONDA_PATH%\Scripts\activate.bat" instruct_pix2pix

rem 切换到脚本所在目录
cd /d "%SCRIPT_DIR%"

rem 运行 Python 脚本
python edit_image.py

rem 暂停以查看输出
pause
