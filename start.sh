#!/bin/bash

# 学术论文生成系统 - 简化版启动脚本

echo "🚀 启动学术论文生成系统（简化版）"
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "Python版本: $python_version"

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "虚拟环境: $VIRTUAL_ENV"
else
    echo "⚠️  建议使用虚拟环境"
fi

# 创建必要的目录
echo "📁 创建必要目录..."
mkdir -p uploads logs

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env文件不存在，请参考.env.example创建配置文件"
    echo "💡 建议复制.env.example为.env并配置API密钥"
    if [ -f ".env.example" ]; then
        echo "   cp .env.example .env"
    fi
fi

# 安装依赖
echo "📦 检查依赖..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ requirements.txt不存在"
    exit 1
fi

echo ""
echo "🎯 启动选项："
echo "1. 直接启动 (python app.py)"
echo "2. 使用Docker (docker-compose up --build)"
echo ""

# 根据参数选择启动方式
if [ "$1" = "docker" ]; then
    echo "🐳 使用Docker启动..."
    docker-compose up --build
elif [ "$1" = "test" ]; then
    echo "🧪 运行测试..."
    python test_simplified.py
else
    echo "🚀 直接启动服务..."
    echo "服务将在 http://localhost:5000 启动"
    echo "健康检查: http://localhost:5000/health"
    echo "API信息: http://localhost:5000/api_info"
    echo ""
    echo "按 Ctrl+C 停止服务"
    echo ""
    
    # 启动应用
    python app.py
fi