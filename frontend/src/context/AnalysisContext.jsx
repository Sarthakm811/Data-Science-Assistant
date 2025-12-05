import React, { createContext, useContext, useState } from 'react'

const AnalysisContext = createContext()

export function AnalysisProvider({ children }) {
    const [ edaResults, setEdaResults ] = useState(null)
    const [ mlResults, setMlResults ] = useState(null)
    const [ anomalyResults, setAnomalyResults ] = useState(null)
    const [ timeSeriesResults, setTimeSeriesResults ] = useState(null)

    const value = {
        edaResults,
        setEdaResults,
        mlResults,
        setMlResults,
        anomalyResults,
        setAnomalyResults,
        timeSeriesResults,
        setTimeSeriesResults,
        hasResults: !!(edaResults || mlResults || anomalyResults || timeSeriesResults)
    }

    return (
        <AnalysisContext.Provider value={value}>
            {children}
        </AnalysisContext.Provider>
    )
}

export function useAnalysis() {
    const context = useContext(AnalysisContext)
    if (!context) {
        throw new Error('useAnalysis must be used within AnalysisProvider')
    }
    return context
}
