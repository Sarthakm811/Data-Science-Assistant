import React, { useState } from 'react'
import { Brain, Play, Trophy, AlertCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const mockModels = [
    { name: 'Random Forest', accuracy: 0.92, f1: 0.91, time: '2.3s' },
    { name: 'Logistic Regression', accuracy: 0.85, f1: 0.84, time: '0.5s' },
    { name: 'XGBoost', accuracy: 0.94, f1: 0.93, time: '3.1s' },
    { name: 'SVM', accuracy: 0.88, f1: 0.87, time: '1.8s' },
    { name: 'Neural Network', accuracy: 0.90, f1: 0.89, time: '5.2s' },
]

function AutoML({ dataset }) {
    const [ training, setTraining ] = useState(false)
    const [ results, setResults ] = useState(null)
    const [ config, setConfig ] = useState({
        target: '',
        taskType: 'auto'
    })

    const trainModels = () => {
        if (!dataset || !config.target) return

        setTraining(true)

        setTimeout(() => {
            const sortedModels = [ ...mockModels ].sort((a, b) => b.accuracy - a.accuracy)
            setResults({
                models: sortedModels,
                bestModel: sortedModels[ 0 ],
                taskType: config.taskType === 'auto' ? 'Classification' : config.taskType
            })
            setTraining(false)
        }, 3000)
    }

    if (!dataset) {
        return (
            <div className="card text-center py-12">
                <AlertCircle size={48} className="mx-auto text-gray-400 mb-4" />
                <h2 className="text-xl font-semibold text-gray-800 mb-2">No Dataset Loaded</h2>
                <p className="text-gray-500">Please upload a CSV file to train ML models</p>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="card">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">Auto ML</h1>
                        <p className="text-gray-500">Automatic Machine Learning Model Training</p>
                    </div>
                </div>

                {/* Configuration */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Target Column</label>
                        <select
                            value={config.target}
                            onChange={(e) => setConfig({ ...config, target: e.target.value })}
                            className="input-field"
                        >
                            <option value="">Select target...</option>
                            {dataset.headers.map((h, i) => (
                                <option key={i} value={h}>{h}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Task Type</label>
                        <select
                            value={config.taskType}
                            onChange={(e) => setConfig({ ...config, taskType: e.target.value })}
                            className="input-field"
                        >
                            <option value="auto">Auto-detect</option>
                            <option value="classification">Classification</option>
                            <option value="regression">Regression</option>
                        </select>
                    </div>

                    <div className="flex items-end">
                        <button
                            onClick={trainModels}
                            disabled={training || !config.target}
                            className="btn-primary w-full flex items-center justify-center gap-2"
                        >
                            <Play size={18} />
                            {training ? 'Training...' : 'Train Models'}
                        </button>
                    </div>
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600">
                        <strong>Dataset:</strong> {dataset.name} |
                        <strong> Rows:</strong> {dataset.rowCount} |
                        <strong> Columns:</strong> {dataset.colCount}
                    </p>
                </div>
            </div>

            {results && (
                <>
                    {/* Best Model */}
                    <div className="card bg-gradient-to-r from-purple-600 to-pink-600 text-white">
                        <div className="flex items-center gap-4">
                            <div className="bg-white/20 p-4 rounded-lg">
                                <Trophy size={32} />
                            </div>
                            <div>
                                <p className="text-purple-100">Best Performing Model</p>
                                <h2 className="text-2xl font-bold">{results.bestModel.name}</h2>
                                <p className="text-purple-100">
                                    Accuracy: {(results.bestModel.accuracy * 100).toFixed(1)}% |
                                    F1 Score: {(results.bestModel.f1 * 100).toFixed(1)}%
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Model Comparison Chart */}
                    <div className="card">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Model Comparison</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={results.models}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                <YAxis domain={[ 0, 1 ]} />
                                <Tooltip formatter={(value) => `${(value * 100).toFixed(1)}%`} />
                                <Bar dataKey="accuracy" fill="#8b5cf6" name="Accuracy" />
                                <Bar dataKey="f1" fill="#ec4899" name="F1 Score" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Model Details Table */}
                    <div className="card">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Model Details</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="bg-gray-50">
                                        <th className="px-4 py-3 text-left font-semibold">Model</th>
                                        <th className="px-4 py-3 text-left font-semibold">Accuracy</th>
                                        <th className="px-4 py-3 text-left font-semibold">F1 Score</th>
                                        <th className="px-4 py-3 text-left font-semibold">Training Time</th>
                                        <th className="px-4 py-3 text-left font-semibold">Rank</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.models.map((model, i) => (
                                        <tr key={i} className={`border-b ${i === 0 ? 'bg-purple-50' : ''}`}>
                                            <td className="px-4 py-3 font-medium flex items-center gap-2">
                                                {i === 0 && <Trophy size={16} className="text-yellow-500" />}
                                                {model.name}
                                            </td>
                                            <td className="px-4 py-3">{(model.accuracy * 100).toFixed(1)}%</td>
                                            <td className="px-4 py-3">{(model.f1 * 100).toFixed(1)}%</td>
                                            <td className="px-4 py-3">{model.time}</td>
                                            <td className="px-4 py-3">
                                                <span className={`px-2 py-1 rounded text-xs ${i === 0 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-700'
                                                    }`}>
                                                    #{i + 1}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </>
            )}
        </div>
    )
}

export default AutoML
