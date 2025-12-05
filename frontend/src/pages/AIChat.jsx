import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Sparkles, AlertCircle } from 'lucide-react'

function AIChat({ dataset }) {
    const [ messages, setMessages ] = useState([
        {
            role: 'assistant',
            content: 'Hello! I\'m your AI Data Science Assistant. Upload a dataset and ask me anything about your data!'
        }
    ])
    const [ input, setInput ] = useState('')
    const [ loading, setLoading ] = useState(false)
    const [ apiKey, setApiKey ] = useState('')
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [ messages ])

    const sendMessage = async () => {
        if (!input.trim()) return

        const userMessage = { role: 'user', content: input }
        setMessages(prev => [ ...prev, userMessage ])
        setInput('')
        setLoading(true)

        // Simulate AI response
        setTimeout(() => {
            let response = ''

            if (!dataset) {
                response = 'Please upload a dataset first so I can help you analyze it!'
            } else if (input.toLowerCase().includes('summary') || input.toLowerCase().includes('describe')) {
                response = `Here's a summary of your dataset "${dataset.name}":\n\n` +
                    `- Total Rows: ${dataset.rowCount}\n` +
                    `- Total Columns: ${dataset.colCount}\n` +
                    `- Columns: ${dataset.headers.join(', ')}\n\n` +
                    `Would you like me to perform a detailed analysis?`
            } else if (input.toLowerCase().includes('column')) {
                response = `Your dataset has ${dataset.colCount} columns:\n\n` +
                    dataset.headers.map((h, i) => `${i + 1}. ${h}`).join('\n') +
                    `\n\nWould you like to know more about any specific column?`
            } else if (input.toLowerCase().includes('missing')) {
                response = `I can check for missing values in your dataset. Based on a quick scan, ` +
                    `your dataset appears to have some missing values. Would you like me to run a detailed missing data analysis?`
            } else {
                response = `I understand you're asking about "${input}". ` +
                    `Based on your dataset "${dataset.name}" with ${dataset.rowCount} rows and ${dataset.colCount} columns, ` +
                    `I can help you with:\n\n` +
                    `1. Data summary and statistics\n` +
                    `2. Missing value analysis\n` +
                    `3. Column information\n` +
                    `4. Data quality assessment\n\n` +
                    `What would you like to explore?`
            }

            setMessages(prev => [ ...prev, { role: 'assistant', content: response } ])
            setLoading(false)
        }, 1500)
    }

    return (
        <div className="h-[calc(100vh-200px)] flex flex-col">
            {/* Header */}
            <div className="card mb-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="bg-purple-100 p-3 rounded-lg">
                            <Sparkles size={24} className="text-purple-600" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-800">AI Chat</h1>
                            <p className="text-gray-500 text-sm">Ask questions about your data</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <input
                            type="password"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                            placeholder="Gemini API Key"
                            className="input-field w-48"
                        />
                        {dataset && (
                            <div className="bg-green-50 px-3 py-2 rounded-lg border border-green-200">
                                <p className="text-sm text-green-700">{dataset.name}</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 card overflow-y-auto mb-4">
                <div className="space-y-4">
                    {messages.map((msg, i) => (
                        <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-purple-600' : 'bg-gray-200'
                                }`}>
                                {msg.role === 'user' ? (
                                    <User size={20} className="text-white" />
                                ) : (
                                    <Bot size={20} className="text-gray-600" />
                                )}
                            </div>
                            <div className={`max-w-[70%] rounded-lg p-4 ${msg.role === 'user'
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                }`}>
                                <p className="whitespace-pre-wrap">{msg.content}</p>
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="flex gap-3">
                            <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                                <Bot size={20} className="text-gray-600" />
                            </div>
                            <div className="bg-gray-100 rounded-lg p-4">
                                <div className="flex gap-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input */}
            <div className="card">
                <div className="flex gap-4">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Ask a question about your data..."
                        className="input-field flex-1"
                        disabled={loading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !input.trim()}
                        className="btn-primary flex items-center gap-2"
                    >
                        <Send size={18} />
                        Send
                    </button>
                </div>
            </div>
        </div>
    )
}

export default AIChat
