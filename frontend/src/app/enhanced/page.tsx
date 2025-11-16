'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function EnhancedAnalysis() {
    const [ sessionId, setSessionId ] = useState<string>('');
    const [ query, setQuery ] = useState<string>('');
    const [ datasetSearch, setDatasetSearch ] = useState<string>('');
    const [ datasets, setDatasets ] = useState<any[]>([]);
    const [ selectedDataset, setSelectedDataset ] = useState<string>('');
    const [ loading, setLoading ] = useState(false);
    const [ results, setResults ] = useState<any>(null);
    const [ autoEDA, setAutoEDA ] = useState(true);
    const [ autoML, setAutoML ] = useState(false);

    useEffect(() => {
        createSession();
    }, []);

    const createSession = async () => {
        try {
            const res = await axios.post(`${API_URL}/api/v1/sessions`, {});
            setSessionId(res.data.session_id);
        } catch (error) {
            console.error('Failed to create session:', error);
        }
    };

    const searchDatasets = async () => {
        if (!datasetSearch.trim()) return;

        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/api/v1/datasets/search`, {
                query: datasetSearch
            });
            setDatasets(res.data.datasets || []);
        } catch (error) {
            console.error('Search failed:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAnalysis = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/api/v1/query/enhanced`, {
                session_id: sessionId,
                query: query,
                dataset_id: selectedDataset || null,
                auto_eda: autoEDA,
                auto_ml: autoML
            });

            setResults(res.data);
        } catch (error) {
            console.error('Analysis failed:', error);
            alert('Analysis failed. Check console for details.');
        } finally {
            setLoading(false);
        }
    };

    const quickAnalysis = async (type: string) => {
        if (!selectedDataset) {
            alert('Please select a dataset first');
            return;
        }

        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/api/v1/analysis/auto`, {
                session_id: sessionId,
                dataset_id: selectedDataset,
                analysis_type: type
            });

            setResults(res.data);
        } catch (error) {
            console.error('Auto analysis failed:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <header className="bg-white shadow-lg">
                <div className="max-w-7xl mx-auto py-6 px-4">
                    <h1 className="text-4xl font-bold text-indigo-900">
                        🤖 AI Data Science Research Assistant
                    </h1>
                    <p className="text-sm text-gray-600 mt-2">
                        Your personal AI Data Scientist • Session: {sessionId.slice(0, 8)}...
                    </p>
                </div>
            </header>

            <main className="max-w-7xl mx-auto py-8 px-4">
                {/* Dataset Search */}
                <div className="bg-white shadow-lg rounded-xl p-6 mb-6">
                    <h2 className="text-2xl font-bold mb-4 text-gray-800">🔍 Find Dataset</h2>
                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={datasetSearch}
                            onChange={(e) => setDatasetSearch(e.target.value)}
                            placeholder="Search Kaggle datasets (e.g., housing, sales, covid)"
                            className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none"
                        />
                        <button
                            onClick={searchDatasets}
                            disabled={loading}
                            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 font-semibold"
                        >
                            Search
                        </button>
                    </div>

                    {datasets.length > 0 && (
                        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
                            {datasets.map((ds, idx) => (
                                <div
                                    key={idx}
                                    onClick={() => setSelectedDataset(ds.id)}
                                    className={`p-4 border-2 rounded-lg cursor-pointer transition ${selectedDataset === ds.id
                                            ? 'border-indigo-600 bg-indigo-50'
                                            : 'border-gray-200 hover:border-indigo-300'
                                        }`}
                                >
                                    <h3 className="font-semibold text-gray-900">{ds.title}</h3>
                                    <p className="text-sm text-gray-600 mt-1">ID: {ds.id}</p>
                                    <p className="text-xs text-gray-500 mt-1">Size: {ds.size}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Quick Actions */}
                {selectedDataset && (
                    <div className="bg-white shadow-lg rounded-xl p-6 mb-6">
                        <h2 className="text-2xl font-bold mb-4 text-gray-800">⚡ Quick Analysis</h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <button
                                onClick={() => quickAnalysis('eda')}
                                disabled={loading}
                                className="p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-400 font-semibold"
                            >
                                📊 Auto EDA
                            </button>
                            <button
                                onClick={() => quickAnalysis('ml')}
                                disabled={loading}
                                className="p-4 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:bg-gray-400 font-semibold"
                            >
                                🤖 Auto ML
                            </button>
                            <button
                                onClick={() => quickAnalysis('full')}
                                disabled={loading}
                                className="p-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 font-semibold"
                            >
                                🚀 Full Analysis
                            </button>
                        </div>
                    </div>
                )}

                {/* Custom Query */}
                <div className="bg-white shadow-lg rounded-xl p-6 mb-6">
                    <h2 className="text-2xl font-bold mb-4 text-gray-800">💬 Ask Your Question</h2>
                    <form onSubmit={handleAnalysis}>
                        <textarea
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Ask anything: 'What are the top factors affecting sales?' or 'Build a prediction model' or 'Show me correlations'"
                            rows={4}
                            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none"
                        />

                        <div className="flex gap-4 mt-4">
                            <label className="flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    checked={autoEDA}
                                    onChange={(e) => setAutoEDA(e.target.checked)}
                                    className="w-5 h-5"
                                />
                                <span className="text-gray-700">Auto EDA</span>
                            </label>
                            <label className="flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    checked={autoML}
                                    onChange={(e) => setAutoML(e.target.checked)}
                                    className="w-5 h-5"
                                />
                                <span className="text-gray-700">Auto ML</span>
                            </label>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full mt-4 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 font-bold text-lg"
                        >
                            {loading ? '🔄 Analyzing...' : '🚀 Analyze Now'}
                        </button>
                    </form>
                </div>

                {/* Results */}
                {results && (
                    <div className="bg-white shadow-lg rounded-xl p-6">
                        <h2 className="text-2xl font-bold mb-4 text-gray-800">📈 Results</h2>

                        {results.eda_summary && (
                            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                                <h3 className="font-bold text-lg mb-2 text-blue-900">📊 EDA Summary</h3>
                                <pre className="whitespace-pre-wrap text-sm text-gray-800">{results.eda_summary}</pre>
                            </div>
                        )}

                        {results.ml_results && (
                            <div className="mb-6 p-4 bg-purple-50 rounded-lg">
                                <h3 className="font-bold text-lg mb-2 text-purple-900">🤖 ML Results</h3>
                                <p className="text-gray-800">
                                    <strong>Best Model:</strong> {results.ml_results.best_model}
                                </p>
                                <pre className="mt-2 text-sm text-gray-700">
                                    {JSON.stringify(results.ml_results.best_score, null, 2)}
                                </pre>
                            </div>
                        )}

                        {results.insights && (
                            <div className="mb-6 p-4 bg-green-50 rounded-lg">
                                <h3 className="font-bold text-lg mb-2 text-green-900">💡 AI Insights</h3>
                                <div className="whitespace-pre-wrap text-gray-800">{results.insights}</div>
                            </div>
                        )}

                        {results.code && (
                            <div className="mb-6">
                                <h3 className="font-bold text-lg mb-2">💻 Generated Code</h3>
                                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                                    <code>{results.code}</code>
                                </pre>
                            </div>
                        )}

                        {results.report_path && (
                            <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
                                <p className="text-gray-800">
                                    📄 <strong>Report generated:</strong> {results.report_path}
                                </p>
                                {results.notebook_path && (
                                    <p className="text-gray-800 mt-2">
                                        📓 <strong>Notebook:</strong> {results.notebook_path}
                                    </p>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}
