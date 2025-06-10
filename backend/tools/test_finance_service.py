#!/usr/bin/env python3
"""
金融术语标准化服务测试脚本
测试金融术语的搜索、查询等功能
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

def test_finance_service():
    """测试金融术语标准化服务"""
    
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
        test_queries = [
            "股票",
            "债券",
            "期权",
            "期货",
            "基金",
            "投资",
            "风险",
            "收益",
            "股票市场",
            "债券市场"
        ]
        
        logger.info("=" * 60)
        logger.info("测试相似术语搜索功能")
        logger.info("=" * 60)
        
        for query in test_queries:
            logger.info(f"\n搜索查询: '{query}'")
            results = service.search_similar_terms(query, limit=3)
            
            if results:
                logger.info("搜索结果:")
                for i, result in enumerate(results, 1):
                    logger.info(f"  {i}. {result['term']} (相似度: {result['similarity']:.4f})")
            else:
                logger.info("  未找到相关结果")
        
        # 测试精确查询
        logger.info("\n" + "=" * 60)
        logger.info("测试精确查询功能")
        logger.info("=" * 60)
        
        exact_terms = ["A-Share", "Bond", "Option", "Futures", "ETF"]
        
        for term in exact_terms:
            logger.info(f"\n精确查询: '{term}'")
            result = service.get_term_by_name(term)
            
            if result:
                logger.info(f"  找到: {result['term']} (分类: {result['category']})")
            else:
                logger.info(f"  未找到术语: {term}")
        
        # 测试分类查询
        logger.info("\n" + "=" * 60)
        logger.info("测试分类查询功能")
        logger.info("=" * 60)
        
        logger.info("\n查询FINTERM分类的术语:")
        category_results = service.get_terms_by_category("FINTERM", limit=5)
        
        for i, result in enumerate(category_results, 1):
            logger.info(f"  {i}. {result['term']}")
        
        logger.info("\n" + "=" * 60)
        logger.info("所有测试完成！")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_finance_service() 