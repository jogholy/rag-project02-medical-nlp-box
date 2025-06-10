from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Literal, Union, Any
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(title="Finance RAG Backend - Offline Mode")

# 配置跨域资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础模型类
class BaseInputModel(BaseModel):
    """基础输入模型，包含所有模型共享的字段"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    llmOptions: Dict[str, str] = Field(
        default_factory=lambda: {
            "provider": "ollama",
            "model": "qwen2.5:7b"
        },
        description="大语言模型配置选项"
    )

class TextInput(BaseInputModel):
    """文本输入模型"""
    text: str = Field(..., description="输入文本")
    options: Dict[str, bool] = Field(
        default_factory=dict,
        description="处理选项"
    )

# 健康检查端点
@app.get("/")
async def root():
    """根路径"""
    return {"message": "Finance RAG Backend is running in offline mode"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "Server is running in offline mode"}

# 模拟的API端点
@app.post("/api/ner")
async def ner(input: TextInput):
    """命名实体识别 - 离线模式"""
    return {
        "text": input.text,
        "entities": [],
        "message": "NER service not available in offline mode",
        "mode": "offline"
    }

@app.post("/api/std")
async def standardization(input: TextInput):
    """金融术语标准化 - 离线模式"""
    return {
        "message": "Standardization service not available in offline mode",
        "standardized_terms": [],
        "mode": "offline"
    }

@app.post("/api/abbr")
async def expand_abbreviations(input: TextInput):
    """缩写扩展 - 离线模式"""
    return {
        "text": input.text,
        "expanded_text": input.text,
        "message": "Abbreviation service not available in offline mode",
        "mode": "offline"
    }

@app.post("/api/corr")
async def correct_notes(input: TextInput):
    """拼写纠正 - 离线模式"""
    return {
        "text": input.text,
        "corrected_text": input.text,
        "message": "Correction service not available in offline mode",
        "mode": "offline"
    }

@app.post("/api/gen")
async def generate_financial_content(input: TextInput):
    """金融内容生成 - 离线模式"""
    return {
        "generated_content": "Content generation not available in offline mode",
        "message": "Generation service not available in offline mode",
        "mode": "offline"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting backend server in offline mode...")
    uvicorn.run(
        "main_offline:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 