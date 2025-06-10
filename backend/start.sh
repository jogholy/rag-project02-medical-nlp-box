#!/bin/bash

# 后端服务器启动脚本
# 提供多种启动模式

echo "=== Finance RAG Backend 启动脚本 ==="
echo "1. 离线模式 (推荐，避免网络问题)"
echo "2. 完整模式 (需要网络连接)"
echo "3. 测试模式 (仅基本功能)"
echo "4. 退出"
echo ""

read -p "请选择启动模式 (1-4): " choice

case $choice in
    1)
        echo "启动离线模式..."
        python main_offline.py
        ;;
    2)
        echo "启动完整模式..."
        python start_server.py
        ;;
    3)
        echo "启动测试模式..."
        python test_server.py
        ;;
    4)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择，默认启动离线模式..."
        python main_offline.py
        ;;
esac 