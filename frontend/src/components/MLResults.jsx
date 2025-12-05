import React, { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { CheckCircle, ChevronDown, Trophy, Zap, Clock } from 'lucide-react'

const CATEGORY_COLORS = {
    'Boosting': 'bg-purple-100 text-purple-700',
    'Ensemble': 'bg-blue-100 text-blue-700',
    'Linear': 'bg-green-100 text-green-700',
    'SVM': 'bg-orange-100 text-orange-700',
    'Neural Network': 'bg-pink-100 text-pink-700',
    'Deep Learning': 'bg-rose-100 text-rose-700',
    'Tree': 'bg-yellow-100 text-yellow-700',
    'Distance': 'bg-cyan-100 text-cyan-700',
    'Probabilistic': 'bg-indigo-100 text-indigo-700',
    'Discriminant': 'bg-teal-100 text-teal-700',
    'Gaussian Process': 'bg-violet-100 text-violet-700',
    'Robust': 'bg-amber-100 text-amber-700',
    'Polynomial': 'bg-lime-100 text-lime-700',
    'Kernel': 'bg-fuchsia-100 text-fuchsia-700',
    'GLM': 'bg-emerald-100 text-emerald-700'
}

function MLResults({ results }) {
    const [ expandedModel, setExpandedModel ] = useState(null)
    const [ viewMode, setViewMode ] = useState('all') // 'all' or category name

    if (!results || !results.models) {
        return (
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <p className="text-yellow-800">No model results available</p>
            </div>
        )
    }

    const isClassification = results.taskType === 'classification'
    const primaryMetric = isClassification ? 'accuracy' : 'r2'

    const bestModel = results.models.reduce((best, current) =>
        (current[ primaryMetric ] || 0) > (best[ primaryMetric ] || 0) ? current : best,
        results.models[ 0 ]
    )

    // Get unique categories
    const categories = [ ...new Set(results.models.map(m => m.category).filter(Boolean)) ]

    // Filter models by category
    const filteredModels = viewMode === 'all'
        ? results.models
        : results.models.filter(m => m.category === viewMode)

    return (
        <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-5 border border-blue-200">
                    <div className="flex items-center gap-2 mb-2">
                        <Zap size={18} className="text-blue-600" />
                        <p className="text-gray-600 text-sm font-medium">Models Trained</p>
                    </div>
                    <p className="text-3xl font-bold text-blue-900">{results.models.length}</p>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-5 border border-green-200">
                    <div className="flex items-center gap-2 mb-2">
                        <Trophy size={18} className="text-green-600" />
                        <p className="text-gray-600 text-sm font-medium">{isClassification ? 'Best Accuracy' : 'Best R² Score'}</p>
                    </div>
                    <p className="text-3xl font-bold text-green-900">
                        {isClassification
                            ? `${(bestModel.accuracy * 100).toFixed(1)}%`
                            : bestModel.r2?.toFixed(4)
                        }
                    </p>
                </div>
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-5 border border-purple-200">
                    <p className="text-gray-600 text-sm font-medium mb-2">Best Model</p>
                    <p className="text-xl font-bold text-purple-900">{bestModel.type}</p>
                    {bestModel.category && (
                        <span className={`text-xs px-2 py-0.5 rounded mt-1 inline-block ${CATEGORY_COLORS[ bestModel.category ] || 'bg-gray-100 text-gray-700'}`}>
                            {bestModel.category}
                        </span>
                    )}
                </div>
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-5 border border-orange-200">
                    <div className="flex items-center gap-2 mb-2">
                        <Clock size={18} className="text-orange-600" />
                        <p className="text-gray-600 text-sm font-medium">Training Time</p>
                    </div>
                    <p className="text-3xl font-bold text-orange-900">
                        {results.trainingTime ? `${results.trainingTime.toFixed(1)}s` : 'N/A'}
                    </p>
                </div>
            </div>

            {/* Category Filter */}
            {categories.length > 0 && (
                <div className="flex flex-wrap gap-2">
                    <button
                        onClick={() => setViewMode('all')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition ${viewMode === 'all'
                            ? 'bg-gray-900 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                    >
                        All Models ({results.models.length})
                    </button>
                    {categories.map(cat => (
                        <button
                            key={cat}
                            onClick={() => setViewMode(cat)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${viewMode === cat
                                ? 'bg-gray-900 text-white'
                                : `${CATEGORY_COLORS[ cat ] || 'bg-gray-100 text-gray-700'} hover:opacity-80`
                                }`}
                        >
                            {cat} ({results.models.filter(m => m.category === cat).length})
                        </button>
                    ))}
                </div>
            )}

            {/* Model Comparison Chart */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Model Comparison - Top 10 {isClassification ? 'by Accuracy' : 'by R² Score'}
                </h3>
                <ResponsiveContainer width="100%" height={350}>
                    <BarChart
                        data={filteredModels.slice(0, 10).map(m => ({
                            name: m.type.length > 15 ? m.type.substring(0, 15) + '...' : m.type,
                            ...(isClassification ? {
                                Accuracy: ((m.accuracy || 0) * 100).toFixed(1),
                                Precision: ((m.precision || 0) * 100).toFixed(1),
                                Recall: ((m.recall || 0) * 100).toFixed(1),
                                F1: ((m.f1 || 0) * 100).toFixed(1)
                            } : {
                                'R²': (m.r2 || 0).toFixed(3),
                                RMSE: (m.rmse || 0).toFixed(3),
                                MAE: (m.mae || 0).toFixed(3)
                            })
                        }))}
                        layout="vertical"
                        margin={{ left: 100 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" domain={isClassification ? [ 0, 100 ] : [ 0, 1 ]} />
                        <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 11 }} />
                        <Tooltip />
                        <Legend />
                        {isClassification ? (
                            <>
                                <Bar dataKey="Accuracy" fill="#4f46e5" />
                                <Bar dataKey="F1" fill="#ec4899" />
                            </>
                        ) : (
                            <>
                                <Bar dataKey="R²" fill="#4f46e5" />
                            </>
                        )}
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Detailed Model Results */}
            <div className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-900">
                    Model Details ({filteredModels.length} models)
                </h3>
                {filteredModels.map((model, idx) => (
                    <div key={idx} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                        <button
                            onClick={() => setExpandedModel(expandedModel === idx ? null : idx)}
                            className="w-full px-5 py-4 hover:bg-gray-50 transition flex items-center justify-between"
                        >
                            <div className="flex items-center gap-4 flex-1">
                                <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold text-white text-sm ${model === bestModel ? 'bg-gradient-to-br from-yellow-400 to-orange-500' : 'bg-gray-400'
                                    }`}>
                                    {model === bestModel ? <Trophy size={18} /> : idx + 1}
                                </div>
                                <div className="text-left">
                                    <div className="flex items-center gap-2">
                                        <p className="font-semibold text-gray-900">{model.type}</p>
                                        {model.category && (
                                            <span className={`text-xs px-2 py-0.5 rounded ${CATEGORY_COLORS[ model.category ] || 'bg-gray-100 text-gray-700'}`}>
                                                {model.category}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-sm text-gray-500">
                                        {isClassification
                                            ? `Accuracy: ${(model.accuracy * 100).toFixed(2)}% | F1: ${(model.f1 * 100).toFixed(2)}%`
                                            : `R²: ${model.r2?.toFixed(4)} | RMSE: ${model.rmse?.toFixed(4)} | MAE: ${model.mae?.toFixed(4)}`
                                        }
                                    </p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                {model === bestModel && <CheckCircle size={20} className="text-green-600" />}
                                <ChevronDown size={20} className={`text-gray-400 transition ${expandedModel === idx ? 'rotate-180' : ''}`} />
                            </div>
                        </button>

                        {expandedModel === idx && (
                            <div className="border-t border-gray-200 px-5 py-4 space-y-4 bg-gray-50">
                                <div>
                                    <p className="text-sm font-semibold text-gray-900 mb-3">Performance Metrics</p>
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                        {isClassification ? (
                                            <>
                                                <MetricCard label="Accuracy" value={`${(model.accuracy * 100).toFixed(2)}%`} />
                                                <MetricCard label="Precision" value={`${(model.precision * 100).toFixed(2)}%`} />
                                                <MetricCard label="Recall" value={`${(model.recall * 100).toFixed(2)}%`} />
                                                <MetricCard label="F1 Score" value={`${(model.f1 * 100).toFixed(2)}%`} />
                                            </>
                                        ) : (
                                            <>
                                                <MetricCard label="R² Score" value={model.r2?.toFixed(4)} />
                                                <MetricCard label="RMSE" value={model.rmse?.toFixed(4)} />
                                                <MetricCard label="MAE" value={model.mae?.toFixed(4)} />
                                                <MetricCard label="Category" value={model.category || 'N/A'} />
                                            </>
                                        )}
                                    </div>
                                </div>

                                {results.featureImportance && results.featureImportance.length > 0 && (
                                    <div>
                                        <p className="text-sm font-semibold text-gray-900 mb-3">Feature Importance</p>
                                        <div className="space-y-2">
                                            {results.featureImportance.slice(0, 5).map((feat, fidx) => (
                                                <div key={fidx} className="flex items-center justify-between">
                                                    <span className="text-sm text-gray-700 truncate max-w-[150px]">{feat.feature}</span>
                                                    <div className="flex items-center gap-2">
                                                        <div className="w-32 bg-gray-200 rounded-full h-2">
                                                            <div
                                                                className="bg-indigo-600 h-2 rounded-full"
                                                                style={{ width: `${feat.importance * 100}%` }}
                                                            />
                                                        </div>
                                                        <span className="text-sm font-medium text-gray-600 w-12 text-right">
                                                            {(feat.importance * 100).toFixed(1)}%
                                                        </span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    )
}

function MetricCard({ label, value }) {
    return (
        <div className="bg-white p-3 rounded-lg border border-gray-100">
            <p className="text-xs text-gray-500">{label}</p>
            <p className="text-lg font-bold text-gray-900">{value}</p>
        </div>
    )
}

export default MLResults
