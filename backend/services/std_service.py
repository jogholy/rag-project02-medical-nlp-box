from pymilvus import MilvusClient
from dotenv import load_dotenv
from utils.embedding_factory import EmbeddingFactory
from utils.embedding_config import EmbeddingProvider, EmbeddingConfig
import os
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class FinanceStdService:
    """
    金融术语标准化服务
    使用向量数据库进行金融术语的标准化和相似度搜索
    """
    def __init__(self, 
                 provider="huggingface",
                 model="BAAI/bge-m3",
                 db_path="db/finance_terms_simple.db",
                 collection_name="finance_terms"):
        """
        初始化金融术语标准化服务
        
        Args:
            provider: 嵌入模型提供商 (openai/bedrock/huggingface)
            model: 使用的模型名称
            db_path: Milvus 数据库路径
            collection_name: 集合名称
        """
        # 根据 provider 字符串匹配正确的枚举值
        provider_mapping = {
            'openai': EmbeddingProvider.OPENAI,
            'bedrock': EmbeddingProvider.BEDROCK,
            'huggingface': EmbeddingProvider.HUGGINGFACE
        }
        
        # 创建 embedding 函数
        embedding_provider = provider_mapping.get(provider.lower())
        if embedding_provider is None:
            raise ValueError(f"Unsupported provider: {provider}")
            
        config = EmbeddingConfig(
            provider=embedding_provider,
            model_name=model
        )
        self.embedding_func = EmbeddingFactory.create_embedding_function(config)
        
        # 连接 Milvus
        self.client = MilvusClient(db_path)
        self.collection_name = collection_name
        self.client.load_collection(self.collection_name)

    def search_similar_terms(self, query: str, limit: int = 5) -> List[Dict]:
        """
        搜索与查询文本相似的金融术语
        
        Args:
            query: 查询文本
            limit: 返回结果的最大数量
            
        Returns:
            包含相似术语信息的列表，每个术语包含：
            - term: 金融术语名称
            - category: 术语分类
            - input_file: 数据来源文件
            - similarity: 相似度分数（0-1，1为最相似）
            - distance: 距离分数（可选）
        """
        # 获取查询的向量表示
        query_embedding = self.embedding_func.embed_query(query)
        
        # 设置搜索参数
        search_params = {
            "collection_name": self.collection_name,
            "data": [query_embedding],
            "limit": limit,
            "output_fields": [
                "term", "category", "input_file"
            ]
        }
        
        # 搜索相似项
        search_result = self.client.search(**search_params)

        results = []
        if 'data' in search_result and len(search_result['data']) > 0:
            for hit in search_result['data'][0]:
                if 'entity' in hit:
                    results.append({
                        "term": hit['entity'].get('term'),
                        "category": hit['entity'].get('category'),
                        "input_file": hit['entity'].get('input_file'),
                        "similarity": 1 - float(hit['distance']) if 'distance' in hit else None,
                        "distance": float(hit['distance']) if 'distance' in hit else None
                    })
        return results

    def get_term_by_name(self, term_name: str) -> Dict:
        """
        根据术语名称精确查询金融术语
        
        Args:
            term_name: 金融术语名称
            
        Returns:
            包含术语信息的字典
        """
        query_result = self.client.query(
            collection_name=self.collection_name,
            filter=f"term == '{term_name}'",
            output_fields=["term", "category", "input_file"],
            limit=1
        )
        
        if 'data' in query_result and len(query_result['data']) > 0:
            return query_result['data'][0]
        return None

    def get_terms_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """
        根据分类查询金融术语
        
        Args:
            category: 术语分类
            limit: 返回结果的最大数量
            
        Returns:
            包含术语信息的列表
        """
        query_result = self.client.query(
            collection_name=self.collection_name,
            filter=f"category == '{category}'",
            output_fields=["term", "category", "input_file"],
            limit=limit
        )
        
        if 'data' in query_result:
            return query_result['data']
        return []

    def get_collection_stats(self) -> Dict:
        """
        获取集合统计信息
        
        Returns:
            包含统计信息的字典
        """
        return self.client.get_collection_stats(self.collection_name)

    def __del__(self):
        """清理资源，释放集合"""
        if hasattr(self, 'client') and hasattr(self, 'collection_name'):
            try:
                self.client.release_collection(self.collection_name)
            except Exception as e:
                logger.warning(f"Error releasing collection: {e}")

# 为了保持向后兼容，保留原来的类名作为别名
StdService = FinanceStdService