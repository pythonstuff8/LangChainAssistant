import ChatInterface from '@/components/ChatInterface';
import { Zap, BookOpen, Activity } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="glass border-b border-[var(--border)] sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold gradient-text">LangChain Assistant</h1>
                <p className="text-xs text-[var(--muted)]">AI-Powered Documentation Helper</p>
              </div>
            </div>

            {/* Quick Links */}
            <div className="hidden md:flex items-center gap-4">
              <a
                href="https://python.langchain.com/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
              >
                <BookOpen className="w-4 h-4" />
                Docs
              </a>
              <a
                href="https://smith.langchain.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--foreground)] transition-colors"
              >
                <Activity className="w-4 h-4" />
                LangSmith
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Feature Pills */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-wrap justify-center gap-3">
          <div className="glass-card px-4 py-2 rounded-full flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500" />
            <span className="text-sm">LangChain</span>
          </div>
          <div className="glass-card px-4 py-2 rounded-full flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-500" />
            <span className="text-sm">LangGraph</span>
          </div>
          <div className="glass-card px-4 py-2 rounded-full flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-orange-500" />
            <span className="text-sm">LangSmith</span>
          </div>
        </div>
      </div>

      {/* Chat Container */}
      <div className="flex-1 container mx-auto px-4 pb-4 max-w-4xl">
        <div className="glass rounded-2xl h-[calc(100vh-220px)] min-h-[500px] overflow-hidden flex flex-col shadow-2xl">
          <ChatInterface />
        </div>
      </div>

      {/* Footer */}
      <footer className="py-4 text-center text-xs text-[var(--muted)]">
        <p>By Suhaan Thayyil</p>
      </footer>
    </main>
  );
}
