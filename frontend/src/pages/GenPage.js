import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { LLMOptions, TextInput } from '../components/shared/ModelOptions';

const GenPage = () => {
  // 基础状态
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  
  // 方法选择
  const [method, setMethod] = useState('generate_financial_note');
  const generationTypes = {
    generate_financial_note: '生成完整金融记录',
    generate_summary: '生成摘要',
    generate_qa: '生成问答对',
    generate_structured_data: '生成结构化数据'
  };

  // 患者信息
  const [patientInfo, setPatientInfo] = useState({
    financialHistory: ''
  });

  // 症状列表
  const [symptoms, setSymptoms] = useState('');
  const [diagnosis, setDiagnosis] = useState('');
  const [treatment, setTreatment] = useState('');

  // LLM 选项
  const [llmOptions, setLlmOptions] = useState({
    provider: 'ollama',
    model: 'qwen2.5:7b'
  });

  const handlePatientInfoChange = (e) => {
    const { name, value } = e.target;
    setPatientInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLlmOptionChange = (e) => {
    const { name, value } = e.target;
    setLlmOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSymptomsChange = (e) => {
    setSymptoms(e.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/gen', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_info: patientInfo,
          symptoms: symptoms.split('\n').filter(s => s.trim()),
          diagnosis,
          treatment,
          method,
          llmOptions
        }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Error:', error);
      setResult('处理请求时发生错误。');
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融内容生成 💰</h1>
      
      <div className="grid grid-cols-3 gap-6">
        {/* 左侧面板：输入表单 */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">患者信息</h2>
          
          {/* 患者基本信息 */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">金融历史</label>
              <textarea
                name="financialHistory"
                value={patientInfo.financialHistory}
                onChange={(e) => setPatientInfo({...patientInfo, financialHistory: e.target.value})}
                rows={3}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                placeholder="请输入金融历史信息..."
              />
            </div>
          </div>

          {/* 症状输入 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">症状（每行一个）</label>
            <TextInput
              value={symptoms}
              onChange={handleSymptomsChange}
              rows={3}
              placeholder="输入症状，每行一个..."
            />
          </div>

          {/* 诊断和治疗（仅在生成金融记录时显示） */}
          {method === 'generate_financial_note' && (
            <>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">诊断</label>
                <input
                  type="text"
                  value={diagnosis}
                  onChange={(e) => setDiagnosis(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  placeholder="输入诊断..."
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">治疗</label>
                <input
                  type="text"
                  value={treatment}
                  onChange={(e) => setTreatment(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  placeholder="输入治疗方案..."
                />
              </div>
            </>
          )}

          <button
            onClick={handleSubmit}
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? '生成中...' : '生成内容'}
          </button>
        </div>

        {/* 右侧面板：选项 */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">选项</h2>
          
          {/* 方法选择 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">生成方法</label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            >
              {Object.entries(generationTypes).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          {/* LLM 选项 */}
          <LLMOptions options={llmOptions} onChange={handleLlmOptionChange} />
        </div>
      </div>

      {/* 结果显示 */}
      {result && (
        <div className="mt-6">
          <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-6" role="alert">
            <p className="font-bold">生成结果：</p>
            <pre className="whitespace-pre-wrap">{result}</pre>
          </div>
        </div>
      )}

      <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md mt-6">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div>
    </div>
  );
};

export default GenPage; 