import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import DatasetSearch from './pages/DatasetSearch'
import AutoEDA from './pages/AutoEDA'
import AutoML from './pages/AutoML'
import AIChat from './pages/AIChat'
import Reports from './pages/Reports'
import AnomalyDetection from './pages/AnomalyDetection'
import TimeSeries from './pages/TimeSeries'
import { AnalysisProvider } from './context/AnalysisContext'

function App() {
    const [ dataset, setDataset ] = useState(null)
    const [ sidebarOpen, setSidebarOpen ] = useState(true)

    return (
        <AnalysisProvider>
            <Router>
                <div className="flex h-screen bg-gray-100">
                    <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

                    <div className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
                        <Header
                            dataset={dataset}
                            setDataset={setDataset}
                            toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
                        />

                        <main className="flex-1 overflow-auto p-6">
                            <Routes>
                                <Route path="/" element={<Dashboard dataset={dataset} />} />
                                <Route path="/search" element={<DatasetSearch setDataset={setDataset} />} />
                                <Route path="/eda" element={<AutoEDA dataset={dataset} />} />
                                <Route path="/ml" element={<AutoML dataset={dataset} />} />
                                <Route path="/anomaly" element={<AnomalyDetection dataset={dataset} />} />
                                <Route path="/timeseries" element={<TimeSeries dataset={dataset} />} />
                                <Route path="/chat" element={<AIChat dataset={dataset} />} />
                                <Route path="/reports" element={<Reports dataset={dataset} />} />
                            </Routes>
                        </main>
                    </div>
                </div>
            </Router>
        </AnalysisProvider>
    )
}

export default App
