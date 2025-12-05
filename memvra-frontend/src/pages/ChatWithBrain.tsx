import { useState, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
// @ts-ignore
import { Send, Brain, User, Loader2, Sparkles } from 'lucide-react';
import { recallFromBrain } from '../lib/api';

interface Message {
    id: string;
    role: 'user' | 'brain';
    content: string;
    timestamp: Date;
    matches?: any[];
}

export default function ChatWithBrain() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'brain',
            content: "Hello! I'm the MemVra Brain. Ask me anything about your stored memories, or just chat with me!",
            timestamp: new Date()
        }
    ]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const chatMutation = useMutation({
        mutationFn: (query: string) => recallFromBrain(query),
        onSuccess: (data) => {
            // Add brain response
            const brainMessage: Message = {
                id: Date.now().toString() + '-brain',
                role: 'brain',
                content: data.result,
                timestamp: new Date(),
                matches: data.matches
            };
            setMessages(prev => [...prev, brainMessage]);
        },
        onError: (error: any) => {
            const errorMessage: Message = {
                id: Date.now().toString() + '-error',
                role: 'brain',
                content: `Sorry, I encountered an error: ${error.message || 'Unable to process your request'}`,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        }
    });

    const handleSend = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || chatMutation.isPending) return;

        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMessage]);

        // Send to brain
        chatMutation.mutate(input);
        setInput('');
    };

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)] flex flex-col">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-6"
                >
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-2xl flex items-center justify-center">
                            <Brain className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-serif">Chat with Brain</h1>
                            <p className="text-white/60 text-sm">Your AI memory assistant</p>
                        </div>
                    </div>
                </motion.div>

                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto mb-6 space-y-4 scroll-smooth">
                    <AnimatePresence mode="popLayout">
                        {messages.map((message) => (
                            <motion.div
                                key={message.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {message.role === 'brain' && (
                                    <div className="w-8 h-8 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-full flex items-center justify-center flex-shrink-0 border border-cyan-500/30">
                                        <Brain className="w-4 h-4 text-cyan-400" />
                                    </div>
                                )}

                                <div className={`max-w-[70%] ${message.role === 'user' ? 'order-first' : ''}`}>
                                    <div
                                        className={`p-4 rounded-2xl ${message.role === 'user'
                                                ? 'bg-cyan-500 text-black'
                                                : 'bg-white/5 border border-white/10 text-white'
                                            }`}
                                    >
                                        <p className="whitespace-pre-wrap">{message.content}</p>
                                    </div>

                                    {/* Show matches if available */}
                                    {message.matches && message.matches.length > 0 && (
                                        <div className="mt-3 space-y-2">
                                            <p className="text-xs text-white/40 px-2">Found {message.matches.length} memory match(es):</p>
                                            {message.matches.map((match, idx) => (
                                                <div key={idx} className="bg-white/5 border border-white/10 rounded-xl p-3">
                                                    <div className="flex items-center gap-2 mb-2">
                                                        <Sparkles className="w-3 h-3 text-purple-400" />
                                                        <span className={`text-xs px-2 py-0.5 rounded ${match.relevance === 'exact'
                                                                ? 'bg-green-500/20 text-green-400'
                                                                : 'bg-yellow-500/20 text-yellow-400'
                                                            }`}>
                                                            {match.relevance}
                                                        </span>
                                                    </div>
                                                    <p className="text-sm text-white/80">{match.content}</p>
                                                    <p className="text-xs text-white/30 mt-1">
                                                        {new Date(match.created_at).toLocaleDateString()}
                                                    </p>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    <p className="text-xs text-white/30 mt-1 px-2">
                                        {message.timestamp.toLocaleTimeString()}
                                    </p>
                                </div>

                                {message.role === 'user' && (
                                    <div className="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center flex-shrink-0 border border-cyan-500/30">
                                        <User className="w-4 h-4 text-cyan-400" />
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {chatMutation.isPending && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex gap-3 justify-start"
                        >
                            <div className="w-8 h-8 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-full flex items-center justify-center flex-shrink-0 border border-cyan-500/30">
                                <Brain className="w-4 h-4 text-cyan-400" />
                            </div>
                            <div className="bg-white/5 border border-white/10 p-4 rounded-2xl">
                                <div className="flex items-center gap-2 text-white/60">
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    <span className="text-sm">Brain is thinking...</span>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Form */}
                <form onSubmit={handleSend} className="flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask me anything..."
                        disabled={chatMutation.isPending}
                        className="flex-1 bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white placeholder:text-white/30 focus:outline-none focus:border-cyan-500/50 transition-colors disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={chatMutation.isPending || !input.trim()}
                        className="bg-gradient-to-br from-cyan-500 to-purple-500 text-white rounded-2xl px-6 py-4 font-medium hover:from-cyan-400 hover:to-purple-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        <Send className="w-5 h-5" />
                        <span className="hidden sm:inline">Send</span>
                    </button>
                </form>

                {/* Quick suggestions */}
                <div className="mt-4 flex flex-wrap gap-2">
                    <p className="text-xs text-white/40 w-full mb-1">Try asking:</p>
                    {['What memories do you have?', 'Search for dark mode', 'Tell me about recent changes'].map((suggestion, idx) => (
                        <button
                            key={idx}
                            onClick={() => setInput(suggestion)}
                            className="text-xs px-3 py-1.5 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition-colors text-white/60 hover:text-white/80"
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
