'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
    const [ sessionId, setSessionId ] = useState<string>('');
    const [ query, setQuery ] = useState<string>('');
    const [ datasetId, setDatasetId ] = useState<string>('');
    const [ loading, setLoading ] = useState(false);
    const [ results, setResults ] = useState<any>(null);
    const [ history, setHistory ] = useState<any[]>([]);

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

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/api/v1/query`, {
                session_id: sessionId,
                query: query,
                dataset_id: datasetId || null
            });

            setResults(res.data);
            setHistory([ ...history, { query, response: res.data } ]);
            setQuery('');
        } catch (error) {
            console.error('Query failed:', error);
            alert('Query failed. Check console for details.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto py-6 px-4">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Data Science Research Assistant
                    </h1>
                    <p className="text-sm text-gray-500 mt-1">
                        Session: {sessionId.slice(0, 8)}...
                    </p>
                    <div className="mt-3">
                        <a
                            href="/enhanced"
                            className="inline-block px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold"
                        >
                            🚀 Try Enhanced Version (AutoEDA + AutoML)
                        </a>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto py-6 px-4">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Query Panel */}
                    <div className="lg:col-span-2">
                        <div className="bg-white shadow rounded-lg p-6">
                            <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>

                            <form onSubmit={handleSubmit}>
                                <div className="mb-4">
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Dataset ID (optional)
                                    </label>
                                    <input
                                        type="text"
                                        value={datasetId}
                                        onChange={(e) => setDatasetId(e.target.value)}
                                        placeholder="e.g., username/dataset-name"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                                    />
                                </div>

                                <div className="mb-4">
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Your Question
                                    </label>
                                    <textarea
                                        value={query}
                                        onChange={(e) => setQuery(e.target.value)}
                                        placeholder="e.g., Show me the top 5 features correlated with the target variable"
                                        rows={4}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                                    />
                                </div>

                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
                                >
                                    {loading ? 'Processing...' : 'Analyze'}
                                </button>
                            </form>

                            {/* Results */}
                            {results && (
                                <div className="mt-6 space-y-4">
                                    <div className="border-t pt-4">
                                        <h3 className="font-semibold text-lg mb-2">Analysis Plan</h3>
                                        <p className="text-gray-700 whitespace-pre-wrap">{results.plan}</p>
                                    </div>

                                    {results.code && (
                                        <div className="border-t pt-4">
                                            <h3 className="font-semibold text-lg mb-2">Generated Code</h3>
                                            <pre className="bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto text-sm">
                                                <code>{results.code}</code>
                                            </pre>
                                        </div>
                                    )}

                                    {results.explanation && (
                                        <div className="border-t pt-4">
                                            <h3 className="font-semibold text-lg mb-2">Explanation</h3>
                                            <p className="text-gray-700 whitespace-pre-wrap">{results.explanation}</p>
                                        </div>
                                    )}

                                    {results.results && (
                                        <div className="border-t pt-4">
                                            <h3 className="font-semibold text-lg mb-2">Results</h3>
                                            <pre className="bg-gray-50 p-4 rounded overflow-x-auto text-sm">
                                                {JSON.stringify(results.results, null, 2)}
                                            </pre>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* History Panel */}
                    <div className="lg:col-span-1">
                        <div className="bg-white shadow rounded-lg p-6">
                            <h2 className="text-xl font-semibold mb-4">History</h2>
                            <div className="space-y-3">
                                {history.length === 0 ? (
                                    <p className="text-gray-500 text-sm">No queries yet</p>
                                ) : (
                                    history.map((item, idx) => (
                                        <div key={idx} className="border-b pb-3">
                                            <p className="text-sm font-medium text-gray-900">
                                                {item.query}
                                            </p>
                                            <p className="text-xs text-gray-500 mt-1">
                                                Status: {item.response.status}
                                            </p>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
