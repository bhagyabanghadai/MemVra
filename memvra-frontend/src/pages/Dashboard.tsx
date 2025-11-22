import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getApiKeys, createApiKey, revokeApiKey } from '../lib/api';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { Key, Plus, Trash2, Copy, Check } from 'lucide-react';

export default function Dashboard() {
    const { logout } = useAuth();
    const queryClient = useQueryClient();
    const [newKeyName, setNewKeyName] = useState('');
    const [createdKey, setCreatedKey] = useState<string | null>(null);
    const [copied, setCopied] = useState(false);

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

    const handleCopy = () => {
        if (createdKey) {
            navigator.clipboard.writeText(createdKey);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    return (
        <div className="min-h-screen bg-background pt-24 px-6 pb-12">
            <div className="max-w-4xl mx-auto">
                <div className="flex items-end justify-between mb-12">
                    <div>
                        <h1 className="text-4xl font-serif mb-2">Developer Dashboard</h1>
                        <p className="text-white/60">Manage your API keys and integration settings.</p>
                    </div>
                    <button
                        onClick={logout}
                        className="text-sm text-white/40 hover:text-white transition-colors"
                    >
                        Sign Out
                    </button>
                </div>

                {/* Create Key Section */}
                <div className="bg-white/5 border border-white/10 rounded-3xl p-8 mb-8">
                    <h2 className="text-xl font-medium mb-6 flex items-center gap-2">
                        <Plus className="w-5 h-5" />
                        Generate New Key
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
