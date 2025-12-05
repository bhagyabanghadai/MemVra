import { motion } from 'framer-motion';
// @ts-ignore
import { Database, Lock, Zap, Globe, Search, Shield } from 'lucide-react';
import { cn } from '../lib/utils';

const features = [
    {
        title: "Immutable Ledger",
        desc: "Once written, facts cannot be altered. Secured by SHA-256 cryptography.",
        icon: Lock,
        className: "md:col-span-2",
        gradient: "from-cyan-500/20 to-blue-500/20"
    },
    {
        title: "Global Search",
        desc: "Instantly query the truth across millions of records.",
        icon: Search,
        className: "md:col-span-1",
        gradient: "from-purple-500/20 to-pink-500/20"
    },
    {
        title: "Real-time Verification",
        desc: "< 50ms latency for signature checks.",
        icon: Zap,
        className: "md:col-span-1",
        gradient: "from-yellow-500/20 to-orange-500/20"
    },
    {
        title: "Agent Consensus",
        desc: "A unified protocol for autonomous agents to agree on reality.",
        icon: Globe,
        className: "md:col-span-2",
        gradient: "from-green-500/20 to-emerald-500/20"
    },
];

export default function BentoGrid() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-6xl mx-auto px-6">
            {features.map((feature, i) => (
                <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.1 }}
                    className={cn(
                        "group relative overflow-hidden rounded-3xl border border-white/10 bg-black/50 backdrop-blur-sm p-8 hover:border-white/20 transition-colors",
                        feature.className
                    )}
                >
                    <div className={cn(
                        "absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-500",
                        feature.gradient
                    )} />

                    <div className="relative z-10 h-full flex flex-col justify-between">
                        <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6">
                            <feature.icon className="w-6 h-6 text-white" />
                        </div>

                        <div>
                            <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                            <p className="text-gray-400">{feature.desc}</p>
                        </div>
                    </div>
                </motion.div>
            ))}
        </div>
    );
}
