import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
// @ts-ignore
import { PenTool, Save, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { recordFact } from '../lib/api';
import { Link } from 'react-router-dom';

export default function RecordFact() {
    const [formData, setFormData] = useState({
        content: '',
        source_type: 'user_input',
        source_id: '',
        recorded_by: ''
    });

    const mutation = useMutation({
        mutationFn: recordFact
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        mutation.mutate(formData);
    };

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-2xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-12"
                >
                    <h1 className="text-4xl font-serif mb-4">Record Truth</h1>
                    <p className="text-white/60 text-lg">
                        Permanently record a verified fact to the immutable ledger.
                    </p>
                </motion.div>

                {mutation.isSuccess ? (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-green-500/10 border border-green-500/20 rounded-3xl p-8 text-center"
                    >
                        <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                            <CheckCircle2 className="w-8 h-8 text-green-500" />
                        </div>
                        <h2 className="text-2xl font-serif mb-4 text-green-400">Fact Recorded Successfully</h2>
                        <p className="text-white/60 mb-8">
                            Your fact has been cryptographically signed and stored.
                        </p>
                        <div className="flex gap-4 justify-center">
                            <Link
                                to={`/verify?id=${mutation.data.fact_id}`}
                                className="px-6 py-3 bg-white text-black rounded-full font-medium hover:bg-gray-200 transition-colors"
                            >
                                Verify Now
                            </Link>
                            <button
                                onClick={() => mutation.reset()}
                                className="px-6 py-3 bg-white/10 text-white rounded-full font-medium hover:bg-white/20 transition-colors"
                            >
                                Record Another
                            </button>
                        </div>
                    </motion.div>
                ) : (
                    <motion.form
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        onSubmit={handleSubmit}
                        className="space-y-6"
                    >
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-white/60">Content</label>
                            <textarea
                                required
                                value={formData.content}
                                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                                className="w-full h-32 bg-white/5 border border-white/10 rounded-2xl p-4 text-white placeholder:text-white/20 focus:outline-none focus:border-white/30 transition-colors resize-none"
                                placeholder="Enter the fact content..."
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-white/60">Source Type</label>
                                <select
                                    value={formData.source_type}
                                    onChange={(e) => setFormData({ ...formData, source_type: e.target.value })}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:border-white/30 transition-colors"
                                >
                                    <option value="user_input" className="bg-black">User Input</option>
                                    <option value="api_response" className="bg-black">API Response</option>
                                    <option value="agent_inference" className="bg-black">Agent Inference</option>
                                </select>
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium text-white/60">Source ID</label>
                                <input
                                    type="text"
                                    required
                                    value={formData.source_id}
                                    onChange={(e) => setFormData({ ...formData, source_id: e.target.value })}
                                    className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder:text-white/20 focus:outline-none focus:border-white/30 transition-colors"
                                    placeholder="e.g., manual-entry-001"
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-white/60">Recorded By (Agent ID)</label>
                            <input
                                type="text"
                                required
                                value={formData.recorded_by}
                                onChange={(e) => setFormData({ ...formData, recorded_by: e.target.value })}
                                className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder:text-white/20 focus:outline-none focus:border-white/30 transition-colors"
                                placeholder="e.g., agent-alpha"
                            />
                        </div>

                        {mutation.isError && (
                            <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 flex items-center gap-3 text-red-400">
                                <AlertCircle className="w-5 h-5" />
                                <span>{(mutation.error as any).response?.data?.message || "Failed to record fact"}</span>
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={mutation.isPending}
                            className="w-full bg-white text-black rounded-full py-4 font-medium hover:bg-gray-200 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {mutation.isPending ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    Signing & Recording...
                                </>
                            ) : (
                                <>
                                    <Save className="w-5 h-5" />
                                    Record Fact
                                </>
                            )}
                        </button>
                    </motion.form>
                )}
            </div>
        </div>
    );
}
