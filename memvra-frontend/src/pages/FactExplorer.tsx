import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Search, Calendar, User, Database } from 'lucide-react';
import { searchFacts } from '../lib/api';
import { Link } from 'react-router-dom';

export default function FactExplorer() {
    const [searchTerm, setSearchTerm] = useState('');
    const [filters, setFilters] = useState({ sourceId: '', sourceType: '' });
    const [dateRange, setDateRange] = useState<{ from?: string; to?: string }>({});

    const [page, setPage] = useState(0);
    const pageSize = 9;

    const { data: factsPage, isLoading } = useQuery({
        queryKey: ['facts', searchTerm, filters, dateRange, page],
        queryFn: () => searchFacts({
            recorded_by: searchTerm || undefined,
            source_id: filters.sourceId || undefined,
            source_type: filters.sourceType || undefined,
            from_date: dateRange.from,
            to_date: dateRange.to,
            page,
            size: pageSize
        })
    });

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-7xl mx-auto">
                {/* ... (Header and Filters remain same) ... */}
                <div className="flex flex-col md:flex-row items-end justify-between mb-12 gap-6">
                    <div>
                        <h1 className="text-4xl md:text-5xl font-serif mb-4">Global Ledger</h1>
                        <p className="text-white/60 text-lg max-w-xl">
                            Explore the immutable history of verified autonomous interactions.
                        </p>
                    </div>

                    <div className="flex flex-col gap-4 w-full md:w-auto">
                        <div className="flex flex-wrap items-center gap-4">
                            <div className="relative flex-1 min-w-[200px]">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
                                <input
                                    type="text"
                                    placeholder="Filter by Agent ID..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="w-full bg-white/5 border border-white/10 rounded-full py-3 pl-10 pr-4 text-sm focus:outline-none focus:border-white/30 transition-colors"
                                />
                            </div>
                            <div className="relative flex-1 min-w-[200px]">
                                <Database className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
                                <input
                                    type="text"
                                    placeholder="Filter by Source ID..."
                                    value={filters.sourceId}
                                    onChange={(e) => setFilters({ ...filters, sourceId: e.target.value })}
                                    className="w-full bg-white/5 border border-white/10 rounded-full py-3 pl-10 pr-4 text-sm focus:outline-none focus:border-white/30 transition-colors"
                                />
                            </div>
                            <select
                                value={filters.sourceType}
                                onChange={(e) => setFilters({ ...filters, sourceType: e.target.value })}
                                className="bg-white/5 border border-white/10 rounded-full py-3 px-6 text-sm text-white/80 focus:outline-none focus:border-white/30 transition-colors appearance-none cursor-pointer hover:bg-white/10"
                            >
                                <option value="" className="bg-black">All Sources</option>
                                <option value="user_input" className="bg-black">User Input</option>
                                <option value="api_response" className="bg-black">API Response</option>
                                <option value="agent_inference" className="bg-black">Agent Inference</option>
                            </select>
                        </div>

                        {/* Time Travel Controls */}
                        <div className="flex items-center gap-2 bg-white/5 p-2 rounded-2xl border border-white/5">
                            <div className="flex items-center gap-2 px-3">
                                <Calendar className="w-4 h-4 text-cyan-400" />
                                <span className="text-xs font-medium text-cyan-400 uppercase tracking-wider">Time Travel</span>
                            </div>
                            <div className="h-8 w-px bg-white/10" />
                            <input
                                type="date"
                                className="bg-transparent text-white text-sm focus:outline-none [&::-webkit-calendar-picker-indicator]:invert [&::-webkit-calendar-picker-indicator]:opacity-50 hover:[&::-webkit-calendar-picker-indicator]:opacity-100"
                                onChange={(e) => setDateRange(prev => ({ ...prev, from: e.target.value ? new Date(e.target.value).toISOString() : undefined }))}
                            />
                            <span className="text-white/40 text-sm">to</span>
                            <input
                                type="date"
                                className="bg-transparent text-white text-sm focus:outline-none [&::-webkit-calendar-picker-indicator]:invert [&::-webkit-calendar-picker-indicator]:opacity-50 hover:[&::-webkit-calendar-picker-indicator]:opacity-100"
                                onChange={(e) => setDateRange(prev => ({ ...prev, to: e.target.value ? new Date(e.target.value).toISOString() : undefined }))}
                            />
                        </div>
                    </div>
                </div>

                {isLoading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[1, 2, 3, 4, 5, 6].map((i) => (
                            <div key={i} className="h-64 bg-white/5 rounded-3xl animate-pulse" />
                        ))}
                    </div>
                ) : (
                    <>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                            {factsPage?.content.map((fact, i) => (
                                <motion.div
                                    key={fact.fact_id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.05 }}
                                >
                                    <Link
                                        to={`/verify?id=${fact.fact_id}`}
                                        className="block group h-full bg-white/5 border border-white/10 rounded-3xl p-8 hover:bg-white/10 transition-all duration-300 hover:-translate-y-1"
                                    >
                                        <div className="flex items-start justify-between mb-6">
                                            <div className="bg-white/10 p-3 rounded-2xl">
                                                <Database className="w-6 h-6 text-white/80" />
                                            </div>
                                            <span className={`text-xs font-medium px-3 py-1 rounded-full ${fact.revoked ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                                                {fact.revoked ? 'REVOKED' : 'VERIFIED'}
                                            </span>
                                        </div>

                                        <p className="text-white/80 font-serif text-lg mb-8 line-clamp-3">
                                            "{fact.content}"
                                        </p>

                                        <div className="space-y-3 text-sm text-white/40">
                                            <div className="flex items-center gap-2">
                                                <User className="w-4 h-4" />
                                                <span className="font-mono truncate">{fact.recorded_by}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Calendar className="w-4 h-4" />
                                                <span>{new Date(fact.created_at).toLocaleDateString()}</span>
                                            </div>
                                        </div>
                                    </Link>
                                </motion.div>
                            ))}
                        </div>

                        {/* Pagination Controls */}
                        <div className="flex justify-center items-center gap-4">
                            <button
                                onClick={() => setPage(p => Math.max(0, p - 1))}
                                disabled={page === 0}
                                className="px-4 py-2 bg-white/5 rounded-lg disabled:opacity-50 hover:bg-white/10 transition-colors"
                            >
                                Previous
                            </button>
                            <span className="text-white/60">
                                Page {page + 1} of {factsPage?.totalPages || 1}
                            </span>
                            <button
                                onClick={() => setPage(p => Math.min((factsPage?.totalPages || 1) - 1, p + 1))}
                                disabled={page >= (factsPage?.totalPages || 1) - 1}
                                className="px-4 py-2 bg-white/5 rounded-lg disabled:opacity-50 hover:bg-white/10 transition-colors"
                            >
                                Next
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
