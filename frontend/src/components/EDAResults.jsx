import React, { useState } from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Download, AlertCircle, TrendingUp } from 'lucide-react'

function EDAResults({ results }) {
    const [ activeTab, setActiveTab ] = useState('overview')

    if (!results) {
        return (
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <p className="text-yellow-800">No analysis results available</p>
            </div>
        )
    }

    const tabs = [
        { id: 'overview', label: 'Overview', icon: '📊' },
        { id: 'statistical', label: 'Statistics', icon: '📈' },
        { id: 'correlation', label: 'Correlations', icon: '🔗' },
        { id: 'quality', label: 'Quality', icon: '✓' },
        { id: 'distribution', label: 'Distribution', icon: '📉' }
    ]

    return (
        <div className="space-y-6">
            {/* Tabs */}
            <div className="flex gap-2 border-b border-gray-200 overflow-x-auto">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-3 font-medium transition whitespace-nowrap ${activeTab === tab.id
                                ? 'border-b-2 border-indigo-600 text-indigo-600'
                                : 'text-gray-600 hover:text-gray-900'
                            }`}
                    >
                        {tab.icon} {tab.label}
                    </button>
                ))}
            </div>

            {/* Overview Tab */}
            {activeTab === 'overview' && (
                <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6 border border-blue-200">
                            <p className="text-gray-600 text-sm font-medium">Total Rows</p>
                            <p className="text-3xl font-bold text-blue-900">{results.rowCount?.toLocaleString() || 0}</p>
                        </div>
                        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6 border border-green-200">
                            <p className="text-gray-600 text-sm font-medium">Total Columns</p>
                            <p className="text-3xl font-bold text-green-900">{results.columnCount || 0}</p>
                        </div>
                        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-6 border border-purple-200">
                            <p className="text-gray-600 text-sm font-medium">Missing Values</p>
                            <p className="text-3xl font-bold text-purple-900">{results.missingCount || 0}</p>
                        </div>
                    </div>

                    {/* Column Types */}
                    {results.columnTypes && (
                        <div className="bg-white border border-gray-200 rounded-lg p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Column Types</h3>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {results.columnTypes.map((col, idx) => (
                                    <div key={idx} className="text-center p-4 bg-gray-50 rounded-lg">
                                        <p className="text-sm font-medium text-gray-700 truncate">{col.name}</p>
                                        <p className="text-xs text-gray-500 mt-1 capitalize">{col.type}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Statistical Tab */}
            {activeTab === 'statistical' && (
                <div className="space-y-4">
                    {results.statistics && (
                        <div className="bg-white border border-gray-200 rounded-lg p-6 overflow-x-auto">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Descriptive Statistics</h3>
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="border-b border-gray-200">
                                        <th className="text-left px-4 py-2 font-semibold text-gray-900">Column</th>
                                        <th className="text-right px-4 py-2 font-semibold text-gray-900">Mean</th>
                                        <th className="text-right px-4 py-2 font-semibold text-gray-900">Std Dev</th>
                                        <th className="text-right px-4 py-2 font-semibold text-gray-900">Min</th>
                                        <th className="text-right px-4 py-2 font-semibold text-gray-900">Max</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(results.statistics).map(([ col, stats ]) => (
                                        <tr key={col} className="border-b border-gray-100 hover:bg-gray-50">
                                            <td className="px-4 py-2 font-medium text-gray-900">{col}</td>
                                            <td className="text-right px-4 py-2 text-gray-700">{typeof stats.mean === 'number' ? stats.mean.toFixed(2) : 'N/A'}</td>
                                            <td className="text-right px-4 py-2 text-gray-700">{typeof stats.std === 'number' ? stats.std.toFixed(2) : 'N/A'}</td>
                                            <td className="text-right px-4 py-2 text-gray-700">{typeof stats.min === 'number' ? stats.min.toFixed(2) : 'N/A'}</td>
                                            <td className="text-right px-4 py-2 text-gray-700">{typeof stats.max === 'number' ? stats.max.toFixed(2) : 'N/A'}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}

            {/* Correlation Tab */}
            {activeTab === 'correlation' && (
                <div className="space-y-4">
                    {results.correlation && (
                        <div className="bg-white border border-gray-200 rounded-lg p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Correlations</h3>
                            <div className="space-y-2">
                                {results.correlation.slice(0, 10).map((corr, idx) => (
                                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                        <span className="text-sm font-medium text-gray-900">{corr.variable1} ↔ {corr.variable2}</span>
                                        <div className="flex items-center gap-2">
                                            <div className="w-32 bg-gray-200 rounded-full h-2">
                                                <div
                                                    className="bg-indigo-600 h-2 rounded-full"
                                                    style={{ width: `${Math.abs(corr.value) * 100}%` }}
                                                />
                                            </div>
                                            <span className="text-sm font-semibold text-gray-900 min-w-fit">{corr.value.toFixed(3)}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Quality Tab */}
            {activeTab === 'quality' && (
                <div className="space-y-4">
                    {results.dataQuality && (
                        <div className="bg-white border border-gray-200 rounded-lg p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Quality Report</h3>
                            <div className="space-y-3">
                                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <span className="text-sm font-medium text-gray-900">Completeness</span>
                                    <span className="text-sm font-semibold text-green-600">{(results.dataQuality.completeness * 100).toFixed(1)}%</span>
                                </div>
                                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <span className="text-sm font-medium text-gray-900">Missing Values</span>
                                    <span className="text-sm font-semibold text-gray-600">{results.dataQuality.missingCount}</span>
                                </div>
                                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <span className="text-sm font-medium text-gray-900">Duplicates</span>
                                    <span className="text-sm font-semibold text-gray-600">{results.dataQuality.duplicateCount}</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Distribution Tab */}
            {activeTab === 'distribution' && (
                <div className="space-y-4">
                    {results.distributions && results.distributions.length > 0 && (
                        <div className="bg-white border border-gray-200 rounded-lg p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Value Distributions</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={results.distributions.slice(0, 5)}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="count" fill="#4f46e5" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default EDAResults
