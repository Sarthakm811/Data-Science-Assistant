import React, { useState } from 'react'
import { BarChart3, PieChart, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPie, Pie, Cell } from 'recharts'

const COLORS = [ '#8b5cf6', '#ec4899', '#3b82f6', '#10b981', '#f59e0b' ]

function AutoEDA({ dataset }) {
    const [ analyzing, setAnalyzing ] = useState(false)
    const [ results, setResults ] = useState(null)

    const runAnalysis = () => {
        if (!dataset) return

        setAnalyzing(true)

        // Simulate analysis
        setTimeout(() => {
            // Calculate basic stats
            const numericCols = dataset.headers.filter(h => {
                const val = dataset.rows[ 0 ]?.[ h ]
                return !isNaN(parseFloat(val))
            })

            const missingData = dataset.headers.map(h => ({
                name: h,
                missing: dataset.rows.filter(r => !r[ h ] || r[ h ] === '').length
            }))

            const dataTypes = dataset.headers.map(h => {
                const val = dataset.rows[ 0 ]?.[ h ]
                return {
                    name: h,
                    type: !isNaN(parseFloat(val)) ? 'Numeric' : 'Categorical'
                }
            })

            const typeCount = [
                { name: 'Numeric', value: dataTypes.filter(d => d.type === 'Numeric').length },
                { name: 'Categorical', value: dataTypes.filter(d => d.type === 'Categorical').length }
            ]

            setResults({
                summary: {
                    rows: dataset.rowCount,
                    columns: dataset.colCount,
                    numericCols: numericCols.length,
                    categoricalCols: dataset.colCount - numericCols.length,
                    missingTotal: missingData.reduce((a, b) => a + b.missing, 0)
                },
                missingData,
                typeCount,
                dataTypes
            })
            setAnalyzing(false)
        }, 2000)
    }

    if (!dataset) {
        return (
            <div className="card text-center py-12">
                <AlertCircle size={48} className="mx-auto text-gray-400 mb-4" />
                <h2 className="text-xl font-semibold text-gray-800 mb-2">No Dataset Loaded</h2>
                <p className="text-gray-500">Please upload a CSV file to run EDA analysis</p>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="card">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">Auto EDA</h1>
                        <p className="text-gray-500">Automated Exploratory Data Analysis</p>
                    </div>
                    <button
                        onClick={runAnalysis}
                        disabled={analyzing}
                        className="btn-primary flex items-center gap-2"
                    >
                        <BarChart3 size={18} />
                        {analyzing ? 'Analyzing...' : 'Run Analysis'}
                    </button>
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
                    {/* Summary Stats */}
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                        <div className="card text-center">
                            <p className="text-3xl font-bold text-purple-600">{results.summary.rows}</p>
                            <p className="text-gray-500 text-sm">Total Rows</p>
                        </div>
                        <div className="card text-center">
                            <p className="text-3xl font-bold text-blue-600">{results.summary.columns}</p>
                            <p className="text-gray-500 text-sm">Total Columns</p>
                        </div>
                        <div className="card text-center">
                            <p className="text-3xl font-bold text-green-600">{results.summary.numericCols}</p>
                            <p className="text-gray-500 text-sm">Numeric Cols</p>
                        </div>
                        <div className="card text-center">
                            <p className="text-3xl font-bold text-pink-600">{results.summary.categoricalCols}</p>
                            <p className="text-gray-500 text-sm">Categorical Cols</p>
                        </div>
                        <div className="card text-center">
                            <p className="text-3xl font-bold text-orange-600">{results.summary.missingTotal}</p>
                            <p className="text-gray-500 text-sm">Missing Values</p>
                        </div>
                    </div>

                    {/* Charts */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Missing Data Chart */}
                        <div className="card">
                            <h3 className="text-lg font-semibold text-gray-800 mb-4">Missing Data by Column</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={results.missingData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="missing" fill="#8b5cf6" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Data Types Chart */}
                        <div className="card">
                            <h3 className="text-lg font-semibold text-gray-800 mb-4">Data Types Distribution</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <RechartsPie>
                                    <Pie
                                        data={results.typeCount}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, value }) => `${name}: ${value}`}
                                        outerRadius={100}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {results.typeCount.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[ index % COLORS.length ]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </RechartsPie>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Column Details */}
                    <div className="card">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Column Details</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="bg-gray-50">
                                        <th className="px-4 py-3 text-left font-semibold">Column</th>
                                        <th className="px-4 py-3 text-left font-semibold">Type</th>
                                        <th className="px-4 py-3 text-left font-semibold">Missing</th>
                                        <th className="px-4 py-3 text-left font-semibold">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.dataTypes.map((col, i) => (
                                        <tr key={i} className="border-b">
                                            <td className="px-4 py-3 font-medium">{col.name}</td>
                                            <td className="px-4 py-3">
                                                <span className={`px-2 py-1 rounded text-xs ${col.type === 'Numeric' ? 'bg-blue-100 text-blue-700' : 'bg-pink-100 text-pink-700'
                                                    }`}>
                                                    {col.type}
                                                </span>
                                            </td>
                                            <td className="px-4 py-3">{results.missingData[ i ]?.missing || 0}</td>
                                            <td className="px-4 py-3">
                                                {results.missingData[ i ]?.missing === 0 ? (
                                                    <CheckCircle size={18} className="text-green-500" />
                                                ) : (
                                                    <AlertCircle size={18} className="text-orange-500" />
                                                )}
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

export default AutoEDA
