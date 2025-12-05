import React, { useState, useRef, useEffect, useCallback } from 'react'
import { Send, Bot, User, AlertCircle, Loader, Sparkles } from 'lucide-react'
import { chatAPI, sessionAPI, handleApiError } from '../services/api'

function AIChat({ dataset }) {
    const [ messages, setMessages ] = useState([
        {
            role: 'assistant',
            content: 'Hello! I\'m your AI Data Science Assistant. Upload a dataset and ask me anything about your data!'
        }
    ])
    const [ input, setInput ] = useState('')
    const [ loading, setLoading ] = useState(false)
    const [ error, setError ] = useState(null)
    const [ sessionId, setSessionId ] = useState(null)
    const messagesEndRef = useRef(null)

    // Initialize session
    useEffect(() => {
        const initSession = async () => {
            try {
                const session = await sessionAPI.createSession()
                setSessionId(session.session_id)
            } catch (err) {
                console.log('Session initialization skipped (optional)')
            }
        }
        initSession()
    }, [])

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [ messages ])

    const sendMessage = useCallback(async () => {
        if (!input.trim()) return

        const userMessage = { role: 'user', content: input }
        setMessages(prev => [ ...prev, userMessage ])
        setInput('')
        setLoading(true)
        setError(null)

        try {
            const response = await chatAPI.sendMessage(
                input,
                dataset?.id || dataset?.datasetId,
                sessionId || 'demo'
            )

            const assistantMessage = {
                role: 'assistant',
                content: response.response || response.message || 'I understood your question'
            }
            setMessages(prev => [ ...prev, assistantMessage ])
        } catch (err) {
            setError(handleApiError(err))
            const errorMessage = {
                role: 'assistant',
                content: `Sorry, I encountered an error: ${handleApiError(err)}`
            }
            setMessages(prev => [ ...prev, errorMessage ])
        } finally {
            setLoading(false)
        }
    }, [ input, dataset, sessionId ])

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
                        <div className="bg-green-50 px-3 py-2 rounded-lg border border-green-200">
                            <p className="text-sm text-green-700">AI Ready</p>
                        </div>
                        {dataset && (
                            <div className="bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
                                <p className="text-sm text-blue-700">{dataset.name}</p>
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
