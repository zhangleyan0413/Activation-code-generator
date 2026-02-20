#!/bin/bash

echo "=== 激活码生成工具启动脚本 ==="

# 检查Python是否安装
if command -v python3 &> /dev/null; then
    echo "Python已安装"
    PYTHON=python3
else
    echo "Python未安装，正在尝试安装..."
    
    # 在macOS上使用Homebrew安装Python
    if command -v brew &> /dev/null; then
        echo "使用Homebrew安装Python..."
        brew install python
    else
        echo "Homebrew未安装，正在安装Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # 重新检查Homebrew
        if command -v brew &> /dev/null; then
            echo "使用Homebrew安装Python..."
            brew install python
        else
            echo "无法安装Homebrew，请手动安装Python"
            exit 1
        fi
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
