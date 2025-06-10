#!/usr/bin/env python3
"""
简单的金融术语标准化服务测试脚本
测试修复后的服务是否能正常工作
"""

import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

try:
    from services.std_service import FinanceStdService
    import logging
except ImportError as e:
    print(f"导入错误: {e}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    sys.exit(1)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_simple_search():
    """测试简单的搜索功能"""
    
    try:
        # 初始化服务
        logger.info("初始化金融术语标准化服务...")
        service = FinanceStdService(
            provider="huggingface",
            model="BAAI/bge-m3",
            db_path="db/finance_terms_simple.db",
            collection_name="finance_terms"
        )
        
        # 获取集合统计信息
        logger.info("获取集合统计信息...")
        stats = service.get_collection_stats()
        logger.info(f"数据库统计: {stats}")
        
        # 测试相似术语搜索
        test_query = "股票"
        logger.info(f"测试搜索: '{test_query}'")
        
        results = service.search_similar_terms(test_query, limit=3)
        logger.info(f"搜索结果: {results}")
        
        if results:
            logger.info("✅ 搜索功能正常工作！")
            for i, result in enumerate(results, 1):
                logger.info(f"  {i}. {result['term']} (相似度: {result.get('similarity', 'N/A')})")
        else:
            logger.warning("⚠️ 没有找到搜索结果")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    logger.info("开始测试修复后的金融术语标准化服务...")
    
    success = test_simple_search()
    
    if success:
        logger.info("🎉 测试成功！修复有效。")
    else:
        logger.error("💥 测试失败！需要进一步调试。") 