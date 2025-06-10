from pymilvus import model
from pymilvus import MilvusClient
import pandas as pd
from tqdm import tqdm
import logging
from dotenv import load_dotenv
load_dotenv()
import torch    
from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema
import os
import numpy as np

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建一个简单的嵌入函数，避免网络依赖
class SimpleEmbeddingFunction:
    def __init__(self, dimension=384):
        self.dimension = dimension
        
    def __call__(self, texts):
        """为文本生成简单的嵌入向量"""
        embeddings = []
        for text in texts:
            # 使用文本的字符编码生成一个简单的向量
            # 这是一个简化的方法，实际应用中应该使用真正的嵌入模型
            np.random.seed(hash(text) % 2**32)  # 使用文本的hash作为随机种子
            embedding = np.random.normal(0, 1, self.dimension)
            # 归一化向量
            embedding = embedding / np.linalg.norm(embedding)
            embeddings.append(embedding.tolist())
        return embeddings

# 初始化嵌入函数
embedding_function = SimpleEmbeddingFunction(dimension=384)

# 文件路径
file_path = "backend/tools/万条金融标准术语.csv"
db_path = "backend/db/finance_terms_simple.db"

# 确保db目录存在
os.makedirs("backend/db", exist_ok=True)

# 连接到 Milvus
client = MilvusClient(db_path)

collection_name = "finance_terms"

# 加载数据
logging.info("Loading data from CSV")
df = pd.read_csv(file_path, 
                 dtype=str, 
                 low_memory=False,
                 ).fillna("NA")

# 重命名列以便处理
df.columns = ['term', 'category']

logging.info(f"Loaded {len(df)} financial terms")

# 获取向量维度
vector_dim = 384

logging.info(f"Vector dimension: {vector_dim}")

# 构造Schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=vector_dim),
    FieldSchema(name="term", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="input_file", dtype=DataType.VARCHAR, max_length=500),
]
schema = CollectionSchema(fields, 
                          "Financial Terms Collection", 
                          enable_dynamic_field=True)

# 如果集合不存在，创建集合
if not client.has_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        schema=schema,
    )
    logging.info(f"Created new collection: {collection_name}")

# 在创建集合后添加索引
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="vector",
    index_type="AUTOINDEX",
    metric_type="COSINE",
    params={"nlist": 1024}
)

client.create_index(
    collection_name=collection_name,
    index_params=index_params
)

# 批量处理
batch_size = 1024

for start_idx in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
    end_idx = min(start_idx + batch_size, len(df))
    batch_df = df.iloc[start_idx:end_idx]

    # 准备文档 - 使用金融术语作为文档内容
    docs = batch_df['term'].tolist()

    # 生成嵌入
    try:
        embeddings = embedding_function(docs)
        logging.info(f"Generated embeddings for batch {start_idx // batch_size + 1}")
    except Exception as e:
        logging.error(f"Error generating embeddings for batch {start_idx // batch_size + 1}: {e}")
        continue

    # 准备数据
    data = [
        {
            "vector": embeddings[idx],
            "term": str(row['term']),
            "category": str(row['category']),
            "input_file": file_path
        } for idx, (_, row) in enumerate(batch_df.iterrows())
    ]

    # 插入数据
    try:
        res = client.insert(
            collection_name=collection_name,
            data=data
        )
        logging.info(f"Inserted batch {start_idx // batch_size + 1}, result: {res}")
    except Exception as e:
        logging.error(f"Error inserting batch {start_idx // batch_size + 1}: {e}")

logging.info("Insert process completed.")

# 示例查询
query = "股票"
query_embeddings = embedding_function([query])

# 搜索余弦相似度最高的
search_result = client.search(
    collection_name=collection_name,
    data=[query_embeddings[0]],
    limit=5,
    output_fields=["term", "category"]
)
logging.info(f"Search result for '{query}': {search_result}")

# 查询所有匹配的实体
query_result = client.query(
    collection_name=collection_name,
    filter="term == 'A-Share'",
    output_fields=["term", "category"],
    limit=5
)
logging.info(f"Query result for term == 'A-Share': {query_result}")

# 获取集合统计信息
collection_stats = client.get_collection_stats(collection_name)
logging.info(f"Collection statistics: {collection_stats}") 