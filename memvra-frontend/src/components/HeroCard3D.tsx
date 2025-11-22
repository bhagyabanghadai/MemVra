import { useRef } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { ShieldCheck, Fingerprint, Activity } from 'lucide-react';

export default function HeroCard3D() {
    const ref = useRef<HTMLDivElement>(null);

    const x = useMotionValue(0);
    const y = useMotionValue(0);

    const mouseX = useSpring(x, { stiffness: 150, damping: 15 });
    const mouseY = useSpring(y, { stiffness: 150, damping: 15 });

    const rotateX = useTransform(mouseY, [-0.5, 0.5], ["10deg", "-10deg"]);
    const rotateY = useTransform(mouseX, [-0.5, 0.5], ["-10deg", "10deg"]);
    const glareX = useTransform(mouseX, [-0.5, 0.5], ["0%", "100%"]);
    const glareY = useTransform(mouseY, [-0.5, 0.5], ["0%", "100%"]);

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        const rect = ref.current?.getBoundingClientRect();
        if (rect) {
            const width = rect.width;
            const height = rect.height;
            const mouseXVal = e.clientX - rect.left;
            const mouseYVal = e.clientY - rect.top;
            const xPct = mouseXVal / width - 0.5;
            const yPct = mouseYVal / height - 0.5;
            x.set(xPct);
            y.set(yPct);
        }
    };

    const handleMouseLeave = () => {
        x.set(0);
        y.set(0);
    };

    return (
        <motion.div
            ref={ref}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={{
                rotateX,
                rotateY,
                transformStyle: "preserve-3d",
            }}
            className="relative w-full max-w-[400px] aspect-[3/4] mx-auto perspective-1000 cursor-pointer"
        >
            {/* The Physical Card */}
            <motion.div
                style={{ transform: "translateZ(0px)", transformStyle: "preserve-3d" }}
                className="absolute inset-0 rounded-[30px] bg-gradient-to-br from-gray-900 to-black border border-white/10 shadow-2xl overflow-hidden"
            >
                {/* Glare Effect */}
                <motion.div
                    style={{
                        background: `radial-gradient(circle at ${glareX} ${glareY}, rgba(255,255,255,0.1) 0%, transparent 80%)`
                    }}
                    className="absolute inset-0 z-50 pointer-events-none"
                />

                {/* Card Content Layer 1 (Background) */}
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10" />

                {/* Floating Elements */}
                <motion.div
                    style={{ transform: "translateZ(30px)" }}
                    className="absolute top-8 left-8 right-8 flex items-center justify-between"
                >
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center border border-cyan-500/30">
                            <ShieldCheck className="w-4 h-4 text-cyan-400" />
                        </div>
                        <span className="text-sm font-medium text-gray-300">Verified Fact</span>
                    </div>
                    <div className="px-2 py-1 rounded-full bg-green-500/10 border border-green-500/20 text-[10px] font-bold text-green-400 uppercase tracking-wider">
                        Live
                    </div>
                </motion.div>

                <motion.div
                    style={{ transform: "translateZ(50px)" }}
                    className="absolute top-24 left-8 right-8"
                >
                    <h3 className="text-2xl font-bold text-white leading-tight mb-2">
                        "The sky is blue."
                    </h3>
                    <p className="text-sm text-gray-500 font-mono">ID: mv-8f4...b21</p>
                </motion.div>

                <motion.div
                    style={{ transform: "translateZ(40px)" }}
                    className="absolute bottom-8 left-8 right-8"
                >
                    <div className="flex items-center gap-4 mb-6">
                        <div className="flex-1 h-1 bg-gray-800 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: "0%" }}
                                animate={{ width: "100%" }}
                                transition={{ duration: 2, repeat: Infinity }}
                                className="h-full bg-cyan-500"
                            />
                        </div>
                        <div className="text-xs text-cyan-400 font-mono">VERIFYING</div>
                    </div>

                    <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-blue-500/20 text-blue-400">
                                <Fingerprint className="w-5 h-5" />
                            </div>
                            <div>
                                <div className="text-xs text-gray-400">Signer</div>
                                <div className="text-sm font-medium text-white">Agent-007</div>
                            </div>
                        </div>
                        <Activity className="w-5 h-5 text-gray-600" />
                    </div>
                </motion.div>

            </motion.div>
        </motion.div>
    );
}
