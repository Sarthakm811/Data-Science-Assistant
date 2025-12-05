import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
    LayoutDashboard,
    Search,
    BarChart3,
    Brain,
    MessageSquare,
    FileText,
    ChevronLeft,
    ChevronRight
} from 'lucide-react'

const menuItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/search', icon: Search, label: 'Dataset Search' },
    { path: '/eda', icon: BarChart3, label: 'Auto EDA' },
    { path: '/ml', icon: Brain, label: 'Auto ML' },
    { path: '/chat', icon: MessageSquare, label: 'AI Chat' },
    { path: '/reports', icon: FileText, label: 'Reports' },
]

function Sidebar({ isOpen, setIsOpen }) {
    const location = useLocation()

    return (
        <aside className={`fixed left-0 top-0 h-full bg-gray-900 text-white transition-all duration-300 z-50 ${isOpen ? 'w-64' : 'w-20'}`}>
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
                {isOpen && (
                    <h1 className="text-xl font-bold gradient-text">DS Assistant</h1>
                )}
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
                >
                    {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
                </button>
            </div>

            <nav className="mt-6">
                {menuItems.map((item) => {
                    const Icon = item.icon
                    const isActive = location.pathname === item.path

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center px-4 py-3 mx-2 rounded-lg transition-all duration-200 ${isActive
                                    ? 'bg-purple-600 text-white'
                                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                                }`}
                        >
                            <Icon size={20} />
                            {isOpen && <span className="ml-3">{item.label}</span>}
                        </Link>
                    )
                })}
            </nav>

            <div className="absolute bottom-4 left-0 right-0 px-4">
                {isOpen && (
                    <div className="bg-gray-800 rounded-lg p-4">
                        <p className="text-xs text-gray-400">Powered by</p>
                        <p className="text-sm font-semibold">Gemini AI</p>
                    </div>
                )}
            </div>
        </aside>
    )
}

export default Sidebar
