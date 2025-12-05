import React, { useState } from 'react'
import { FileText, Download, FileCode, File, AlertCircle, CheckCircle } from 'lucide-react'

function Reports({ dataset }) {
    const [ generating, setGenerating ] = useState(null)
    const [ generated, setGenerated ] = useState([])

    const generateReport = (type) => {
        if (!dataset) return

        setGenerating(type)

        setTimeout(() => {
            const report = {
                id: Date.now(),
                type,
                name: `${dataset.name.replace('.csv', '')}_${type}_report`,
                date: new Date().toLocaleString(),
                size: type === 'pdf' ? '2.4 MB' : type === 'markdown' ? '45 KB' : '12 KB'
            }
            setGenerated(prev => [ report, ...prev ])
            setGenerating(null)
        }, 2000)
    }

    const downloadReport = (report) => {
        // Simulate download
        alert(`Downloading ${report.name}... (Demo mode)`)
    }

    if (!dataset) {
        return (
            <div className="card text-center py-12">
                <AlertCircle size={48} className="mx-auto text-gray-400 mb-4" />
                <h2 className="text-xl font-semibold text-gray-800 mb-2">No Dataset Loaded</h2>
                <p className="text-gray-500">Please upload a CSV file to generate reports</p>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="card">
                <h1 className="text-2xl font-bold text-gray-800 mb-2">Generate Reports</h1>
                <p className="text-gray-500 mb-6">Create professional reports from your data analysis</p>

                <div className="bg-gray-50 rounded-lg p-4 mb-6">
                    <p className="text-sm text-gray-600">
                        <strong>Dataset:</strong> {dataset.name} |
                        <strong> Rows:</strong> {dataset.rowCount} |
                        <strong> Columns:</strong> {dataset.colCount}
                    </p>
                </div>

                {/* Report Types */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* PDF Report */}
                    <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 hover:border-purple-400 transition-colors">
                        <div className="bg-red-100 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                            <FileText size={28} className="text-red-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">PDF Report</h3>
                        <p className="text-gray-500 text-sm mb-4">
                            Comprehensive PDF report with charts, statistics, and insights
                        </p>
                        <button
                            onClick={() => generateReport('pdf')}
                            disabled={generating === 'pdf'}
                            className="btn-primary w-full"
                        >
                            {generating === 'pdf' ? 'Generating...' : 'Generate PDF'}
                        </button>
                    </div>

                    {/* Markdown Report */}
                    <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 hover:border-purple-400 transition-colors">
                        <div className="bg-blue-100 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                            <File size={28} className="text-blue-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">Markdown Report</h3>
                        <p className="text-gray-500 text-sm mb-4">
                            Text-based report for documentation and sharing
                        </p>
                        <button
                            onClick={() => generateReport('markdown')}
                            disabled={generating === 'markdown'}
                            className="btn-primary w-full"
                        >
                            {generating === 'markdown' ? 'Generating...' : 'Generate Markdown'}
                        </button>
                    </div>

                    {/* Python Code */}
                    <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 hover:border-purple-400 transition-colors">
                        <div className="bg-green-100 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                            <FileCode size={28} className="text-green-600" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-800 mb-2">Python Code</h3>
                        <p className="text-gray-500 text-sm mb-4">
                            Reproducible Python code for your analysis
                        </p>
                        <button
                            onClick={() => generateReport('python')}
                            disabled={generating === 'python'}
                            className="btn-primary w-full"
                        >
                            {generating === 'python' ? 'Generating...' : 'Generate Code'}
                        </button>
                    </div>
                </div>
            </div>

            {/* Generated Reports */}
            {generated.length > 0 && (
                <div className="card">
                    <h2 className="text-lg font-semibold text-gray-800 mb-4">Generated Reports</h2>
                    <div className="space-y-3">
                        {generated.map((report) => (
                            <div key={report.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                <div className="flex items-center gap-4">
                                    <div className={`p-2 rounded-lg ${report.type === 'pdf' ? 'bg-red-100' :
                                            report.type === 'markdown' ? 'bg-blue-100' : 'bg-green-100'
                                        }`}>
                                        {report.type === 'pdf' ? <FileText size={20} className="text-red-600" /> :
                                            report.type === 'markdown' ? <File size={20} className="text-blue-600" /> :
                                                <FileCode size={20} className="text-green-600" />}
                                    </div>
                                    <div>
                                        <p className="font-medium text-gray-800">{report.name}</p>
                                        <p className="text-sm text-gray-500">{report.date} • {report.size}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <CheckCircle size={20} className="text-green-500" />
                                    <button
                                        onClick={() => downloadReport(report)}
                                        className="btn-secondary flex items-center gap-2"
                                    >
                                        <Download size={16} />
                                        Download
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}

export default Reports
