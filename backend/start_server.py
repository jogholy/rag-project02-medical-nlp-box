#!/usr/bin/env python3
"""
后端服务器启动脚本
避免文件监视限制问题，并提供更好的错误处理
"""

import uvicorn
import logging
import os
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        # 设置环境变量
        os.environ["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
        
        # 配置服务器参数
        config = uvicorn.Config(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # 禁用热重载以避免文件监视问题
            log_level="info",
            access_log=True
        )
        
        # 创建服务器实例
        server = uvicorn.Server(config)
        
        logger.info("Starting backend server...")
        logger.info("Server will be available at http://0.0.0.0:8000")
        logger.info("Press Ctrl+C to stop the server")
        
        # 启动服务器
        server.run()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 