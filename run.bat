@echo off
chcp 65001

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python已安装
    goto check_pip
)

echo Python未安装，正在准备安装...

REM 检测系统架构
for /f "tokens=2 delims==" %%a in ('wmic os get osarchitecture /value') do set "ARCH=%%a"

REM 根据架构设置Python下载链接
if "%ARCH%" equ "64-bit" (
    set "PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
) else (
    set "PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9.exe"
)

set "PYTHON_EXE=python-installer.exe"

echo 检测到系统架构: %ARCH%
echo 正在下载Python...

REM 下载Python安装包
if exist "%SYSTEMROOT%\System32\curl.exe" (
    curl -o "%PYTHON_EXE%" "%PYTHON_URL%"
) else if exist "%SYSTEMROOT%\System32\bitsadmin.exe" (
    bitsadmin /transfer python_download /download /priority foreground "%PYTHON_URL%" "%CD%\%PYTHON_EXE%"
) else (
    echo 无法下载Python，请手动访问 https://www.python.org/downloads/ 下载并安装
    pause
    exit /b 1
)

REM 检查下载是否成功
if not exist "%PYTHON_EXE%" (
    echo Python下载失败，请手动下载并安装
    pause
    exit /b 1
)

echo Python下载成功，正在安装...

REM 静默安装Python
"%PYTHON_EXE%" /quiet PrependPath=1 Include_pip=1

REM 检查安装是否成功
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python安装失败，请尝试手动安装
    pause
    exit /b 1
)

echo Python安装成功

REM 清理安装包
del "%PYTHON_EXE%" >nul 2>&1

:check_pip
REM 检查pip是否可用
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip未安装，正在尝试安装...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo pip安装失败，请重新安装Python
        pause
        exit /b 1
    )
    echo pip安装成功
) else (
    echo pip已安装
)

REM 检查wxPython是否安装
pip show wxPython >nul 2>&1
if %errorlevel% neq 0 (
    echo wxPython未安装，正在安装...
    pip install wxPython
    if %errorlevel% neq 0 (
        echo wxPython安装失败，请尝试手动安装: pip install wxPython
        pause
        exit /b 1
    )
    echo wxPython安装成功
) else (
    echo wxPython已安装
)

echo 所有依赖已就绪，正在启动程序...

REM 尝试使用pythonw.exe隐藏命令窗口
where pythonw.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo 使用pythonw.exe启动程序（无命令窗口）...
    pythonw.exe main.py
) else (
    echo pythonw.exe未找到，使用python.exe启动程序...
    python.exe main.py
)

REM 程序已启动，批处理文件结束
