#!/usr/bin/env python3
"""
API集成测试脚本
测试金融术语标准化API是否正常工作
"""

import requests
import json
import sys
import os

def test_finance_std_api():
    """测试金融术语标准化API"""
    
    # API端点
    url = "http://127.0.0.1:8000/api/std"
    
    # 测试数据
    test_cases = [
        {
            "text": "股票投资",
            "description": "测试股票相关术语"
        },
        {
            "text": "债券市场",
            "description": "测试债券相关术语"
        },
        {
            "text": "期权交易",
            "description": "测试衍生品相关术语"
        },
        {
            "text": "共同基金",
            "description": "测试基金相关术语"
        }
    ]
    
    print("=" * 60)
    print("开始测试金融术语标准化API")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['description']}")
        print(f"输入文本: {test_case['text']}")
        
        # 准备请求数据
        payload = {
            "text": test_case['text'],
            "options": {
                "allFinancialTerms": True,
                "stocks": True,
                "bonds": True,
                "derivatives": True,
                "forex": True,
                "commodities": True,
                "mutualFunds": True,
                "etf": True,
                "banking": True,
                "insurance": True,
                "fintech": True
            },
            "embeddingOptions": {
                "provider": "huggingface",
                "model": "BAAI/bge-m3",
                "dbName": "finance_terms_simple",
                "collectionName": "finance_terms"
            }
        }
        
        try:
            # 发送请求
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 请求成功")
                print(f"返回消息: {result.get('message', 'N/A')}")
                
                if 'standardized_terms' in result:
                    terms = result['standardized_terms']
                    print(f"识别到 {len(terms)} 个术语:")
                    
                    for j, term in enumerate(terms, 1):
                        print(f"  {j}. 原始术语: {term.get('original_term', 'N/A')}")
                        print(f"     实体类型: {term.get('entity_group', 'N/A')}")
                        
                        std_results = term.get('standardized_results', [])
                        if std_results:
                            print(f"     标准化建议:")
                            for k, std in enumerate(std_results[:3], 1):  # 只显示前3个
                                print(f"       {k}. {std.get('term', 'N/A')} (相似度: {std.get('similarity', 0):.4f})")
                        else:
                            print(f"     未找到标准化建议")
                else:
                    print("❌ 未返回标准化术语")
            else:
                print(f"❌ 请求失败: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ 连接失败: 请确保后端服务器正在运行 (python backend/main.py)")
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
        except Exception as e:
            print(f"❌ 其他错误: {str(e)}")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("API集成测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_finance_std_api() 