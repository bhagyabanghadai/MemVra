import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, Search, AlertCircle, CheckCircle2, Clock, FileText, Hash } from 'lucide-react';
import { getFact } from '../lib/api';
import { useSearchParams } from 'react-router-dom';

export default function VerificationPortal() {
    const [searchParams] = useSearchParams();
    const [searchId, setSearchId] = useState(searchParams.get('id') || '');
    const [queryId, setQueryId] = useState(searchParams.get('id') || '');

    useEffect(() => {
        const id = searchParams.get('id');
        if (id) {
            setSearchId(id);
            setQueryId(id);
        }
    }, [searchParams]);

    const { data: fact, isLoading, error } = useQuery({
        queryKey: ['fact', queryId],
        queryFn: () => getFact(queryId),
        enabled: !!queryId,
        retry: false
    });

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchId.trim()) {
            setQueryId(searchId.trim());
        }
    };

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-3xl mx-auto">

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-12"
                >
                    <h1 className="text-4xl md:text-5xl font-serif mb-4">Verify Truth</h1>
                    <p className="text-white/60 text-lg">
                        Cryptographically verify the authenticity and lineage of any MemVra record.
                    </p>
                </motion.div>

                <motion.form
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    onSubmit={handleSearch}
                    className="relative mb-16"
                >
                    <div className="relative group">
                        <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-white/5 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                        <input
                            type="text"
                            value={searchId}
                            onChange={(e) => setSearchId(e.target.value)}
                            placeholder="Enter Fact ID (UUID)"
                            className="relative z-10 w-full bg-black/50 border border-white/10 rounded-full py-4 pl-6 pr-16 text-lg focus:outline-none focus:border-white/30 focus:ring-1 focus:ring-white/30 transition-all placeholder:text-white/20"
                        />
                        <button
                            type="submit"
                            className="absolute right-2 top-2 bottom-2 z-20 px-6 bg-white text-black rounded-full font-medium hover:bg-gray-200 transition-colors flex items-center gap-2"
                        >
                            <Search className="w-4 h-4" />
                            <span className="hidden sm:inline">Verify</span>
                        </button>
                    </div>
                </motion.form>

                <AnimatePresence mode="wait">
                    {isLoading && (
                        <motion.div
                            key="loading"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col items-center justify-center py-12"
                        >
                            <div className="w-12 h-12 border-2 border-white/10 border-t-white rounded-full animate-spin mb-4" />
                            <p className="text-white/40 font-mono text-sm">VERIFYING SIGNATURE...</p>
                        </motion.div>
                    )}

                    {error && (
                        <motion.div
                            key="error"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 text-center"
                        >
                            <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                                <AlertCircle className="w-8 h-8 text-red-500" />
                            </div>
                            <h3 className="text-2xl font-serif mb-2 text-red-400">Verification Failed</h3>
                            <p className="text-white/60 mb-4">
                                The record ID could not be found or has been tampered with.
                            </p>
                            <p className="text-red-400/60 text-sm font-mono bg-black/20 p-2 rounded">
                                {(error as any).message || "Unknown error"}
                                {(error as any).response?.data?.message && ` - ${(error as any).response.data.message}`}
                            </p>
                        </motion.div>
                    )}

                    {fact && (
                        <motion.div
                            key="fact"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="bg-white/5 border border-white/10 rounded-3xl overflow-hidden backdrop-blur-sm"
                        >
                            {/* Header */}
                            <div className="bg-white/5 border-b border-white/5 p-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
                                <div className="flex items-center gap-4">
                                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${fact.revoked ? 'bg-red-500/20 text-red-500' : 'bg-green-500/20 text-green-500'}`}>
                                        {fact.revoked ? <AlertCircle className="w-6 h-6" /> : <CheckCircle2 className="w-6 h-6" />}
                                    </div>
                                    <div>
                                        <h2 className={`text-xl font-medium ${fact.revoked ? 'text-red-400' : 'text-green-400'}`}>
                                            {fact.revoked ? 'Revoked Record' : 'Verified Authentic'}
                                        </h2>
                                        <p className="text-white/40 text-sm font-mono mt-1">{fact.fact_id}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2 text-white/40 text-sm bg-black/20 px-4 py-2 rounded-full self-start md:self-auto">
                                    <Clock className="w-4 h-4" />
                                    {new Date(fact.created_at).toLocaleString()}
                                </div>
                            </div>

                            {/* Content */}
                            <div className="p-8 space-y-8">
                                <div>
                                    <label className="flex items-center gap-2 text-sm font-medium text-white/40 mb-3">
                                        <FileText className="w-4 h-4" /> RECORDED CONTENT
                                    </label>
                                    <div className="bg-black/30 rounded-xl p-6 font-serif text-xl leading-relaxed text-white/90 border border-white/5">
                                        "{fact.content}"
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div>
                                        <label className="flex items-center gap-2 text-sm font-medium text-white/40 mb-3">
                                            <Hash className="w-4 h-4" /> SOURCE METADATA
                                        </label>
                                        <div className="space-y-3">
                                            <div className="flex justify-between py-2 border-b border-white/5">
                                                <span className="text-white/60">Source Type</span>
                                                <span className="font-mono text-white/80">{fact.source_type}</span>
                                            </div>
                                            <div className="flex justify-between py-2 border-b border-white/5">
                                                <span className="text-white/60">Source ID</span>
                                                <span className="font-mono text-white/80">{fact.source_id}</span>
                                            </div>
                                            <div className="flex justify-between py-2 border-b border-white/5">
                                                <span className="text-white/60">Recorded By</span>
                                                <span className="font-mono text-white/80">{fact.recorded_by}</span>
                                            </div>
                                        </div>
                                    </div>

                                    <div>
                                        <label className="flex items-center gap-2 text-sm font-medium text-white/40 mb-3">
                                            <ShieldCheck className="w-4 h-4" /> CRYPTOGRAPHIC PROOF
                                        </label>
                                        <div className="bg-black/30 rounded-xl p-4 border border-white/5 mb-6">
                                            <p className="text-xs font-mono text-white/30 break-all leading-relaxed">
                                                {fact.signature}
                                            </p>
                                        </div>

                                        {!fact.revoked && (
                                            <div className="border-t border-white/5 pt-6">
                                                <h4 className="text-sm font-medium text-white/60 mb-3">Danger Zone</h4>
                                                <button
                                                    onClick={async () => {
                                                        const reason = prompt("Enter revocation reason:");
                                                        if (reason) {
                                                            try {
                                                                await import('../lib/api').then(m => m.revokeFact(fact.fact_id, reason));
                                                                window.location.reload();
                                                            } catch (e) {
                                                                alert("Failed to revoke fact");
                                                            }
                                                        }
                                                    }}
                                                    className="w-full py-3 border border-red-500/20 text-red-400 rounded-xl hover:bg-red-500/10 transition-colors text-sm font-medium flex items-center justify-center gap-2"
                                                >
                                                    <AlertCircle className="w-4 h-4" />
                                                    Revoke This Record
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

            </div>
        </div>
    );
}
