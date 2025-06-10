from pymilvus import MilvusClient
import numpy as np
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 连接到数据库
db_path = "db/finance_terms_simple.db"
client = MilvusClient(db_path)
collection_name = "finance_terms"

# 简单的嵌入函数（与创建时相同）
class SimpleEmbeddingFunction:
    def __init__(self, dimension=384):
        self.dimension = dimension
        
    def __call__(self, texts):
        embeddings = []
        for text in texts:
            np.random.seed(hash(text) % 2**32)
            embedding = np.random.normal(0, 1, self.dimension)
            embedding = embedding / np.linalg.norm(embedding)
            embeddings.append(embedding.tolist())
        return embeddings

embedding_function = SimpleEmbeddingFunction(dimension=384)

def test_search(query_text, limit=5):
    """测试搜索功能"""
    logging.info(f"搜索查询: '{query_text}'")
    
    # 生成查询向量
    query_embeddings = embedding_function([query_text])
    
    # 执行搜索
    search_result = client.search(
        collection_name=collection_name,
        data=[query_embeddings[0]],
        limit=limit,
        output_fields=["term", "category"]
    )
    
    logging.info("搜索结果:")
    # 修复结果处理逻辑
    if 'data' in search_result and len(search_result['data']) > 0:
        for i, result in enumerate(search_result['data'][0]):
            if 'entity' in result:
                logging.info(f"  {i+1}. {result['entity']['term']} (相似度: {1 - result['distance']:.4f})")
            else:
                logging.info(f"  {i+1}. {result}")
    else:
        logging.info(f"  搜索结果: {search_result}")
    
    return search_result

def test_query(filter_condition, limit=5):
    """测试精确查询功能"""
    logging.info(f"精确查询: {filter_condition}")
    
    query_result = client.query(
        collection_name=collection_name,
        filter=filter_condition,
        output_fields=["term", "category"],
        limit=limit
    )
    
    logging.info("查询结果:")
    if 'data' in query_result and len(query_result['data']) > 0:
        for i, result in enumerate(query_result['data']):
            logging.info(f"  {i+1}. {result['term']} ({result['category']})")
    else:
        logging.info(f"  查询结果: {query_result}")
    
    return query_result

def get_collection_stats():
    """获取集合统计信息"""
    stats = client.get_collection_stats(collection_name)
    logging.info(f"集合统计: {stats}")
    return stats

if __name__ == "__main__":
    logging.info("开始测试金融术语向量数据库...")
    
    # 获取集合统计信息
    get_collection_stats()
    
    # 测试搜索功能
    test_queries = [
        "股票",
        "债券",
        "期权",
        "期货",
        "基金",
        "投资",
        "风险",
        "收益"
    ]
    
    for query in test_queries:
        test_search(query)
        print("-" * 50)
    
    # 测试精确查询
    test_query("term == 'A-Share'")
    test_query("term == 'Bond'")
    test_query("term == 'Option'")
    
    logging.info("测试完成！") 