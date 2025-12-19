'use client';

import { useState, useRef, useEffect, FormEvent } from 'react';
import { sendChatMessage, ServiceFilter } from '@/lib/api';
import MessageBubble, { Message } from './MessageBubble';
import ServiceSelector from './ServiceSelector';
import { Send, Sparkles, Loader2, Maximize2, Minimize2 } from 'lucide-react';

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [serviceFilter, setServiceFilter] = useState<ServiceFilter>('all');
    const [isFullScreen, setIsFullScreen] = useState(true);

    // NOTE: Auto-scroll disabled by user request
    // const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // Auto-scroll to bottom REMOVED
    // useEffect(() => {
    //     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    // }, [messages]);

    // Auto-resize textarea
    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.style.height = 'auto';
            inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 150)}px`;
        }
    }, [input]);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input.trim(),
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        setError(null);

        try {
            const response = await sendChatMessage(userMessage.content, serviceFilter);

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: response.answer,
                sources: response.sources,
                processingTime: response.processing_time,
                timestamp: new Date(),
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
            // Remove the user message if we got an error
            setMessages(prev => prev.slice(0, -1));
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    const toggleFullScreen = () => {
        setIsFullScreen(!isFullScreen);
    };

    const exampleQuestions = [
        "How do I create a simple chain in LangChain?",
        "What are the key concepts in LangGraph?",
        "How do I set up tracing with LangSmith?",
        "Explain LCEL and give me an example",
    ];

    const containerClasses = isFullScreen
        ? "fixed inset-0 z-50 bg-[var(--background)] flex flex-col"
        : "flex flex-col h-full";

    return (
        <div className={containerClasses}>
            {/* Header / Service Selector */}
            <div className="flex-shrink-0 p-4 border-b border-[var(--border)] flex justify-between items-center bg-[var(--secondary)]">
                <ServiceSelector selected={serviceFilter} onChange={setServiceFilter} />
                <button
                    onClick={toggleFullScreen}
                    className="p-2 hover:bg-[var(--primary)] hover:text-white rounded-lg transition-colors text-[var(--muted)]"
                    title={isFullScreen ? "Exit Full Screen" : "Full Screen"}
                >
                    {isFullScreen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
                </button>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.length === 0 ? (
                    /* Empty State */
                    <div className="flex flex-col items-center justify-center h-full text-center py-12">
                        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center mb-6 animate-pulse-glow">
                            <Sparkles className="w-10 h-10 text-white" />
                        </div>
                        <h2 className="text-2xl font-bold gradient-text mb-2">
                            LangChain Documentation Assistant
                        </h2>
                        <p className="text-[var(--muted)] mb-8 max-w-md">
                            Ask me anything about LangChain, LangGraph, or LangSmith.
                            I'll search the documentation and provide accurate answers with sources.
                        </p>

                        {/* Example Questions */}
                        <div className="grid gap-2 w-full max-w-lg">
                            <p className="text-sm text-[var(--muted)] mb-2">Try asking:</p>
                            {exampleQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    onClick={() => setInput(question)}
                                    className="glass-card text-left px-4 py-3 rounded-xl text-sm hover:border-[var(--primary)] transition-all"
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    /* Message List */
                    <>
                        {messages.map((message) => (
                            <MessageBubble key={message.id} message={message} />
                        ))}

                        {/* Loading Indicator */}
                        {isLoading && (
                            <div className="flex gap-3 animate-fade-in">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[var(--accent)] to-cyan-600 flex items-center justify-center">
                                    <Loader2 className="w-5 h-5 text-white animate-spin" />
                                </div>
                                <div className="message-assistant px-4 py-3">
                                    <div className="flex gap-1.5">
                                        <span className="typing-dot" />
                                        <span className="typing-dot" />
                                        <span className="typing-dot" />
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Scroll anchor removed */}
                        {/* <div ref={messagesEndRef} /> */}
                    </>
                )}
            </div>

            {/* Error Display */}
            {error && (
                <div className="mx-4 mb-2 p-3 rounded-lg bg-[var(--error)]/10 border border-[var(--error)]/30 text-[var(--error)] text-sm">
                    {error}
                </div>
            )}

            {/* Input Area */}
            <div className="flex-shrink-0 p-4 border-t border-[var(--border)] bg-[var(--secondary)]">
                <form onSubmit={handleSubmit} className="flex gap-3">
                    <div className="flex-1 relative">
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask about LangChain, LangGraph, or LangSmith..."
                            className="chat-input w-full px-4 py-3 pr-12 resize-none min-h-[48px] max-h-[150px]"
                            rows={1}
                            disabled={isLoading}
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="btn-primary flex items-center gap-2 self-end"
                    >
                        {isLoading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                        <span className="hidden sm:inline">Send</span>
                    </button>
                </form>
                <p className="text-xs text-[var(--muted)] mt-2 text-center">
                    Powered by RAG • Press Enter to send, Shift+Enter for new line
                </p>
            </div>
        </div>
    );
}
