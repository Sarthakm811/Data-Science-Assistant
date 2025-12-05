import React from 'react'
import { Link } from 'react-router-dom'
import { Search, BarChart3, Brain, MessageSquare, FileText, Database } from 'lucide-react'

const features = [
    {
        icon: Search,
        title: 'Dataset Search',
        description: 'Search and download datasets from Kaggle',
        path: '/search',
        color: 'bg-blue-500'
    },
    {
        icon: BarChart3,
        title: 'Auto EDA',
        description: 'Automated exploratory data analysis with visualizations',
        path: '/eda',
        color: 'bg-green-500'
    },
    {
        icon: Brain,
        title: 'Auto ML',
        description: 'Train and compare machine learning models automatically',
        path: '/ml',
        color: 'bg-purple-500'
    },
    {
        icon: MessageSquare,
        title: 'AI Chat',
        description: 'Ask questions about your data and get AI insights',
        path: '/chat',
        color: 'bg-pink-500'
    },
    {
        icon: FileText,
        title: 'Reports',
        description: 'Generate professional PDF and markdown reports',
        path: '/reports',
        color: 'bg-orange-500'
    }
]

function Dashboard({ dataset }) {
    return (
        <div className="space-y-8">
            {/* Hero Section */}
            <div className="card bg-gradient-to-r from-purple-600 to-pink-600 text-white">
                <h1 className="text-3xl font-bold mb-2">Welcome to AI Data Science Assistant</h1>
                <p className="text-purple-100 mb-4">Your personal AI-powered data scientist</p>

                {dataset ? (
                    <div className="bg-white/20 rounded-lg p-4 inline-block">
                        <div className="flex items-center gap-3">
                            <Database size={24} />
                            <div>
                                <p className="font-semibold">{dataset.name}</p>
                                <p className="text-sm text-purple-100">{dataset.rowCount} rows x {dataset.colCount} columns</p>
                            </div>
                        </div>
                    </div>
                ) : (
                    <p className="text-purple-200">Upload a dataset to get started</p>
                )}
            </div>

            {/* Stats */}
            {dataset && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="card text-center">
                        <p className="text-3xl font-bold text-purple-600">{dataset.rowCount}</p>
                        <p className="text-gray-500">Rows</p>
                    </div>
                    <div className="card text-center">
                        <p className="text-3xl font-bold text-blue-600">{dataset.colCount}</p>
                        <p className="text-gray-500">Columns</p>
                    </div>
                    <div className="card text-center">
                        <p className="text-3xl font-bold text-green-600">0</p>
                        <p className="text-gray-500">Analyses Run</p>
                    </div>
                    <div className="card text-center">
                        <p className="text-3xl font-bold text-orange-600">0</p>
                        <p className="text-gray-500">Models Trained</p>
                    </div>
                </div>
            )}

            {/* Features Grid */}
            <div>
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Features</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {features.map((feature) => {
                        const Icon = feature.icon
                        return (
                            <Link key={feature.path} to={feature.path}>
                                <div className="card hover:scale-105 transition-transform cursor-pointer">
                                    <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                                        <Icon size={24} className="text-white" />
                                    </div>
                                    <h3 className="text-lg font-semibold text-gray-800 mb-2">{feature.title}</h3>
                                    <p className="text-gray-500 text-sm">{feature.description}</p>
                                </div>
                            </Link>
                        )
                    })}
                </div>
            </div>

            {/* Data Preview */}
            {dataset && (
                <div className="card">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">Data Preview</h2>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="bg-gray-50">
                                    {dataset.headers.map((header, i) => (
                                        <th key={i} className="px-4 py-3 text-left font-semibold text-gray-700 border-b">
                                            {header}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {dataset.rows.slice(0, 5).map((row, i) => (
                                    <tr key={i} className="hover:bg-gray-50">
                                        {dataset.headers.map((header, j) => (
                                            <td key={j} className="px-4 py-3 border-b text-gray-600">
                                                {row[ header ]}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Dashboard
