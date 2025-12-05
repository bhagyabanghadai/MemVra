import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
// @ts-ignore
import { Brain, Sparkles, Loader2 } from 'lucide-react';
import { recallFromBrain, triggerDreamCycle, getBrainStatus, searchFacts } from '../lib/api';

export default function BrainExplorer() {
    const [query, setQuery] = useState('');

    // Get brain status
    const { data: brainStatus } = useQuery({
        queryKey: ['brainStatus'],
        queryFn: getBrainStatus
    });

    // Recall mutation
    const recallMutation = useMutation({
        mutationFn: (searchQuery: string) => recallFromBrain(searchQuery)
    });

    // Dream cycle mutation
    const dreamMutation = useMutation({
        mutationFn: async () => {
            // Fetch recent facts from your database
            const recentFacts = await searchFacts({ size: 10 });

            // Transform to brain format
            const factsForBrain = recentFacts.content.map(fact => ({
                content: fact.content,
                fact_id: fact.fact_id,
                created_at: fact.created_at
            }));

            // Send to brain for consolidation
            return triggerDreamCycle(factsForBrain);
        }
    });

    const handleRecall = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            recallMutation.mutate(query);
        }
    };

    const handleDreamCycle = () => {
        dreamMutation.mutate();
    };

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-4xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-12"
                >
                    <h1 className="text-4xl font-serif mb-4">Brain Explorer</h1>
                    <p className="text-white/60 text-lg">
                        Interact with the bicameral AI brain for memory recall and pattern detection.
                    </p>
                </motion.div>

                {/* Brain Status */}
                {brainStatus && (
                    <div className="mb-8 p-6 bg-white/5 border border-white/10 rounded-2xl">
                        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <Brain className="w-6 h-6" />
                            Brain Status
                        </h3>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <span className="text-white/60">Status:</span>
                                <span className="ml-2 text-green-400">{brainStatus.status}</span>
                            </div>
                            <div>
                                <span className="text-white/60">Logical Brain:</span>
                                <span className="ml-2">{brainStatus.logicalBrain}</span>
                            </div>
                            <div className="col-span-2">
                                <span className="text-white/60">Intuitive Brain:</span>
                                <span className="ml-2">{brainStatus.intuitiveBrain}</span>
                            </div>
                        </div>
                    </div>
                )}

                {/* Logical Recall */}
                <div className="mb-8">
                    <h2 className="text-2xl font-semibold mb-4">Logical Recall</h2>
                    <form onSubmit={handleRecall} className="space-y-4">
                        <div className="flex gap-4">
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="Search memories..."
                                className="flex-1 bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder:text-white/20 focus:outline-none focus:border-white/30 transition-colors"
                            />
                            <button
                                type="submit"
                                disabled={recallMutation.isPending || !query.trim()}
                                className="px-6 py-4 bg-cyan-500 text-black rounded-xl font-medium hover:bg-cyan-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                {recallMutation.isPending ? (
                                    <>
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        Searching...
                                    </>
                                ) : (
                                    <>
                                        <Brain className="w-5 h-5" />
                                        Recall
                                    </>
                                )}
                            </button>
                        </div>
                    </form>

                    {/* Recall Results */}
                    {recallMutation.data && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="mt-6 p-6 bg-cyan-500/10 border border-cyan-500/20 rounded-2xl"
                        >
                            <h3 className="text-lg font-semibold mb-2 text-cyan-400">Results</h3>
                            <p className="text-white/80 mb-4">{recallMutation.data.result}</p>

                            {recallMutation.data.matches && recallMutation.data.matches.length > 0 && (
                                <div className="space-y-3">
                                    <p className="text-white/60 text-sm">Found {recallMutation.data.matches.length} match(es):</p>
                                    {recallMutation.data.matches.map((match, idx) => (
                                        <div key={idx} className="p-4 bg-white/5 rounded-xl border border-white/10">
                                            <div className="flex justify-between items-start mb-2">
                                                <span className="text-xs text-white/40">{match.fact_id}</span>
                                                <span className={`text-xs px-2 py-1 rounded ${match.relevance === 'exact' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                                                    }`}>
                                                    {match.relevance}
                                                </span>
                                            </div>
                                            <p className="text-white">{match.content}</p>
                                            <p className="text-xs text-white/40 mt-2">{new Date(match.created_at).toLocaleString()}</p>
                                        </div>
                                    ))}
                                </div>
                            )}

                            {recallMutation.data.suggestion && (
                                <p className="mt-4 text-sm text-white/60 italic">{recallMutation.data.suggestion}</p>
                            )}
                        </motion.div>
                    )}
                </div>

                {/* Dream Cycle */}
                <div>
                    <h2 className="text-2xl font-semibold mb-4">Intuitive Dream Cycle</h2>
                    <p className="text-white/60 mb-4">
                        Consolidate recent memories and detect patterns using the intuitive brain.
                    </p>

                    <button
                        onClick={handleDreamCycle}
                        disabled={dreamMutation.isPending}
                        className="px-6 py-4 bg-purple-500 text-white rounded-xl font-medium hover:bg-purple-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        {dreamMutation.isPending ? (
                            <>
                                <Loader2 className="w-5 h-5 animate-spin" />
                                Dreaming...
                            </>
                        ) : (
                            <>
                                <Sparkles className="w-5 h-5" />
                                Trigger Dream Cycle
                            </>
                        )}
                    </button>

                    {/* Dream Results */}
                    {dreamMutation.data && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="mt-6 p-6 bg-purple-500/10 border border-purple-500/20 rounded-2xl"
                        >
                            <h3 className="text-lg font-semibold mb-4 text-purple-400">Dream Insights</h3>

                            <div className="space-y-4">
                                <div>
                                    <p className="text-sm text-white/60 mb-1">Summary</p>
                                    <p className="text-white">{dreamMutation.data.summary}</p>
                                </div>

                                <div>
                                    <p className="text-sm text-white/60 mb-2">Detected Patterns</p>
                                    <div className="space-y-2">
                                        {dreamMutation.data.patterns.map((pattern, idx) => (
                                            <div key={idx} className="flex items-start gap-2">
                                                <span className="text-purple-400">•</span>
                                                <span className="text-white/80">{pattern}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-sm text-white/60 mb-1">Sentiment</p>
                                        <p className="text-white capitalize">{dreamMutation.data.sentiment.replace('-', ' ')}</p>
                                    </div>
                                    {dreamMutation.data.consolidated_memories && (
                                        <div>
                                            <p className="text-sm text-white/60 mb-1">Memories Processed</p>
                                            <p className="text-white">{dreamMutation.data.consolidated_memories}</p>
                                        </div>
                                    )}
                                </div>

                                {dreamMutation.data.key_insights && dreamMutation.data.key_insights.length > 0 && (
                                    <div>
                                        <p className="text-sm text-white/60 mb-2">Key Insights</p>
                                        <div className="space-y-1">
                                            {dreamMutation.data.key_insights.map((insight, idx) => (
                                                <p key={idx} className="text-white/80 text-sm">→ {insight}</p>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    )}

                    {dreamMutation.isError && (
                        <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
                            Error: {(dreamMutation.error as any)?.message || 'Failed to trigger dream cycle'}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
