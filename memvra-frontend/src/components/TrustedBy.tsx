import { motion } from 'framer-motion';

const avatars = [
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Aneka",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Mark",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Sasha"
];

export default function TrustedBy() {
    return (
        <div className="flex flex-col items-center justify-center py-12 gap-6">
            <p className="text-sm text-gray-500 uppercase tracking-widest font-medium">Trusted by Next-Gen Agents</p>
            <div className="flex items-center -space-x-4">
                {avatars.map((src, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="w-12 h-12 rounded-full border-2 border-black bg-gray-800 overflow-hidden relative z-10 hover:z-20 hover:scale-110 transition-transform"
                    >
                        <img src={src} alt="Avatar" className="w-full h-full object-cover" />
                    </motion.div>
                ))}
                <div className="w-12 h-12 rounded-full border-2 border-black bg-gray-900 flex items-center justify-center text-xs font-bold text-gray-400 relative z-0">
                    +2k
                </div>
            </div>
        </div>
    );
}
