#!/usr/bin/env python3
"""
测试服务器 - 只启动基本的FastAPI应用
用于验证服务器是否能正常启动
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(title="Finance RAG Backend - Test Mode")

# 配置跨域资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径测试"""
    return {"message": "Finance RAG Backend is running in test mode"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "Server is running"}

@app.get("/api/test")
async def test_endpoint():
    """测试API端点"""
    return {"message": "API is working", "services": "Basic server only"}

if __name__ == "__main__":
    logger.info("Starting test server...")
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 