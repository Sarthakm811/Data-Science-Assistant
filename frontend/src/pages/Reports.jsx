import React, { useState } from 'react'
import { FileText, Download, Loader, CheckCircle, AlertCircle, BarChart3, Brain, AlertTriangle, TrendingUp, Eye, Settings, RefreshCw } from 'lucide-react'
import { useAnalysis } from '../context/AnalysisContext'

function Reports({ dataset }) {
    const [ generating, setGenerating ] = useState(false)
    const [ reportData, setReportData ] = useState(null)
    const [ config, setConfig ] = useState({
        includeEDA: true,
        includeML: true,
        includeAnomaly: true,
        includeTimeSeries: true,
        includeDataPreview: true
    })

    const { edaResults, mlResults, anomalyResults, timeSeriesResults, hasResults } = useAnalysis()

    const generateReport = async () => {
        if (!dataset) return
        setGenerating(true)

        setTimeout(() => {
            const report = buildReport()
            setReportData(report)
            setGenerating(false)
        }, 1500)
    }

    const buildReport = () => {
        const now = new Date().toLocaleString()
        let html = `<!DOCTYPE html><html><head>
<title>Data Analysis Report - ${dataset.name}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;line-height:1.6;color:#333;max-width:1200px;margin:0 auto;padding:40px;background:#f5f5f5}
.report{background:white;padding:40px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}
h1{color:#7c3aed;font-size:2.2em;margin-bottom:10px;border-bottom:3px solid #7c3aed;padding-bottom:15px}
h2{color:#1f2937;font-size:1.6em;margin:30px 0 15px;padding:10px 0;border-bottom:2px solid #e5e7eb}
h3{color:#4b5563;font-size:1.2em;margin:20px 0 10px}
.meta{color:#6b7280;margin-bottom:30px}
.section{margin:30px 0;padding:25px;background:#f9fafb;border-radius:8px;border-left:4px solid #7c3aed}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px;margin:20px 0}
.card{background:white;padding:20px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.05);text-align:center}
.card-value{font-size:1.8em;font-weight:bold;color:#7c3aed}
.card-label{color:#6b7280;font-size:0.85em;margin-top:5px}
table{width:100%;border-collapse:collapse;margin:15px 0;background:white;border-radius:8px;overflow:hidden;font-size:0.9em}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid #e5e7eb}
th{background:#7c3aed;color:white;font-weight:600}
tr:hover{background:#f3f4f6}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.8em;font-weight:500}
.badge-success{background:#d1fae5;color:#065f46}
.badge-warning{background:#fef3c7;color:#92400e}
.badge-danger{background:#fee2e2;color:#991b1b}
.badge-info{background:#dbeafe;color:#1e40af}
.insight{padding:15px;margin:10px 0;border-radius:8px}
.insight-success{background:#ecfdf5;border-left:4px solid #10b981}
.insight-warning{background:#fffbeb;border-left:4px solid #f59e0b}
.insight-info{background:#eff6ff;border-left:4px solid #3b82f6}
.footer{margin-top:40px;padding-top:20px;border-top:2px solid #e5e7eb;color:#6b7280;text-align:center}
.chart-placeholder{background:#f3f4f6;border:2px dashed #d1d5db;border-radius:8px;padding:40px;text-align:center;color:#6b7280}
@media print{body{background:white}.report{box-shadow:none}}
</style></head><body><div class="report">
<h1>📊 Comprehensive Data Analysis Report</h1>
<p class="meta">Generated: ${now} | Dataset: <strong>${dataset.name}</strong></p>`

        // Dataset Overview
        html += `<h2>📁 Dataset Overview</h2>
<div class="grid">
<div class="card"><div class="card-value">${dataset.rowCount.toLocaleString()}</div><div class="card-label">Total Rows</div></div>
<div class="card"><div class="card-value">${dataset.colCount}</div><div class="card-label">Total Columns</div></div>
<div class="card"><div class="card-value">${edaResults?.summary?.numericCols || '-'}</div><div class="card-label">Numeric</div></div>
<div class="card"><div class="card-value">${edaResults?.summary?.categoricalCols || '-'}</div><div class="card-label">Categorical</div></div>
</div>`

        if (config.includeDataPreview) {
            html += `<h3>Data Preview</h3><table><thead><tr>${dataset.headers.slice(0, 8).map(h => `<th>${h}</th>`).join('')}</tr></thead>
<tbody>${dataset.rows.slice(0, 5).map(row => `<tr>${dataset.headers.slice(0, 8).map(h => `<td>${row[ h ] || '-'}</td>`).join('')}</tr>`).join('')}</tbody></table>`
        }

        // EDA Section
        if (config.includeEDA && edaResults) {
            html += `<h2>🔍 Exploratory Data Analysis</h2><div class="section">
<div class="grid">
<div class="card"><div class="card-value" style="color:${edaResults.qualityScore >= 80 ? '#10b981' : edaResults.qualityScore >= 60 ? '#f59e0b' : '#ef4444'}">${edaResults.qualityScore}/100</div><div class="card-label">Quality Score</div></div>
<div class="card"><div class="card-value">${edaResults.summary?.missingTotal || 0}</div><div class="card-label">Missing Values</div></div>
<div class="card"><div class="card-value">${edaResults.summary?.outlierTotal || 0}</div><div class="card-label">Outliers</div></div>
<div class="card"><div class="card-value">${edaResults.summary?.duplicateRows || 0}</div><div class="card-label">Duplicates</div></div>
</div>
<h3>Statistical Summary</h3><table><thead><tr><th>Column</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th><th>Outliers</th><th>Skewness</th></tr></thead>
<tbody>${(edaResults.statistics || []).map(s => `<tr><td><strong>${s.name}</strong></td><td>${s.mean?.toFixed?.(2) || s.mean}</td><td>${s.std?.toFixed?.(2) || s.std}</td><td>${s.min?.toFixed?.(2) || s.min}</td><td>${s.max?.toFixed?.(2) || s.max}</td><td><span class="badge ${s.outlierCount > 0 ? 'badge-warning' : 'badge-success'}">${s.outlierCount || 0}</span></td><td>${s.skewness || '-'}</td></tr>`).join('')}</tbody></table>
<h3>Missing Data Analysis</h3><table><thead><tr><th>Column</th><th>Missing</th><th>%</th><th>Status</th></tr></thead>
<tbody>${(edaResults.missingData || []).map(m => `<tr><td>${m.name}</td><td>${m.missing}</td><td>${m.percentage?.toFixed?.(1) || m.percentage}%</td><td><span class="badge ${parseFloat(m.percentage) === 0 ? 'badge-success' : parseFloat(m.percentage) < 10 ? 'badge-warning' : 'badge-danger'}">${parseFloat(m.percentage) === 0 ? 'Complete' : parseFloat(m.percentage) < 10 ? 'Low' : 'High'}</span></td></tr>`).join('')}</tbody></table>`

            // Correlations
            if (edaResults.correlations?.length > 0) {
                const topCorr = edaResults.correlations.sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation)).slice(0, 10)
                html += `<h3>Top Correlations</h3><table><thead><tr><th>Feature 1</th><th>Feature 2</th><th>Correlation</th><th>Strength</th></tr></thead>
<tbody>${topCorr.map(c => `<tr><td>${c.feature1}</td><td>${c.feature2}</td><td style="color:${c.correlation > 0 ? '#10b981' : '#ef4444'}">${c.correlation?.toFixed?.(3) || c.correlation}</td><td><span class="badge badge-info">${c.strength}</span></td></tr>`).join('')}</tbody></table>`
            }

            // Insights
            if (edaResults.insights?.length > 0) {
                html += `<h3>AI-Generated Insights</h3>`
                edaResults.insights.forEach(i => {
                    html += `<div class="insight insight-${i.type === 'warning' ? 'warning' : i.type === 'success' ? 'success' : 'info'}"><strong>${i.title}:</strong> ${i.desc} <em>(${i.action})</em></div>`
                })
            }
            html += `</div>`
        }

        // ML Section
        if (config.includeML && mlResults) {
            const bestModel = mlResults.models?.[ 0 ]
            const isClassification = mlResults.taskType === 'classification'
            html += `<h2>🤖 Machine Learning Results</h2><div class="section">
<div class="insight insight-success"><strong>🏆 Best Model:</strong> ${bestModel?.type || bestModel?.name || 'N/A'} with ${isClassification ? (bestModel?.accuracy * 100)?.toFixed(1) + '% accuracy' : bestModel?.r2?.toFixed(4) + ' R² score'}</div>
<div class="grid">
<div class="card"><div class="card-value">${mlResults.models?.length || 0}</div><div class="card-label">Models Trained</div></div>
<div class="card"><div class="card-value">${mlResults.taskType || 'auto'}</div><div class="card-label">Task Type</div></div>
<div class="card"><div class="card-value">${mlResults.trainingTime?.toFixed(1) || '-'}s</div><div class="card-label">Training Time</div></div>
</div>
<h3>Model Comparison (Top 10)</h3><table><thead><tr><th>#</th><th>Model</th><th>Category</th>${isClassification ? '<th>Accuracy</th><th>F1</th>' : '<th>R²</th><th>RMSE</th>'}<th>Status</th></tr></thead>
<tbody>${(mlResults.models || []).slice(0, 10).map((m, i) => `<tr><td>${i + 1}</td><td><strong>${m.type || m.name}</strong></td><td><span class="badge badge-info">${m.category || '-'}</span></td>${isClassification ? `<td>${(m.accuracy * 100)?.toFixed(1)}%</td><td>${(m.f1 * 100)?.toFixed(1)}%</td>` : `<td>${m.r2?.toFixed(4)}</td><td>${m.rmse?.toFixed(4)}</td>`}<td>${i === 0 ? '<span class="badge badge-success">🥇 Best</span>' : '<span class="badge">Trained</span>'}</td></tr>`).join('')}</tbody></table>`

            // Feature Importance
            if (mlResults.featureImportance?.length > 0) {
                html += `<h3>Feature Importance (Top 10)</h3><table><thead><tr><th>Feature</th><th>Importance</th><th>Visual</th></tr></thead>
<tbody>${mlResults.featureImportance.slice(0, 10).map(f => `<tr><td>${f.feature}</td><td>${(f.importance * 100)?.toFixed(1)}%</td><td><div style="background:#e5e7eb;border-radius:4px;height:20px;width:200px"><div style="background:#7c3aed;height:100%;width:${f.importance * 100}%;border-radius:4px"></div></div></td></tr>`).join('')}</tbody></table>`
            }
            html += `</div>`
        }

        // Anomaly Section
        if (config.includeAnomaly && anomalyResults) {
            html += `<h2>⚠️ Anomaly Detection Results</h2><div class="section">
<div class="grid">
<div class="card"><div class="card-value">${anomalyResults.totalRows?.toLocaleString()}</div><div class="card-label">Total Records</div></div>
<div class="card"><div class="card-value" style="color:#ef4444">${anomalyResults.anomalyCount}</div><div class="card-label">Anomalies</div></div>
<div class="card"><div class="card-value" style="color:#10b981">${anomalyResults.normalCount?.toLocaleString()}</div><div class="card-label">Normal</div></div>
<div class="card"><div class="card-value">${anomalyResults.anomalyPercentage}%</div><div class="card-label">Anomaly Rate</div></div>
</div>
<div class="insight ${parseFloat(anomalyResults.anomalyPercentage) < 5 ? 'insight-success' : parseFloat(anomalyResults.anomalyPercentage) < 15 ? 'insight-warning' : 'insight-info'}">
<strong>Detection Method:</strong> ${anomalyResults.method || 'Isolation Forest'} | 
<strong>Result:</strong> ${parseFloat(anomalyResults.anomalyPercentage) < 5 ? 'Low anomaly rate - data appears clean' : parseFloat(anomalyResults.anomalyPercentage) < 15 ? 'Moderate anomalies detected - review recommended' : 'High anomaly rate - data quality review needed'}
</div>`
            if (anomalyResults.columnStats?.length > 0) {
                html += `<h3>Column Statistics (Normal vs Anomaly)</h3><table><thead><tr><th>Column</th><th>Normal Mean</th><th>Anomaly Mean</th><th>Difference</th></tr></thead>
<tbody>${anomalyResults.columnStats.slice(0, 10).map(s => `<tr><td>${s.column}</td><td style="color:#10b981">${s.normalMean}</td><td style="color:#ef4444">${s.anomalyMean}</td><td><span class="badge ${parseFloat(s.difference) > 1 ? 'badge-warning' : 'badge-success'}">${s.difference}</span></td></tr>`).join('')}</tbody></table>`
            }
            html += `</div>`
        }

        // Time Series Section
        if (config.includeTimeSeries && timeSeriesResults) {
            const ts = timeSeriesResults.statistics
            html += `<h2>📈 Time Series Analysis</h2><div class="section">
<div class="grid">
<div class="card"><div class="card-value">${ts?.dataPoints?.toLocaleString() || '-'}</div><div class="card-label">Data Points</div></div>
<div class="card"><div class="card-value" style="color:${ts?.trend === 'Upward' ? '#10b981' : '#ef4444'}">${ts?.trend || '-'}</div><div class="card-label">Trend</div></div>
<div class="card"><div class="card-value">${ts?.seasonalityStrength || '-'}</div><div class="card-label">Seasonality</div></div>
<div class="card"><div class="card-value">${ts?.slope || '-'}</div><div class="card-label">Slope</div></div>
</div>
<h3>Statistical Summary</h3><table><thead><tr><th>Metric</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Mean</td><td>${ts?.mean || '-'}</td></tr>
<tr><td>Standard Deviation</td><td>${ts?.std || '-'}</td></tr>
<tr><td>Minimum</td><td>${ts?.min || '-'}</td></tr>
<tr><td>Maximum</td><td>${ts?.max || '-'}</td></tr>
<tr><td>Date Column</td><td>${timeSeriesResults.config?.dateColumn || '-'}</td></tr>
<tr><td>Value Column</td><td>${timeSeriesResults.config?.valueColumn || '-'}</td></tr>
</tbody></table>
<div class="insight insight-info"><strong>Trend Analysis:</strong> Data shows ${ts?.trend?.toLowerCase() || 'a'} trend with slope of ${ts?.slope || 'N/A'} and seasonality strength of ${ts?.seasonalityStrength || 'N/A'}.</div>
</div>`
        }

        // Recommendations
        html += `<h2>💡 Recommendations & Next Steps</h2><div class="section">`

        if (edaResults) {
            html += `<div class="insight ${edaResults.qualityScore >= 80 ? 'insight-success' : 'insight-warning'}"><strong>Data Quality:</strong> ${edaResults.qualityScore >= 80 ? 'Excellent data quality (' + edaResults.qualityScore + '/100). Ready for advanced modeling.' : 'Data quality score is ' + edaResults.qualityScore + '/100. Consider addressing missing values and outliers.'}</div>`
        }
        if (mlResults?.models?.[ 0 ]) {
            html += `<div class="insight insight-info"><strong>Model Recommendation:</strong> ${mlResults.models[ 0 ].type || mlResults.models[ 0 ].name} performed best. Consider hyperparameter tuning for further improvement.</div>`
        }
        if (anomalyResults) {
            html += `<div class="insight ${parseFloat(anomalyResults.anomalyPercentage) < 10 ? 'insight-success' : 'insight-warning'}"><strong>Anomaly Handling:</strong> ${anomalyResults.anomalyCount} anomalies detected (${anomalyResults.anomalyPercentage}%). ${parseFloat(anomalyResults.anomalyPercentage) < 10 ? 'Acceptable level.' : 'Review and handle before production use.'}</div>`
        }
        if (timeSeriesResults) {
            html += `<div class="insight insight-info"><strong>Time Series:</strong> ${timeSeriesResults.statistics?.trend} trend detected. Consider ARIMA or Prophet for production forecasting.</div>`
        }

        html += `</div>
<div class="footer"><p>Generated by <strong>AI Data Science Research Assistant</strong></p><p>${now}</p></div>
</div></body></html>`
        return html
    }

    const downloadReport = (format) => {
        if (!reportData) return
        if (format === 'html') {
            const blob = new Blob([ reportData ], { type: 'text/html' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `${dataset.name}_full_analysis_report.html`
            a.click()
            URL.revokeObjectURL(url)
        } else if (format === 'pdf') {
            const printWindow = window.open('', '_blank')
            printWindow.document.write(reportData)
            printWindow.document.close()
            setTimeout(() => printWindow.print(), 500)
        }
    }

    if (!dataset) {
        return (
            <div className="card text-center py-16">
                <FileText size={64} className="mx-auto text-gray-300 mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">No Dataset Loaded</h2>
                <p className="text-gray-500">Upload a dataset to generate reports</p>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="card bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold mb-1">Comprehensive Report Generator</h1>
                        <p className="text-indigo-100">Generate full analysis reports with all insights & visualizations</p>
                    </div>
                    <button onClick={generateReport} disabled={generating} className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-indigo-50 transition flex items-center gap-2">
                        {generating ? <Loader size={18} className="animate-spin" /> : <FileText size={18} />}
                        {generating ? 'Generating...' : 'Generate Report'}
                    </button>
                </div>
            </div>

            {/* Analysis Status */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                    { key: 'eda', label: 'EDA', icon: BarChart3, data: edaResults, color: 'green', value: edaResults?.qualityScore ? `${edaResults.qualityScore}/100` : 'Not Run' },
                    { key: 'ml', label: 'ML', icon: Brain, data: mlResults, color: 'purple', value: mlResults?.models?.[ 0 ]?.type || 'Not Run' },
                    { key: 'anomaly', label: 'Anomaly', icon: AlertTriangle, data: anomalyResults, color: 'red', value: anomalyResults ? `${anomalyResults.anomalyCount} found` : 'Not Run' },
                    { key: 'timeSeries', label: 'Time Series', icon: TrendingUp, data: timeSeriesResults, color: 'cyan', value: timeSeriesResults?.statistics?.trend || 'Not Run' }
                ].map(item => {
                    const Icon = item.icon
                    const hasData = !!item.data
                    return (
                        <div key={item.key} className={`card ${hasData ? '' : 'opacity-60'}`}>
                            <div className="flex items-center justify-between mb-2">
                                <Icon size={24} className={`text-${item.color}-600`} />
                                {hasData ? <CheckCircle size={18} className="text-green-500" /> : <AlertCircle size={18} className="text-gray-400" />}
                            </div>
                            <p className={`text-lg font-bold ${hasData ? `text-${item.color}-600` : 'text-gray-400'}`}>{item.value}</p>
                            <p className="text-gray-500 text-sm">{item.label} Analysis</p>
                        </div>
                    )
                })}
            </div>

            {!hasResults && (
                <div className="card bg-yellow-50 border-yellow-200">
                    <div className="flex items-center gap-3">
                        <AlertCircle size={24} className="text-yellow-600" />
                        <div>
                            <p className="font-semibold text-yellow-800">No Analysis Results Yet</p>
                            <p className="text-yellow-700 text-sm">Run analyses in Auto EDA, Auto ML, Anomaly Detection, or Time Series pages first. Results will be included in the report.</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Configuration */}
            <div className="card">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2"><Settings size={20} /> Report Sections</h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    {[
                        { key: 'includeEDA', label: 'EDA Analysis', icon: BarChart3, hasData: !!edaResults },
                        { key: 'includeML', label: 'ML Results', icon: Brain, hasData: !!mlResults },
                        { key: 'includeAnomaly', label: 'Anomaly Detection', icon: AlertTriangle, hasData: !!anomalyResults },
                        { key: 'includeTimeSeries', label: 'Time Series', icon: TrendingUp, hasData: !!timeSeriesResults },
                        { key: 'includeDataPreview', label: 'Data Preview', icon: Eye, hasData: true }
                    ].map(item => {
                        const Icon = item.icon
                        return (
                            <label key={item.key} className={`flex items-center gap-2 p-3 rounded-lg border-2 cursor-pointer transition ${config[item.key] ? 'border-purple-500 bg-purple-50' : 'border-gray-200'} ${!item.hasData ? 'opacity-50' : ''}`}>
                                <input type="checkbox" checked={config[item.key]} onChange={(e) => setConfig({...config, [item.key]: e.target.checked})} className="w-4 h-4" disabled={!item.hasData && item.key !== 'includeDataPreview'} />
                                <Icon size={16} />
                                <span className="text-sm">{item.label}</span>
                            </label>
                        )
                    })}
                </div>
            </div>

            {/* Report Preview */}
            {reportData && (
                <div className="card">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold flex items-center gap-2"><CheckCircle size={20} className="text-green-600" /> Report Generated</h3>
                        <div className="flex gap-3">
                            <button onClick={() => downloadReport('html')} className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"><Download size={18} /> HTML</button>
                            <button onClick={() => downloadReport('pdf')} className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"><Download size={18} /> PDF</button>
                            <button onClick={generateReport} className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"><RefreshCw size={18} /> Regenerate</button>
                        </div>
                    </div>
                    <div className="border rounded-lg overflow-hidden">
                        <div className="bg-gray-100 px-4 py-2 border-b flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-red-500"></div>
                            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                            <div className="w-3 h-3 rounded-full bg-green-500"></div>
                            <span className="ml-4 text-sm text-gray-600">Report Preview</span>
                        </div>
                        <iframe srcDoc={reportData} className="w-full h-[600px] border-0" title="Report Preview" />
                    </div>
                </div>
            )}

            {/* What's Included */}
            <div className="card">
                <h3 className="text-lg font-semibold mb-4">Report Contents</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {[
                        { icon: '📁', title: 'Dataset Overview', items: ['Row/column counts', 'Data types', 'Data preview'] },
                        { icon: '🔍', title: 'EDA Analysis', items: ['Quality score', 'Statistics', 'Missing data', 'Correlations', 'AI insights'] },
                        { icon: '🤖', title: 'ML Results', items: ['Model comparison', 'Best model', 'Feature importance', 'Metrics'] },
                        { icon: '⚠️', title: 'Anomaly Detection', items: ['Anomaly count', 'Detection method', 'Column statistics'] },
                        { icon: '📈', title: 'Time Series', items: ['Trend analysis', 'Seasonality', 'Statistics'] },
                        { icon: '💡', title: 'Recommendations', items: ['Data quality tips', 'Model suggestions', 'Next steps'] }
                    ].map((section, i) => (
                        <div key={i} className="flex gap-3 p-3 bg-gray-50 rounded-lg">
                            <span className="text-2xl">{section.icon}</span>
                            <div>
                                <p className="font-semibold">{section.title}</p>
                                <p className="text-xs text-gray-500">{section.items.join(' • ')}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default Reports
