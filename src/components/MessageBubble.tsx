'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Source } from '@/lib/api';
import SourceCard from './SourceCard';
import { User, Bot, Clock } from 'lucide-react';

export interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    sources?: Source[];
    processingTime?: number;
    timestamp: Date;
}

interface MessageBubbleProps {
    message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
    const isUser = message.role === 'user';

    return (
        <div
            className={`flex gap-3 animate-fade-in ${isUser ? 'flex-row-reverse' : ''}`}
        >
            {/* Avatar */}
            <div className={`
        flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center
        ${isUser
                    ? 'bg-gradient-to-br from-[var(--primary)] to-purple-600'
                    : 'bg-gradient-to-br from-[var(--accent)] to-cyan-600'
                }
      `}>
                {isUser ? (
                    <User className="w-5 h-5 text-white" />
                ) : (
                    <Bot className="w-5 h-5 text-white" />
                )}
            </div>

            {/* Message Content */}
            <div className={`flex-1 max-w-[80%] ${isUser ? 'text-right' : ''}`}>
                {/* Message Bubble */}
                <div className={`
          inline-block px-4 py-3 ${isUser ? 'message-user' : 'message-assistant'}
        `}>
                    {isUser ? (
                        <p className="text-white">{message.content}</p>
                    ) : (
                        <div className="prose prose-invert prose-sm max-w-none">
                            <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                                components={{
                                    // Custom code block rendering
                                    code({ className, children, ...props }) {
                                        const match = /language-(\w+)/.exec(className || '');
                                        const isInline = !match;

                                        if (isInline) {
                                            return (
                                                <code className={className} {...props}>
                                                    {children}
                                                </code>
                                            );
                                        }

                                        return (
                                            <pre className="overflow-x-auto">
                                                <code className={className} {...props}>
                                                    {children}
                                                </code>
                                            </pre>
                                        );
                                    },
                                }}
                            >
                                {message.content}
                            </ReactMarkdown>
                        </div>
                    )}
                </div>

                {/* Processing Time */}
                {message.processingTime && (
                    <div className="flex items-center gap-1 mt-1 text-xs text-[var(--muted)]">
                        <Clock className="w-3 h-3" />
                        <span>{message.processingTime}s</span>
                    </div>
                )}

                {/* Sources */}
                {message.sources && message.sources.length > 0 && (
                    <div className="mt-3 space-y-2">
                        <p className="text-xs text-[var(--muted)] font-medium mb-2">
                            📚 Sources ({message.sources.length})
                        </p>
                        <div className="grid gap-2">
                            {message.sources.map((source, index) => (
                                <SourceCard key={index} source={source} />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
