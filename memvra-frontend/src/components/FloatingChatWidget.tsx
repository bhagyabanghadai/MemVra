import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Sparkles, Zap, Brain, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../context/AuthContext';

interface Message {
    id: string;
    text: string;
    sender: 'user' | 'brain';
    timestamp: Date;
    metadata?: {
        confidence?: number;
        facts_count?: number;
    };
}

const FloatingChatWidget = () => {
    const { isAuthenticated, token } = useAuth(); // Auth Gating
    const [isOpen, setIsOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState<Message[]>([]);
    const [isThinking, setIsThinking] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isThinking]);

    // Initial Greeting
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([{
                id: 'init',
                text: "MemVra Neural Core online. I am ready to access your external memory.",
                sender: 'brain',
                timestamp: new Date()
            }]);
        }
    }, [isOpen]);

    const handleSend = async () => {
        if (!query.trim()) return;

        const userMsg: Message = {
            id: Date.now().toString(),
            text: query,
            sender: 'user',
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMsg]);
        setQuery('');
        setIsThinking(true);

        // Special Command: /dream
        if (userMsg.text.trim().toLowerCase() === '/dream') {
            try {
                const response = await fetch('/v1/intuitive/dream', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: 'default' })
                });
                const data = await response.json();

                setMessages(prev => [...prev, {
                    id: Date.now().toString(),
                    text: `✨ Dream Cycle Complete!\n\nSummary: ${data.summary}\nPatterns Found: ${data.patterns.length}\nSentiment: ${data.sentiment}\nCompression Ratio: ${data.compression_stats?.compression_ratio?.toFixed(2) || 'N/A'}`,
                    sender: 'brain',
                    timestamp: new Date()
                }]);
            } catch (error) {
                setMessages(prev => [...prev, {
                    id: Date.now().toString(),
                    text: "❌ Dream Cycle failed. Check console for details.",
                    sender: 'brain',
                    timestamp: new Date()
                }]);
            }
            setIsThinking(false);
            return;
        }

        try {
            // Streaming Request
            const response = await fetch('/v1/logical/stream?query=' + encodeURIComponent(userMsg.text) + '&user_id=default', {
                method: 'POST',
                headers: {
                    'Accept': 'text/plain'
                }
            });

            if (!response.body) throw new Error("No response body");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let brainMsgId = (Date.now() + 1).toString();
            let fullText = "";
            let isFirstChunk = true;

            // Create placeholder message
            setMessages(prev => [...prev, {
                id: brainMsgId,
                text: "",
                sender: 'brain',
                timestamp: new Date()
            }]);

            setIsThinking(false); // Start showing stream immediately

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);

                // First chunk might contain metadata JSON
                if (isFirstChunk && chunk.startsWith('{')) {
                    const parts = chunk.split('\n');
                    if (parts.length > 1) {
                        // Parse metadata if needed, ignore for now
                        fullText += parts.slice(1).join('\n');
                    } else {
                        fullText += chunk;
                    }
                    isFirstChunk = false;
                } else {
                    fullText += chunk;
                }

                // Update message in place
                setMessages(prev => prev.map(m =>
                    m.id === brainMsgId ? { ...m, text: fullText } : m
                ));
            }

        } catch (error) {
            console.error("Brain error:", error);
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                text: "Neural link unstable. Please try again.",
                sender: 'brain',
                timestamp: new Date()
            }]);
            setIsThinking(false);
        }
    };

    // Auth Gating: Don't render if not logged in
    // For demo purposes, we might want to show a locked state instead of hidden
    if (!isAuthenticated && !token) {
        return null;
    }

    return (
        <div className="fixed bottom-6 right-6 z-50 font-sans">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        className="absolute bottom-20 right-0 w-[480px] h-[700px] bg-[#0f172a]/95 backdrop-blur-xl border border-slate-700/50 rounded-2xl shadow-2xl flex flex-col overflow-hidden ring-1 ring-white/10"
                    >
                        {/* Header - Executive Suite Theme */}
                        <div className="p-4 bg-gradient-to-r from-slate-900 to-slate-800 border-b border-slate-700 flex justify-between items-center">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500/20 to-amber-600/10 flex items-center justify-center border border-amber-500/30">
                                    <Brain className="w-5 h-5 text-amber-400" />
                                </div>
                                <div>
                                    <h3 className="font-serif text-lg text-slate-100 tracking-wide">MemVra Core</h3>
                                    <div className="flex items-center gap-2">
                                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                                        <span className="text-xs text-slate-400 font-medium">System Online</span>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-400 hover:text-white"
                            >
                                <ChevronDown className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Chat Area */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
                            {messages.map((msg) => (
                                <motion.div
                                    key={msg.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div className={`max-w-[85%] ${msg.sender === 'user'
                                        ? 'bg-gradient-to-br from-amber-600 to-amber-700 text-white shadow-lg shadow-amber-900/20'
                                        : 'bg-slate-800/80 text-slate-200 border border-slate-700'
                                        } rounded-2xl px-5 py-4 relative group`}
                                    >
                                        <p className="leading-relaxed text-[15px] whitespace-pre-wrap">{msg.text}</p>
                                        <span className="text-[10px] opacity-50 mt-2 block font-medium tracking-wider">
                                            {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>
                                </motion.div>
                            ))}

                            {isThinking && (
                                <div className="flex justify-start">
                                    <div className="bg-slate-800/50 rounded-2xl px-4 py-3 flex items-center gap-2 border border-slate-700/50">
                                        <Sparkles className="w-4 h-4 text-amber-400 animate-spin-slow" />
                                        <span className="text-xs text-slate-400 font-medium animate-pulse">Reasoning...</span>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="p-4 bg-slate-900/50 border-t border-slate-700/50 backdrop-blur-md">
                            <div className="relative flex items-center">
                                <input
                                    type="text"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                    placeholder="Ask your external memory..."
                                    className="w-full bg-slate-950/50 border border-slate-700 text-slate-200 rounded-xl pl-4 pr-12 py-4 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50 placeholder-slate-500 transition-all shadow-inner"
                                />
                                <button
                                    onClick={handleSend}
                                    disabled={!query.trim() || isThinking}
                                    className="absolute right-2 p-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-amber-900/30"
                                >
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                            <div className="mt-2 text-center">
                                <span className="text-[10px] text-slate-600 font-medium tracking-widest uppercase">
                                    Powered by MemVra Neural Engine v2.1
                                </span>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Toggle Button */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsOpen(!isOpen)}
                className="w-16 h-16 rounded-full bg-gradient-to-br from-slate-800 to-slate-900 text-amber-500 shadow-2xl shadow-black/50 border border-slate-700 flex items-center justify-center hover:border-amber-500/50 transition-all group relative"
            >
                <div className="absolute inset-0 rounded-full bg-amber-500/10 blur-md group-hover:bg-amber-500/20 transition-all" />
                {isOpen ? <X className="w-7 h-7 relative z-10" /> : <MessageSquare className="w-7 h-7 relative z-10" />}

                {/* Notification Badge */}
                <span className="absolute top-0 right-0 w-4 h-4 bg-amber-500 rounded-full border-2 border-slate-900 flex items-center justify-center">
                    <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
                </span>
            </motion.button>
        </div>
    );
};

export default FloatingChatWidget;
