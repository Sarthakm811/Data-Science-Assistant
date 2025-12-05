import React, { useState } from 'react'
import { Search, Download, ExternalLink, Database } from 'lucide-react'

// Mock datasets for demo
const mockDatasets = [
    { id: 'titanic', title: 'Titanic Dataset', size: '60 KB', downloads: '50K+' },
    { id: 'iris', title: 'Iris Flower Dataset', size: '5 KB', downloads: '100K+' },
    { id: 'housing', title: 'California Housing', size: '400 KB', downloads: '30K+' },
    { id: 'mnist', title: 'MNIST Digits', size: '11 MB', downloads: '200K+' },
]

function DatasetSearch({ setDataset }) {
    const [ query, setQuery ] = useState('')
    const [ results, setResults ] = useState([])
    const [ loading, setLoading ] = useState(false)
    const [ credentials, setCredentials ] = useState({ username: '', key: '' })

    const handleSearch = async () => {
        if (!query) return

        setLoading(true)
        // Simulate API call
        setTimeout(() => {
            const filtered = mockDatasets.filter(d =>
                d.title.toLowerCase().includes(query.toLowerCase())
            )
            setResults(filtered.length > 0 ? filtered : mockDatasets)
            setLoading(false)
        }, 1000)
    }

    const handleDownload = (dataset) => {
        // Simulate download
        alert(`Downloading ${dataset.title}... (Demo mode)`)
    }

    return (
        <div className="space-y-6">
            <div className="card">
                <h1 className="text-2xl font-bold text-gray-800 mb-2">Search Kaggle Datasets</h1>
                <p className="text-gray-500 mb-6">Find and download datasets from Kaggle</p>

                {/* Credentials */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Kaggle Username</label>
                        <input
                            type="text"
                            value={credentials.username}
                            onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                            className="input-field"
                            placeholder="Enter username"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Kaggle API Key</label>
                        <input
                            type="password"
                            value={credentials.key}
                            onChange={(e) => setCredentials({ ...credentials, key: e.target.value })}
                            className="input-field"
                            placeholder="Enter API key"
                        />
                    </div>
                </div>

                {/* Search */}
                <div className="flex gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                            className="input-field pl-10"
                            placeholder="Search datasets (e.g., titanic, housing, iris)"
                        />
                    </div>
                    <button
                        onClick={handleSearch}
                        disabled={loading}
                        className="btn-primary"
                    >
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </div>
            </div>

            {/* Results */}
            {results.length > 0 && (
                <div className="space-y-4">
                    <h2 className="text-lg font-semibold text-gray-800">Search Results ({results.length})</h2>

                    {results.map((dataset) => (
                        <div key={dataset.id} className="card flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div className="bg-purple-100 p-3 rounded-lg">
                                    <Database size={24} className="text-purple-600" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-gray-800">{dataset.title}</h3>
                                    <p className="text-sm text-gray-500">
                                        Size: {dataset.size} • Downloads: {dataset.downloads}
                                    </p>
                                </div>
                            </div>

                            <div className="flex gap-2">
                                <a
                                    href={`https://kaggle.com/datasets/${dataset.id}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-secondary flex items-center gap-2"
                                >
                                    <ExternalLink size={16} />
                                    View
                                </a>
                                <button
                                    onClick={() => handleDownload(dataset)}
                                    className="btn-primary flex items-center gap-2"
                                >
                                    <Download size={16} />
                                    Download
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default DatasetSearch
