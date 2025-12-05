import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { User, Brain, MessageCircle, TrendingUp, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

// Add profile fetching to api.ts
const getUserProfile = async (userId: string = 'default') => {
    const response = await fetch(`/logical/profile/${userId}`);
    return response.json();
};

export default function ProfilePage() {
    const { data: profile, isLoading } = useQuery({
        queryKey: ['userProfile'],
        queryFn: () => getUserProfile('default')
    });

    if (isLoading) {
        return (
            <div className="min-h-screen bg-background pt-24 px-6 pb-12">
                <div className="max-w-4xl mx-auto">
                    <div className="h-64 bg-white/5 rounded-3xl animate-pulse" />
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-4xl mx-auto">
                <div className="flex items-center justify-between mb-12">
                    <div>
                        <h1 className="text-4xl font-serif mb-2">Your Profile</h1>
                        <p className="text-white/60">How the brain adapts to you.</p>
                    </div>
                    <Link
                        to="/dashboard"
                        className="text-sm text-white/60 hover:text-white transition-colors"
                    >
                        ← Back to Dashboard
                    </Link>
                </div>

                {/* Profile Summary */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-white/10 rounded-3xl p-8 mb-8"
                >
                    <div className="flex items-center gap-4 mb-6">
                        <div className="bg-white/10 p-4 rounded-2xl">
                            <User className="w-8 h-8 text-cyan-400" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-serif">User Profile</h2>
                            <p className="text-white/60">ID: {profile?.user_id || 'default'}</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white/5 rounded-2xl p-6">
                            <div className="flex items-center gap-2 mb-2">
                                <MessageCircle className="w-4 h-4 text-white/60" />
                                <span className="text-sm text-white/60">Total Queries</span>
                            </div>
                            <p className="text-3xl font-bold">{profile?.summary?.total_queries || 0}</p>
                        </div>

                        <div className="bg-white/5 rounded-2xl p-6">
                            <div className="flex items-center gap-2 mb-2">
                                <Brain className="w-4 h-4 text-white/60" />
                                <span className="text-sm text-white/60">Total Facts</span>
                            </div>
                            <p className="text-3xl font-bold">{profile?.summary?.total_facts || 0}</p>
                        </div>

                        <div className="bg-white/5 rounded-2xl p-6">
                            <div className="flex items-center gap-2 mb-2">
                                <TrendingUp className="w-4 h-4 text-white/60" />
                                <span className="text-sm text-white/60">Patterns Found</span>
                            </div>
                            <p className="text-3xl font-bold">{profile?.summary?.total_patterns || 0}</p>
                        </div>
                    </div>
                </motion.div>

                {/* Linguistic Profile */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="bg-white/5 border border-white/10 rounded-3xl p-8 mb-8"
                >
                    <h2 className="text-xl font-medium mb-6 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-purple-400" />
                        Linguistic Adaptation
                    </h2>

                    <div className="space-y-6">
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm text-white/60">Formality Level</span>
                                <span className="text-sm font-medium">{((profile?.linguistic_profile?.formality || 0.5) * 100).toFixed(0)}%</span>
                            </div>
                            <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-gradient-to-r from-purple-400 to-pink-400"
                                    style={{ width: `${(profile?.linguistic_profile?.formality || 0.5) * 100}%` }}
                                />
                            </div>
                            <p className="text-xs text-white/40 mt-1">
                                {(profile?.linguistic_profile?.formality || 0.5) > 0.6 ? 'Prefers professional tone' : 'Prefers casual tone'}
                            </p>
                        </div>

                        {profile?.linguistic_profile?.vocabulary_complexity !== undefined && (
                            <div>
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm text-white/60">Vocabulary Complexity</span>
                                    <span className="text-sm font-medium">{((profile?.linguistic_profile?.vocabulary_complexity || 0.5) * 100).toFixed(0)}%</span>
                                </div>
                                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-cyan-400 to-blue-400"
                                        style={{ width: `${(profile?.linguistic_profile?.vocabulary_complexity || 0.5) * 100}%` }}
                                    />
                                </div>
                            </div>
                        )}
                    </div>
                </motion.div>

                {/* Query Style */}
                {profile?.query_style && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="bg-white/5 border border-white/10 rounded-3xl p-8 mb-8"
                    >
                        <h2 className="text-xl font-medium mb-6">Query Style</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {Object.entries(profile.query_style).map(([key, value]) => (
                                <div key={key} className="bg-white/5 rounded-xl p-4">
                                    <p className="text-sm text-white/60 capitalize mb-1">{key.replace(/_/g, ' ')}</p>
                                    <p className="font-medium">{String(value)}</p>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                )}

                {/* Personality Traits */}
                {profile?.personality_traits && Object.keys(profile.personality_traits).length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        className="bg-white/5 border border-white/10 rounded-3xl p-8"
                    >
                        <h2 className="text-xl font-medium mb-6">Personality Traits</h2>
                        <div className="flex flex-wrap gap-3">
                            {Object.entries(profile.personality_traits).map(([trait, score]) => (
                                <div
                                    key={trait}
                                    className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-full px-4 py-2"
                                >
                                    <span className="text-sm capitalize">{trait}: {typeof score === 'number' ? score.toFixed(2) : score}</span>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    );
}
