import React, { useState, useRef } from 'react'
import { Menu, Upload, Database, X } from 'lucide-react'

function Header({ dataset, setDataset, toggleSidebar }) {
    const [ uploading, setUploading ] = useState(false)
    const fileInputRef = useRef(null)

    const handleFileUpload = async (e) => {
        const file = e.target.files[ 0 ]
        if (!file) return

        setUploading(true)

        // Parse CSV file
        const reader = new FileReader()
        reader.onload = (event) => {
            const text = event.target.result
            const lines = text.split('\n')
            const headers = lines[ 0 ].split(',').map(h => h.trim())
            const rows = lines.slice(1).filter(line => line.trim()).map(line => {
                const values = line.split(',')
                const row = {}
                headers.forEach((header, i) => {
                    row[ header ] = values[ i ]?.trim()
                })
                return row
            })

            setDataset({
                name: file.name,
                headers,
                rows,
                rowCount: rows.length,
                colCount: headers.length
            })
            setUploading(false)
        }
        reader.readAsText(file)
    }

    return (
        <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <button
                        onClick={toggleSidebar}
                        className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        <Menu size={20} />
                    </button>
                    <h2 className="text-xl font-semibold text-gray-800">
                        AI Data Science Research Assistant
                    </h2>
                </div>

                <div className="flex items-center gap-4">
                    {dataset ? (
                        <div className="flex items-center gap-3 bg-green-50 px-4 py-2 rounded-lg border border-green-200">
                            <Database size={18} className="text-green-600" />
                            <div>
                                <p className="text-sm font-medium text-green-800">{dataset.name}</p>
                                <p className="text-xs text-green-600">{dataset.rowCount} rows x {dataset.colCount} cols</p>
                            </div>
                            <button
                                onClick={() => setDataset(null)}
                                className="p-1 hover:bg-green-100 rounded"
                            >
                                <X size={16} className="text-green-600" />
                            </button>
                        </div>
                    ) : (
                        <div className="text-sm text-gray-500">No dataset loaded</div>
                    )}

                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                        accept=".csv"
                        className="hidden"
                    />

                    <button
                        onClick={() => fileInputRef.current?.click()}
                        disabled={uploading}
                        className="btn-primary flex items-center gap-2"
                    >
                        <Upload size={18} />
                        {uploading ? 'Uploading...' : 'Upload CSV'}
                    </button>
                </div>
            </div>
        </header>
    )
}

export default Header
