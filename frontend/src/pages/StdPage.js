import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { EmbeddingOptions, TextInput } from '../components/shared/ModelOptions';

const StdPage = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // 金融术语类型选项
  const [options, setOptions] = useState({
    allFinancialTerms: true,
    stocks: true,
    bonds: true,
    derivatives: true,
    forex: true,
    commodities: true,
    mutualFunds: true,
    etf: true,
    banking: true,
    insurance: true,
    fintech: true,
  });

  const [embeddingOptions, setEmbeddingOptions] = useState({
    provider: 'huggingface',
    model: 'BAAI/bge-m3',
    dbName: 'finance_terms_simple',
    collectionName: 'finance_terms'
  });

  const handleOptionChange = (e) => {
    const { name, checked } = e.target;
    if (name === 'allFinancialTerms') {
      setOptions(prevOptions => {
        const newOptions = {};
        Object.keys(prevOptions).forEach(key => {
          newOptions[key] = checked;
        });
        return newOptions;
      });
    } else {
      setOptions(prevOptions => ({
        ...prevOptions,
        [name]: checked,
        allFinancialTerms: checked &&
          Object.entries(prevOptions)
            .filter(([key]) => key !== 'allFinancialTerms' && key !== name)
            .every(([, value]) => value)
      }));
    }
  };

  const handleEmbeddingOptionChange = (e) => {
    const { name, value } = e.target;
    setEmbeddingOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError('');
    setResult('');
    try {
      const response = await fetch('http://127.0.0.1:8000/api/std', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: input, 
          options,
          embeddingOptions 
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      setError(`An error occurred: ${error.message}`);
    }
    setIsLoading(false);
  };

  // 渲染金融术语类型选项
  const financialTypes = [
    ['stocks', '股票'],
    ['bonds', '债券'],
    ['derivatives', '衍生品'],
    ['forex', '外汇'],
    ['commodities', '大宗商品'],
    ['mutualFunds', '共同基金'],
    ['etf', '交易所交易基金'],
    ['banking', '银行业务'],
    ['insurance', '保险'],
    ['fintech', '金融科技'],
  ];

  // 渲染结果
  const renderResult = () => {
    if (!result) return null;
    
    // 处理后端返回的数据结构
    if (result.standardized_terms && Array.isArray(result.standardized_terms)) {
      return (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p className="font-bold">标准化结果：</p>
          <p className="mb-4">{result.message}</p>
          {result.standardized_terms.map((item, idx) => (
            <div key={idx} className="mb-4 p-3 bg-white rounded border">
              <div className="font-semibold text-blue-600">
                原始术语：{item.original_term}
              </div>
              <div className="text-sm text-gray-600 mb-2">
                实体类型：{item.entity_group}
              </div>
              {item.standardized_results && item.standardized_results.length > 0 ? (
                <div>
                  <div className="font-medium mb-2">标准化建议：</div>
                  <ul className="list-disc pl-6 space-y-2">
                    {item.standardized_results.map((std, stdIdx) => (
                      <li key={stdIdx} className="text-sm">
                        <div><b>标准术语：</b>{std.term}</div>
                        <div><b>分类：</b>{std.category}</div>
                        <div><b>相似度：</b>
                          {std.similarity !== undefined ? (std.similarity * 100).toFixed(2) + '%' : '-'}
                        </div>
                        {std.distance !== undefined && (
                          <div><b>距离：</b>{std.distance.toFixed(4)}</div>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <div className="text-gray-500">未找到相关标准化术语</div>
              )}
            </div>
          ))}
        </div>
      );
    } else if (Array.isArray(result)) {
      // 直接返回数组的情况
      return (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p className="font-bold">标准化结果：</p>
          <ul className="list-disc pl-6">
            {result.map((item, idx) => (
              <li key={idx} className="mb-2">
                <div><b>术语：</b>{item.term}</div>
                <div><b>分类：</b>{item.category}</div>
                <div><b>数据来源：</b>{item.input_file}</div>
                <div><b>相似度：</b>
                  {item.similarity !== undefined ? (item.similarity * 100).toFixed(2) + '%' : '-'}
                </div>
              </li>
            ))}
          </ul>
        </div>
      );
    } else if (typeof result === 'object') {
      // 单个对象的情况
      return (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p className="font-bold">标准化结果：</p>
          <div><b>术语：</b>{result.term}</div>
          <div><b>分类：</b>{result.category}</div>
          <div><b>数据来源：</b>{result.input_file}</div>
          <div><b>相似度：</b>
            {result.similarity !== undefined ? (result.similarity * 100).toFixed(2) + '%' : '-'}
          </div>
        </div>
      );
    } else {
      // 其他情况，显示原始数据
      return (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p className="font-bold">结果：</p>
          <pre className="whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      );
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融术语标准化 📚</h1>
      <div className="grid grid-cols-3 gap-6">
        {/* 左侧面板：文本输入和嵌入选项 */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">输入金融术语</h2>
          <TextInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={4}
            placeholder="请输入需要标准化的金融术语，例如：股票、债券、期权、期货等..."
          />
          
          <EmbeddingOptions options={embeddingOptions} onChange={handleEmbeddingOptionChange} />

          <button
            onClick={handleSubmit}
            className="bg-purple-500 text-white px-4 py-2 rounded-md hover:bg-purple-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? '处理中...' : '标准化术语'}
          </button>
        </div>

        {/* 右侧面板：选项列表 */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">金融术语类型</h2>
          <div className="space-y-3">
            {financialTypes.map(([key, label]) => (
              <div key={key} className="flex items-center">
                <input
                  type="checkbox"
                  id={key}
                  name={key}
                  checked={options[key]}
                  onChange={handleOptionChange}
                  className="mr-2"
                />
                <label htmlFor={key}>{label}</label>
              </div>
            ))}
            
            <div className="flex items-center pt-4 border-t">
              <input
                type="checkbox"
                id="allFinancialTerms"
                name="allFinancialTerms"
                checked={options.allFinancialTerms}
                onChange={handleOptionChange}
                className="mr-2"
              />
              <label htmlFor="allFinancialTerms" className="font-semibold">所有金融术语</label>
            </div>
          </div>
        </div>
      </div>
      
      {/* 结果显示区域 */}
      {(error || result) && (
        <div className="mt-6">
          {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
              <p className="font-bold">错误：</p>
              <p>{error}</p>
            </div>
          )}
          {renderResult()}
        </div>
      )}

      <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md mt-6">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div>
    </div>
  );
};

export default StdPage;