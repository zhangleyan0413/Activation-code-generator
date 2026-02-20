#!/bin/bash

echo "=== 激活码生成工具启动脚本 ==="

# 检查Python是否安装
if command -v python3 &> /dev/null; then
    echo "Python已安装"
    PYTHON=python3
else
    echo "Python未安装，正在尝试安装..."
    
    # 检测Linux发行版并尝试安装Python
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt update && sudo apt install -y python3 python3-pip
    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS/Fedora
        sudo dnf install -y python3 python3-pip || sudo yum install -y python3 python3-pip
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        sudo pacman -Syu --noconfirm python python-pip
    else
        echo "无法自动安装Python，请手动安装"
        exit 1
    fi
    
    if command -v python3 &> /dev/null; then
        echo "Python安装成功"
        PYTHON=python3
    else
        echo "Python安装失败，请手动安装"
        exit 1
    fi
fi

# 检查pip是否可用
if command -v pip3 &> /dev/null; then
    echo "pip已安装"
    PIP=pip3
else
    echo "pip未安装，正在尝试安装..."
    $PYTHON -m ensurepip --upgrade
    if command -v pip3 &> /dev/null; then
        echo "pip安装成功"
        PIP=pip3
    else
        echo "pip安装失败，请手动安装"
        exit 1
    fi
fi

# 检查wxPython是否安装
if $PIP show wxPython &> /dev/null; then
    echo "wxPython已安装"
else
    echo "wxPython未安装，正在安装..."
    $PIP install wxPython
    if $PIP show wxPython &> /dev/null; then
        echo "wxPython安装成功"
    else
        echo "wxPython安装失败，请尝试手动安装: $PIP install wxPython"
        exit 1
    fi
fi

echo "所有依赖已就绪，正在启动程序..."
$PYTHON main.py
