import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getApiKeys, createApiKey, revokeApiKey, getBrainStatus, triggerDreamCycle, searchFacts } from '../lib/api';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { Key, Plus, Trash2, Copy, Check, Brain, Zap, Database, TrendingUp, Sparkles, FileText, User } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
    const { logout } = useAuth();
    const queryClient = useQueryClient();
    const [newKeyName, setNewKeyName] = useState('');
    const [createdKey, setCreatedKey] = useState<string | null>(null);
    const [copied, setCopied] = useState(false);

    // Fetch brain statistics
    const { data: brainStats } = useQuery({
        queryKey: ['brainStats'],
        queryFn: getBrainStatus,
        refetchInterval: 30000 // Refresh every 30s
    });

    // Fetch recent facts for dashboard overview
    const { data: recentFacts } = useQuery({
        queryKey: ['recentFacts'],
        queryFn: () => searchFacts({ page: 0, size: 5 })
    });

    const { data: keys, isLoading } = useQuery({
        queryKey: ['apiKeys'],
        queryFn: getApiKeys
    });

    const createMutation = useMutation({
        mutationFn: createApiKey,
        onSuccess: (data) => {
            setCreatedKey(data.key);
            setNewKeyName('');
            queryClient.invalidateQueries({ queryKey: ['apiKeys'] });
        }
    });

    const revokeMutation = useMutation({
        mutationFn: revokeApiKey,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['apiKeys'] });
        }
    });

    const dreamMutation = useMutation({
        mutationFn: async () => {
            if (!recentFacts?.content) return null;
            return triggerDreamCycle(recentFacts.content.map(f => ({
                content: f.content,
                fact_id: f.fact_id,
                created_at: f.created_at
            })));
        }
    });

    const handleCopy = () => {
        if (createdKey) {
            navigator.clipboard.writeText(createdKey);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-7xl mx-auto">
                <div className="flex items-end justify-between mb-12">
                    <div>
                        <h1 className="text-4xl font-serif mb-2">Dashboard</h1>
                        <p className="text-white/60">Your memory system command center.</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <Link
                            to="/profile"
                            className="text-sm text-white/60 hover:text-white transition-colors flex items-center gap-2"
                        >
                            <User className="w-4 h-4" />
                            Profile
                        </Link>
                        <button
                            onClick={logout}
                            className="text-sm text-white/40 hover:text-white transition-colors"
                        >
                            Sign Out
                        </button>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <Link
                        to="/record"
                        className="bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-3xl p-6 hover:scale-105 transition-transform"
                    >
                        <FileText className="w-8 h-8 text-cyan-400 mb-4" />
                        <h3 className="text-lg font-medium mb-2">Record Fact</h3>
                        <p className="text-sm text-white/60">Capture new memories</p>
                    </Link>

                    <button
                        onClick={() => dreamMutation.mutate()}
                        disabled={dreamMutation.isPending || !recentFacts?.content?.length}
                        className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-3xl p-6 hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed text-left"
                    >
                        <Sparkles className="w-8 h-8 text-purple-400 mb-4" />
                        <h3 className="text-lg font-medium mb-2">
                            {dreamMutation.isPending ? 'Analyzing...' : 'Dream Cycle'}
                        </h3>
                        <p className="text-sm text-white/60">Discover patterns</p>
                    </button>

                    <Link
                        to="/explore"
                        className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-3xl p-6 hover:scale-105 transition-transform"
                    >
                        <Database className="w-8 h-8 text-green-400 mb-4" />
                        <h3 className="text-lg font-medium mb-2">Explore</h3>
                        <p className="text-sm text-white/60">Browse all memories</p>
                    </Link>
                </div>

                {/* Brain Statistics */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white/5 border border-white/10 rounded-3xl p-8 mb-8"
                >
                    <h2 className="text-xl font-medium mb-6 flex items-center gap-2">
                        <Brain className="w-5 h-5 text-cyan-400" />
                        Brain Status
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white/5 rounded-2xl p-6">
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-sm text-white/60">Logical Brain</span>
                                <div className={`w-2 h-2 rounded-full ${brainStats?.logicalBrain === 'online' ? 'bg-green-400' : 'bg-red-400'}`} />
                            </div>
                            <p className="text-2xl font-bold">{brainStats?.logicalBrain || 'offline'}</p>
                        </div>

                        <div className="bg-white/5 rounded-2xl p-6">
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-sm text-white/60">Intuitive Brain</span>
                                <div className={`w-2 h-2 rounded-full ${brainStats?.intuitiveBrain === 'online' ? 'bg-green-400' : 'bg-red-400'}`} />
                            </div>
                            <p className="text-2xl font-bold">{brainStats?.intuitiveBrain || 'offline'}</p>
                        </div>

                        <div className="bg-white/5 rounded-2xl p-6">
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-sm text-white/60">Total Memories</span>
                                <TrendingUp className="w-4 h-4 text-white/40" />
                            </div>
                            <p className="text-2xl font-bold">{recentFacts?.totalElements || 0}</p>
                        </div>
                    </div>

                    {dreamMutation.isSuccess && dreamMutation.data && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            className="mt-6 bg-purple-500/10 border border-purple-500/20 rounded-xl p-6"
                        >
                            <h3 className="text-lg font-medium text-purple-400 mb-4">Analysis Complete</h3>
                            <div className="space-y-3 text-sm text-white/80">
                                <p><strong>Patterns Discovered:</strong> {dreamMutation.data.patterns.length}</p>
                                {dreamMutation.data.patterns.map((pattern, i) => (
                                    <p key={i} className="pl-4 border-l-2 border-purple-500/50">• {pattern}</p>
                                ))}
                                <p className="mt-4 text-white/60"><strong>Sentiment:</strong> {dreamMutation.data.sentiment}</p>
                            </div>
                        </motion.div>
                    )}
                </motion.div>

                {/* Create Key Section */}
                <div className="bg-white/5 border border-white/10 rounded-3xl p-8 mb-8">
                    <h2 className="text-xl font-medium mb-6 flex items-center gap-2">
                        <Plus className="w-5 h-5" />
                        Generate New API Key
                    </h2>

                    <div className="flex gap-4">
                        <input
                            type="text"
                            placeholder="Key Name (e.g. Production Agent)"
                            value={newKeyName}
                            onChange={(e) => setNewKeyName(e.target.value)}
                            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-white/30 transition-colors"
                        />
                        <button
                            onClick={() => createMutation.mutate(newKeyName)}
                            disabled={!newKeyName || createMutation.isPending}
                            className="bg-white text-black px-6 py-3 rounded-xl font-medium hover:bg-white/90 transition-colors disabled:opacity-50"
                        >
                            {createMutation.isPending ? 'Generating...' : 'Generate'}
                        </button>
                    </div>

                    {createdKey && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            className="mt-6 bg-green-500/10 border border-green-500/20 rounded-xl p-4"
                        >
                            <p className="text-green-400 text-sm mb-2 font-medium">
                                Key Generated! Copy it now, you won't see it again.
                            </p>
                            <div className="flex items-center justify-between bg-black/20 rounded-lg px-4 py-3">
                                <code className="font-mono text-green-300">{createdKey}</code>
                                <button
                                    onClick={handleCopy}
                                    className="text-green-400 hover:text-green-300 transition-colors"
                                >
                                    {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                                </button>
                            </div>
                        </motion.div>
                    )}
                </div>

                {/* Keys List */}
                <div className="space-y-4">
                    <h2 className="text-xl font-medium mb-4">Active Keys</h2>
                    {isLoading ? (
                        <div className="h-20 bg-white/5 rounded-2xl animate-pulse" />
                    ) : (
                        keys?.map((key) => (
                            <div
                                key={key.keyId}
                                className={`bg-white/5 border border-white/10 rounded-2xl p-6 flex items-center justify-between ${key.revoked ? 'opacity-50' : ''}`}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="bg-white/10 p-3 rounded-xl">
                                        <Key className="w-5 h-5 text-white/80" />
                                    </div>
                                    <div>
                                        <h3 className="font-medium">{key.name}</h3>
                                        <p className="text-xs text-white/40 font-mono mt-1">
                                            Created: {new Date(key.createdAt).toLocaleDateString()}
                                            {key.revoked && <span className="text-red-400 ml-2">(Revoked)</span>}
                                        </p>
                                    </div>
                                </div>

                                {!key.revoked && (
                                    <button
                                        onClick={() => revokeMutation.mutate(key.keyId)}
                                        className="p-2 hover:bg-red-500/20 rounded-lg text-white/40 hover:text-red-400 transition-colors"
                                        title="Revoke Key"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
