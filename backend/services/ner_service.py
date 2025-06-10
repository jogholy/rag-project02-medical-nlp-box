from transformers import pipeline
import torch
import logging
import os
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NERService:
    """
    金融术语命名实体识别服务
    使用规则基础的方法进行金融文本的实体识别
    """
    def __init__(self):
        self.financial_patterns = self._initialize_patterns()
        logger.info("NER service initialized with rule-based patterns")
    
    def _initialize_patterns(self):
        """初始化金融术语识别模式"""
        patterns = {
            'STOCK': [
                r'股票', r'股份', r'股权', r'A股', r'B股', r'H股', r'蓝筹股', r'成长股', r'价值股', 
                r'小盘股', r'大盘股', r'新股', r'次新股', r'ST股', r'\*ST股', r'退市股'
            ],
            'STOCK_INDEX': [
                r'上证指数', r'深证成指', r'创业板指', r'科创50', r'沪深300', r'中证500', 
                r'上证50', r'中证1000', r'恒生指数', r'道琼斯', r'纳斯达克', r'标普500'
            ],
            'INVESTMENT': [
                r'投资', r'理财', r'基金', r'债券', r'期货', r'期权', r'外汇', r'黄金', 
                r'白银', r'原油', r'房地产', r'REITs', r'ETF', r'LOF', r'QDII'
            ],
            'FINANCIAL_INSTITUTION': [
                r'银行', r'证券公司', r'基金公司', r'保险公司', r'信托公司', r'期货公司',
                r'投资银行', r'商业银行', r'政策性银行', r'央行', r'证监会', r'银保监会'
            ],
            'FINANCIAL_TERM': [
                r'收益率', r'风险', r'波动率', r'市盈率', r'市净率', r'股息率', r'换手率',
                r'成交量', r'成交额', r'涨跌幅', r'涨停', r'跌停', r'停牌', r'复牌',
                r'配股', r'增发', r'分红', r'送股', r'转增', r'除权', r'除息'
            ],
            'CURRENCY': [
                r'人民币', r'美元', r'欧元', r'日元', r'英镑', r'港币', r'澳元', r'加元',
                r'瑞士法郎', r'新加坡元', r'韩元', r'泰铢', r'卢布', r'印度卢比'
            ],
            'MARKET': [
                r'股市', r'债市', r'汇市', r'期市', r'房市', r'金市', r'油市', r'牛市', r'熊市',
                r'主板', r'创业板', r'科创板', r'新三板', r'北交所', r'上交所', r'深交所'
            ]
        }
        return patterns
  
    def process(self, text, options, term_types):
        """
        处理输入文本，识别金融术语实体
        
        Args:
            text: 输入文本
            options: 处理选项
            term_types: 需要识别的术语类型
            
        Returns:
            包含识别出的实体和原始文本的字典
        """
        try:
            # 使用规则基础的方法进行实体识别
            entities = self._extract_entities(text)
            
            # 根据术语类型过滤实体
            filtered_entities = self._filter_entities(entities, term_types)
            
            return {
                "text": text,
                "entities": filtered_entities
            }
        except Exception as e:
            logger.error(f"Error processing text with NER: {e}")
            return {
                "text": text,
                "entities": [],
                "error": f"Processing error: {str(e)}"
            }

    def _extract_entities(self, text):
        """使用规则基础的方法提取金融实体"""
        entities = []
        
        logger.info(f"Extracting entities from text: {text}")
        
        for entity_type, patterns in self.financial_patterns.items():
            logger.info(f"Processing entity type: {entity_type}")
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    entity = {
                        'entity_group': entity_type,
                        'word': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'score': 0.9  # 规则基础的方法给予较高置信度
                    }
                    entities.append(entity)
                    logger.info(f"Found entity: {entity}")
        
        # 移除重叠实体，保留最长的
        entities = self._remove_overlapping_entities(entities)
        logger.info(f"Final entities after removing overlaps: {entities}")
        
        return entities

    def _remove_overlapping_entities(self, entities):
        """移除重叠的实体，保留最长的实体"""
        # 按开始位置排序
        sorted_entities = sorted(entities, key=lambda x: x['start'])
        non_overlapping = []
        last_end = -1

        for entity in sorted_entities:
            # 如果当前实体与之前的实体不重叠，直接添加
            if entity['start'] >= last_end:
                non_overlapping.append(entity)
                last_end = entity['end']
            else:
                # 如果重叠，保留较长的实体
                if entity['end'] - entity['start'] > last_end - non_overlapping[-1]['start']:
                    non_overlapping[-1] = entity
                    last_end = entity['end']

        return non_overlapping

    def _filter_entities(self, entities, term_types):
        """
        根据术语类型过滤实体
        """
        if not term_types:
            return entities
            
        filtered_result = []
        for entity in entities:
            # 如果启用了所有金融术语，则包含所有实体
            if term_types.get('allFinancialTerms', False):
                filtered_result.append(entity)
            # 否则根据具体类型过滤
            elif (term_types.get('stocks', False) and entity['entity_group'] == 'STOCK') or \
                 (term_types.get('bonds', False) and entity['entity_group'] == 'INVESTMENT') or \
                 (term_types.get('derivatives', False) and entity['entity_group'] == 'INVESTMENT') or \
                 (term_types.get('forex', False) and entity['entity_group'] == 'CURRENCY') or \
                 (term_types.get('commodities', False) and entity['entity_group'] == 'INVESTMENT') or \
                 (term_types.get('mutualFunds', False) and entity['entity_group'] == 'INVESTMENT') or \
                 (term_types.get('etf', False) and entity['entity_group'] == 'INVESTMENT') or \
                 (term_types.get('banking', False) and entity['entity_group'] == 'FINANCIAL_INSTITUTION') or \
                 (term_types.get('insurance', False) and entity['entity_group'] == 'FINANCIAL_INSTITUTION') or \
                 (term_types.get('fintech', False) and entity['entity_group'] == 'FINANCIAL_TERM'):
                filtered_result.append(entity)
        
        return filtered_result




