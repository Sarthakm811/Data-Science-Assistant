import React, { useState } from 'react'
import { BarChart3, PieChart, TrendingUp, AlertCircle, CheckCircle, Activity, Zap, Target } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPie, Pie, Cell, LineChart, Line, ScatterChart, Scatter, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts'

const COLORS = [ '#8b5cf6', '#ec4899', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16' ]

function AutoEDA({ dataset }) {
    const [ analyzing, setAnalyzing ] = useState(false)
    const [ results, setResults ] = useState(null)
    const [ activeTab, setActiveTab ] = useState('overview')

    const runAnalysis = () => {
        if (!dataset) return
        setAnalyzing(true)

        setTimeout(() => {
            const numericCols = dataset.headers.filter(h => {
                const val = dataset.rows[ 0 ]?.[ h ]
                return !isNaN(parseFloat(val))
            })

            const categoricalCols = dataset.headers.filter(h => !numericCols.includes(h))

            // Missing data analysis
            const missingData = dataset.headers.map(h => ({
                name: h,
                missing: dataset.rows.filter(r => !r[ h ] || r[ h ] === '').length,
                percentage: ((dataset.rows.filter(r => !r[ h ] || r[ h ] === '').length / dataset.rowCount) * 100).toFixed(1)
            }))

            // Data types
            const dataTypes = dataset.headers.map(h => ({
                name: h,
                type: numericCols.includes(h) ? 'Numeric' : 'Categorical'
            }))

            // Statistics for numeric columns
            const statistics = numericCols.map(col => {
                const values = dataset.rows.map(r => parseFloat(r[ col ])).filter(v => !isNaN(v))
                const sorted = [ ...values ].sort((a, b) => a - b)
                const mean = values.reduce((a, b) => a + b, 0) / values.length
                const min = Math.min(...values)
                const max = Math.max(...values)
                const median = sorted[ Math.floor(sorted.length / 2) ]
                const std = Math.sqrt(values.reduce((sq, n) => sq + Math.pow(n - mean, 2), 0) / values.length)
                const q1 = sorted[ Math.floor(sorted.length * 0.25) ]
                const q3 = sorted[ Math.floor(sorted.length * 0.75) ]
                const iqr = q3 - q1
                const outliers = values.filter(v => v < q1 - 1.5 * iqr || v > q3 + 1.5 * iqr).length

                return { name: col, mean: mean.toFixed(2), median: median.toFixed(2), std: std.toFixed(2), min: min.toFixed(2), max: max.toFixed(2), outliers, q1: q1.toFixed(2), q3: q3.toFixed(2) }
            })

            // Correlation matrix (simplified)
            const correlations = []
            for (let i = 0; i < Math.min(numericCols.length, 5); i++) {
                for (let j = i + 1; j < Math.min(numericCols.length, 5); j++) {
                    const col1 = numericCols[ i ]
                    const col2 = numericCols[ j ]
                    const vals1 = dataset.rows.map(r => parseFloat(r[ col1 ])).filter(v => !isNaN(v))
                    const vals2 = dataset.rows.map(r => parseFloat(r[ col2 ])).filter(v => !isNaN(v))
                    const mean1 = vals1.reduce((a, b) => a + b, 0) / vals1.length
                    const mean2 = vals2.reduce((a, b) => a + b, 0) / vals2.length
                    let num = 0, den1 = 0, den2 = 0
                    for (let k = 0; k < Math.min(vals1.length, vals2.length); k++) {
                        num += (vals1[ k ] - mean1) * (vals2[ k ] - mean2)
                        den1 += Math.pow(vals1[ k ] - mean1, 2)
                        den2 += Math.pow(vals2[ k ] - mean2, 2)
                    }
                    const corr = num / Math.sqrt(den1 * den2)
                    if (!isNaN(corr)) correlations.push({ pair: `${col1} vs ${col2}`, value: corr.toFixed(3), strength: Math.abs(corr) > 0.7 ? 'Strong' : Math.abs(corr) > 0.4 ? 'Moderate' : 'Weak' })
                }
            }

            // Categorical analysis
            const categoricalAnalysis = categoricalCols.slice(0, 5).map(col => {
                const valueCounts = {}
                dataset.rows.forEach(r => {
                    const val = r[ col ] || 'Missing'
                    valueCounts[ val ] = (valueCounts[ val ] || 0) + 1
                })
                const sorted = Object.entries(valueCounts).sort((a, b) => b[ 1 ] - a[ 1 ]).slice(0, 10)
                return { name: col, uniqueValues: Object.keys(valueCounts).length, topValues: sorted.map(([ name, value ]) => ({ name, value })) }
            })

            // Data Quality Score
            const missingScore = 100 - (missingData.reduce((a, b) => a + parseFloat(b.percentage), 0) / dataset.headers.length)
            const duplicateRows = new Set(dataset.rows.map(r => JSON.stringify(r))).size
            const duplicateScore = (duplicateRows / dataset.rowCount) * 100
            const outlierScore = 100 - (statistics.reduce((a, b) => a + b.outliers, 0) / (dataset.rowCount * numericCols.length) * 100)
            const qualityScore = ((missingScore + duplicateScore + outlierScore) / 3).toFixed(0)

            // Distribution data for charts
            const distributionData = numericCols.slice(0, 4).map(col => {
                const values = dataset.rows.map(r => parseFloat(r[ col ])).filter(v => !isNaN(v))
                const min = Math.min(...values)
                const max = Math.max(...values)
                const binSize = (max - min) / 10
                const bins = Array(10).fill(0)
                values.forEach(v => {
                    const binIndex = Math.min(Math.floor((v - min) / binSize), 9)
                    bins[ binIndex ]++
                })
                return { name: col, data: bins.map((count, i) => ({ bin: (min + i * binSize).toFixed(1), count })) }
            })

            // ML Readiness
            const mlReadiness = {
                score: Math.min(100, Math.max(0, qualityScore - (missingData.filter(m => parseFloat(m.percentage) > 20).length * 10))),
                issues: [],
                recommendations: []
            }
            if (missingData.some(m => parseFloat(m.percentage) > 20)) mlReadiness.issues.push('High missing data in some columns')
            if (statistics.some(s => s.outliers > dataset.rowCount * 0.1)) mlReadiness.issues.push('Significant outliers detected')
            if (numericCols.length < 2) mlReadiness.issues.push('Limited numeric features')
            mlReadiness.recommendations = [ 'Handle missing values', 'Consider outlier treatment', 'Feature scaling recommended', 'Check for multicollinearity' ]

            setResults({
                summary: { rows: dataset.rowCount, columns: dataset.colCount, numericCols: numericCols.length, categoricalCols: categoricalCols.length, missingTotal: missingData.reduce((a, b) => a + b.missing, 0), duplicateRows: dataset.rowCount - duplicateRows },
                missingData,
                dataTypes,
                statistics,
                correlations,
                categoricalAnalysis,
                qualityScore,
                distributionData,
                mlReadiness,
                typeCount: [
                    { name: 'Numeric', value: numericCols.length },
                    { name: 'Categorical', value: categoricalCols.length }
                ]
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

    const tabs = [
        { id: 'overview', label: 'Overview', icon: BarChart3 },
        { id: 'quality', label: 'Data Quality', icon: CheckCircle },
        { id: 'statistics', label: 'Statistics', icon: Activity },
        { id: 'correlations', label: 'Correlations', icon: TrendingUp },
        { id: 'distributions', label: 'Distributions', icon: PieChart },
        { id: 'mlready', label: 'ML Readiness', icon: Zap }
    ]

    return (
        <div className="space-y-6">
            <div className="card">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">Auto EDA</h1>
                        <p className="text-gray-500">Comprehensive Exploratory Data Analysis</p>
                    </div>
                    <button onClick={runAnalysis} disabled={analyzing} className="btn-primary flex items-center gap-2">
                        <BarChart3 size={18} />
                        {analyzing ? 'Analyzing...' : 'Run Full Analysis'}
                    </button>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600">
                        <strong>Dataset:</strong> {dataset.name} | <strong>Rows:</strong> {dataset.rowCount} | <strong>Columns:</strong> {dataset.colCount}
                    </p>
                </div>
            </div>

            {results && (
                <>
                    {/* Tabs */}
                    <div className="flex gap-2 overflow-x-auto pb-2">
                        {tabs.map(tab => {
                            const Icon = tab.icon
                            return (
                                <button key={tab.id} onClick={() => setActiveTab(tab.id)} className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-colors ${activeTab === tab.id ? 'bg-purple-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'}`}>
                                    <Icon size={16} />
                                    {tab.label}
                                </button>
                            )
                        })}
                    </div>

                    {/* Overview Tab */}
                    {activeTab === 'overview' && (
                        <div className="space-y-6">
                            <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
                                <div className="card text-center"><p className="text-3xl font-bold text-purple-600">{results.summary.rows}</p><p className="text-gray-500 text-sm">Rows</p></div>
                                <div className="card text-center"><p className="text-3xl font-bold text-blue-600">{results.summary.columns}</p><p className="text-gray-500 text-sm">Columns</p></div>
                                <div className="card text-center"><p className="text-3xl font-bold text-green-600">{results.summary.numericCols}</p><p className="text-gray-500 text-sm">Numeric</p></div>
                                <div className="card text-center"><p className="text-3xl font-bold text-pink-600">{results.summary.categoricalCols}</p><p className="text-gray-500 text-sm">Categorical</p></div>
                                <div className="card text-center"><p className="text-3xl font-bold text-orange-600">{results.summary.missingTotal}</p><p className="text-gray-500 text-sm">Missing</p></div>
                                <div className="card text-center"><p className="text-3xl font-bold text-red-600">{results.summary.duplicateRows}</p><p className="text-gray-500 text-sm">Duplicates</p></div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="card">
                                    <h3 className="text-lg font-semibold mb-4">Data Types Distribution</h3>
                                    <ResponsiveContainer width="100%" height={250}>
                                        <RechartsPie><Pie data={results.typeCount} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="value" label={({ name, value }) => `${name}: ${value}`}>{results.typeCount.map((_, i) => <Cell key={i} fill={COLORS[ i ]} />)}</Pie><Tooltip /></RechartsPie>
                                    </ResponsiveContainer>
                                </div>
                                <div className="card">
                                    <h3 className="text-lg font-semibold mb-4">Missing Data by Column</h3>
                                    <ResponsiveContainer width="100%" height={250}>
                                        <BarChart data={results.missingData.slice(0, 8)}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{ fontSize: 10 }} /><YAxis /><Tooltip /><Bar dataKey="missing" fill="#8b5cf6" /></BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Data Quality Tab */}
                    {activeTab === 'quality' && (
                        <div className="space-y-6">
                            <div className="card bg-gradient-to-r from-purple-600 to-pink-600 text-white">
                                <div className="flex items-center gap-4">
                                    <div className="bg-white/20 p-4 rounded-lg"><CheckCircle size={32} /></div>
                                    <div>
                                        <p className="text-purple-100">Data Quality Score</p>
                                        <h2 className="text-4xl font-bold">{results.qualityScore}/100</h2>
                                        <p className="text-purple-100">{results.qualityScore >= 80 ? 'Excellent' : results.qualityScore >= 60 ? 'Good' : results.qualityScore >= 40 ? 'Fair' : 'Needs Improvement'}</p>
                                    </div>
                                </div>
                            </div>
                            <div className="card">
                                <h3 className="text-lg font-semibold mb-4">Missing Data Analysis</h3>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-sm">
                                        <thead><tr className="bg-gray-50"><th className="px-4 py-3 text-left">Column</th><th className="px-4 py-3 text-left">Missing Count</th><th className="px-4 py-3 text-left">Percentage</th><th className="px-4 py-3 text-left">Status</th></tr></thead>
                                        <tbody>
                                            {results.missingData.map((col, i) => (
                                                <tr key={i} className="border-b">
                                                    <td className="px-4 py-3 font-medium">{col.name}</td>
                                                    <td className="px-4 py-3">{col.missing}</td>
                                                    <td className="px-4 py-3">{col.percentage}%</td>
                                                    <td className="px-4 py-3">{parseFloat(col.percentage) === 0 ? <CheckCircle size={18} className="text-green-500" /> : parseFloat(col.percentage) < 5 ? <AlertCircle size={18} className="text-yellow-500" /> : <AlertCircle size={18} className="text-red-500" />}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Statistics Tab */}
                    {activeTab === 'statistics' && (
                        <div className="space-y-6">
                            <div className="card">
                                <h3 className="text-lg font-semibold mb-4">Descriptive Statistics</h3>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-sm">
                                        <thead><tr className="bg-gray-50"><th className="px-4 py-3 text-left">Column</th><th className="px-4 py-3 text-left">Mean</th><th className="px-4 py-3 text-left">Median</th><th className="px-4 py-3 text-left">Std Dev</th><th className="px-4 py-3 text-left">Min</th><th className="px-4 py-3 text-left">Max</th><th className="px-4 py-3 text-left">Q1</th><th className="px-4 py-3 text-left">Q3</th><th className="px-4 py-3 text-left">Outliers</th></tr></thead>
                                        <tbody>
                                            {results.statistics.map((stat, i) => (
                                                <tr key={i} className="border-b">
                                                    <td className="px-4 py-3 font-medium">{stat.name}</td>
                                                    <td className="px-4 py-3">{stat.mean}</td>
                                                    <td className="px-4 py-3">{stat.median}</td>
                                                    <td className="px-4 py-3">{stat.std}</td>
                                                    <td className="px-4 py-3">{stat.min}</td>
                                                    <td className="px-4 py-3">{stat.max}</td>
                                                    <td className="px-4 py-3">{stat.q1}</td>
                                                    <td className="px-4 py-3">{stat.q3}</td>
                                                    <td className="px-4 py-3"><span className={`px-2 py-1 rounded text-xs ${stat.outliers > 0 ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'}`}>{stat.outliers}</span></td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            {results.categoricalAnalysis.length > 0 && (
                                <div className="card">
                                    <h3 className="text-lg font-semibold mb-4">Categorical Variables</h3>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {results.categoricalAnalysis.map((cat, i) => (
                                            <div key={i} className="bg-gray-50 rounded-lg p-4">
                                                <h4 className="font-medium mb-2">{cat.name} <span className="text-gray-500 text-sm">({cat.uniqueValues} unique)</span></h4>
                                                <ResponsiveContainer width="100%" height={150}>
                                                    <BarChart data={cat.topValues.slice(0, 5)} layout="vertical"><XAxis type="number" /><YAxis dataKey="name" type="category" width={80} tick={{ fontSize: 10 }} /><Tooltip /><Bar dataKey="value" fill={COLORS[ i % COLORS.length ]} /></BarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Correlations Tab */}
                    {activeTab === 'correlations' && (
                        <div className="space-y-6">
                            <div className="card">
                                <h3 className="text-lg font-semibold mb-4">Feature Correlations</h3>
                                {results.correlations.length > 0 ? (
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-sm">
                                            <thead><tr className="bg-gray-50"><th className="px-4 py-3 text-left">Feature Pair</th><th className="px-4 py-3 text-left">Correlation</th><th className="px-4 py-3 text-left">Strength</th></tr></thead>
                                            <tbody>
                                                {results.correlations.map((corr, i) => (
                                                    <tr key={i} className="border-b">
                                                        <td className="px-4 py-3 font-medium">{corr.pair}</td>
                                                        <td className="px-4 py-3">{corr.value}</td>
                                                        <td className="px-4 py-3"><span className={`px-2 py-1 rounded text-xs ${corr.strength === 'Strong' ? 'bg-red-100 text-red-700' : corr.strength === 'Moderate' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>{corr.strength}</span></td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                ) : <p className="text-gray-500">Not enough numeric columns for correlation analysis</p>}
                            </div>
                            <div className="card">
                                <h3 className="text-lg font-semibold mb-4">Correlation Insights</h3>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div className="bg-red-50 p-4 rounded-lg"><p className="text-red-700 font-semibold">{results.correlations.filter(c => c.strength === 'Strong').length}</p><p className="text-red-600 text-sm">Strong Correlations</p></div>
                                    <div className="bg-yellow-50 p-4 rounded-lg"><p className="text-yellow-700 font-semibold">{results.correlations.filter(c => c.strength === 'Moderate').length}</p><p className="text-yellow-600 text-sm">Moderate Correlations</p></div>
                                    <div className="bg-green-50 p-4 rounded-lg"><p className="text-green-700 font-semibold">{results.correlations.filter(c => c.strength === 'Weak').length}</p><p className="text-green-600 text-sm">Weak Correlations</p></div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Distributions Tab */}
                    {activeTab === 'distributions' && (
                        <div className="space-y-6">
                            <div className="card">
                                <h3 className="text-lg font-semibold mb-4">Numeric Distributions</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {results.distributionData.map((dist, i) => (
                                        <div key={i} className="bg-gray-50 rounded-lg p-4">
                                            <h4 className="font-medium mb-2">{dist.name}</h4>
                                            <ResponsiveContainer width="100%" height={200}>
                                                <BarChart data={dist.data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="bin" tick={{ fontSize: 10 }} /><YAxis /><Tooltip /><Bar dataKey="count" fill={COLORS[ i % COLORS.length ]} /></BarChart>
                                            </ResponsiveContainer>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* ML Readiness Tab */}
                    {activeTab === 'mlready' && (
                        <div className="space-y-6">
                            <div className="card bg-gradient-to-r from-green-600 to-teal-600 text-white">
                                <div className="flex items-center gap-4">
                                    <div className="bg-white/20 p-4 rounded-lg"><Zap size={32} /></div>
                                    <div>
                                        <p className="text-green-100">ML Readiness Score</p>
                                        <h2 className="text-4xl font-bold">{results.mlReadiness.score}/100</h2>
                                        <p className="text-green-100">{results.mlReadiness.score >= 80 ? 'Ready for ML' : results.mlReadiness.score >= 60 ? 'Minor preprocessing needed' : 'Significant preprocessing required'}</p>
                                    </div>
                                </div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="card">
                                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><AlertCircle className="text-orange-500" /> Issues Detected</h3>
                                    {results.mlReadiness.issues.length > 0 ? (
                                        <ul className="space-y-2">
                                            {results.mlReadiness.issues.map((issue, i) => (
                                                <li key={i} className="flex items-center gap-2 text-gray-700"><span className="w-2 h-2 bg-orange-500 rounded-full"></span>{issue}</li>
                                            ))}
                                        </ul>
                                    ) : <p className="text-green-600">No major issues detected!</p>}
                                </div>
                                <div className="card">
                                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Target className="text-blue-500" /> Recommendations</h3>
                                    <ul className="space-y-2">
                                        {results.mlReadiness.recommendations.map((rec, i) => (
                                            <li key={i} className="flex items-center gap-2 text-gray-700"><CheckCircle size={16} className="text-blue-500" />{rec}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                            <div className="card">
                                <h3 className="text-lg font-semibold mb-4">Feature Summary for ML</h3>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <div className="bg-purple-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-purple-600">{results.summary.numericCols}</p><p className="text-purple-700 text-sm">Numeric Features</p></div>
                                    <div className="bg-pink-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-pink-600">{results.summary.categoricalCols}</p><p className="text-pink-700 text-sm">Categorical Features</p></div>
                                    <div className="bg-blue-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-blue-600">{results.statistics.reduce((a, b) => a + b.outliers, 0)}</p><p className="text-blue-700 text-sm">Total Outliers</p></div>
                                    <div className="bg-green-50 p-4 rounded-lg text-center"><p className="text-2xl font-bold text-green-600">{results.missingData.filter(m => parseFloat(m.percentage) === 0).length}</p><p className="text-green-700 text-sm">Complete Columns</p></div>
                                </div>
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    )
}

export default AutoEDA
