import { useRef, useState } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';

export default function Hero3D() {
    const ref = useRef<HTMLDivElement>(null);

    const x = useMotionValue(0);
    const y = useMotionValue(0);

    const mouseX = useSpring(x, { stiffness: 150, damping: 15 });
    const mouseY = useSpring(y, { stiffness: 150, damping: 15 });

    const rotateX = useTransform(mouseY, [-0.5, 0.5], ["15deg", "-15deg"]);
    const rotateY = useTransform(mouseX, [-0.5, 0.5], ["-15deg", "15deg"]);

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
            className="relative w-full max-w-md aspect-square mx-auto perspective-1000 cursor-pointer"
        >
            {/* Core Cube/Shield Representation */}
            <motion.div
                style={{ transform: "translateZ(50px)", transformStyle: "preserve-3d" }}
                className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-3xl border border-white/10 backdrop-blur-md shadow-[0_0_50px_rgba(6,182,212,0.3)]"
            >
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 rounded-3xl" />

                {/* Inner Floating Elements */}
                <motion.div
                    style={{ transform: "translateZ(80px)" }}
                    className="absolute inset-0 flex items-center justify-center"
                >
                    <div className="relative w-32 h-32">
                        <div className="absolute inset-0 border-4 border-cyan-400 rounded-full animate-[spin_10s_linear_infinite]" />
                        <div className="absolute inset-2 border-4 border-blue-500 rounded-full animate-[spin_15s_linear_infinite_reverse]" />
                        <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-16 h-16 bg-cyan-500 rounded-full blur-md animate-pulse" />
                        </div>
                    </div>
                </motion.div>

                <motion.div
                    style={{ transform: "translateZ(40px)" }}
                    className="absolute bottom-8 left-8 right-8 text-center"
                >
                    <div className="text-xs font-mono text-cyan-300 mb-1">HASH: 8f4...b21</div>
                    <div className="h-1 w-full bg-cyan-900/50 rounded-full overflow-hidden">
                        <div className="h-full bg-cyan-400 w-2/3 animate-pulse" />
                    </div>
                </motion.div>
            </motion.div>
        </motion.div>
    );
}
