'use client';

import { Source } from '@/lib/api';
import { ExternalLink, FileText } from 'lucide-react';

interface SourceCardProps {
    source: Source;
}

const serviceColors: Record<string, string> = {
    langchain: 'bg-green-500/20 text-green-400 border-green-500/30',
    langgraph: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    langsmith: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
};

export default function SourceCard({ source }: SourceCardProps) {
    return (
        <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="source-card block group"
        >
            <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)]">
                    <FileText className="w-4 h-4 text-[var(--accent)]" />
                </div>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-medium text-sm text-[var(--foreground)] truncate group-hover:text-[var(--accent)] transition-colors">
                            {source.title}
                        </h4>
                        <ExternalLink className="w-3 h-3 text-[var(--muted)] opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <span className={`inline-block px-2 py-0.5 text-xs rounded-full border mb-2 ${serviceColors[source.service] || 'bg-gray-500/20 text-gray-400'}`}>
                        {source.service}
                    </span>
                    <p className="text-xs text-[var(--muted)] line-clamp-2">
                        {source.content_preview}
                    </p>
                </div>
            </div>
        </a>
    );
}
