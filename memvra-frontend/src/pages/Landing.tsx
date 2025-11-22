import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Play, ShieldCheck, Github, Twitter, Linkedin } from 'lucide-react';
import CrystalScene from '../components/CrystalScene';
import TrustedBy from '../components/TrustedBy';

export default function Landing() {
    return (
        <div className="relative min-h-screen bg-background text-foreground font-sans selection:bg-white/20 overflow-x-hidden">

            {/* 3D Background */}
            <div className="fixed inset-0 z-0">
                <CrystalScene />
            </div>

            {/* Content Layer */}
            <main className="relative z-10">

                {/* HERO */}
                <section className="min-h-screen flex flex-col items-center justify-center px-6 text-center pt-20 relative">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, delay: 0.5 }}
                        className="max-w-4xl mx-auto"
                    >
                        <h1 className="font-serif text-6xl md:text-9xl font-medium tracking-tight mb-8 mix-blend-difference">
                            Truth, <br />
                            <span className="italic text-white/80">Verified.</span>
                        </h1>

                        <p className="text-xl md:text-2xl text-white/60 max-w-2xl mx-auto mb-12 font-light leading-relaxed">
                            The definitive ledger for autonomous intelligence. <br />
                            Secure. Immutable. Eternal.
                        </p>

                        <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-16">
                            <Link
                                to="/verify"
                                className="group px-8 py-4 bg-white text-black rounded-full font-medium hover:bg-gray-200 transition-all flex items-center gap-2"
                            >
                                Start Verification <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <button className="px-8 py-4 text-white border border-white/20 rounded-full hover:bg-white/5 transition-all flex items-center gap-3 backdrop-blur-sm">
                                <div className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center">
                                    <Play className="w-3 h-3 fill-current" />
                                </div>
                                Watch the Film
                            </button>
                        </div>

                        {/* Trusted By Section */}
                        <div className="flex justify-center">
                            <TrustedBy />
                        </div>
                    </motion.div>
                </section>

                {/* SCROLLYTELLING SECTION */}
                <section className="min-h-[300vh] relative bg-black/80 backdrop-blur-xl border-t border-white/10">
                    <div className="sticky top-0 h-screen flex items-center overflow-hidden pointer-events-none">
                        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />
                        <div className="flex whitespace-nowrap">
                            <h2 className="text-[20vw] font-serif opacity-5 animate-marquee select-none pr-12">
                                IMMUTABLE • SECURE • GLOBAL •
                            </h2>
                            <h2 className="text-[20vw] font-serif opacity-5 animate-marquee select-none pr-12">
                                IMMUTABLE • SECURE • GLOBAL •
                            </h2>
                        </div>
                    </div>

                    <div className="relative z-10 max-w-7xl mx-auto px-6 py-32 space-y-64">
                        {[
                            { title: "The Problem", desc: "AI hallucinations are polluting the digital ecosystem. We need a source of truth." },
                            { title: "The Solution", desc: "A cryptographic chain of custody for every generated token." },
                            { title: "The Future", desc: "A world where autonomous agents can trust each other implicitly." }
                        ].map((item, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 50 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.8 }}
                                className="max-w-2xl p-12 border-l border-white/20 bg-black/50 backdrop-blur-md"
                            >
                                <span className="text-sm font-mono text-white/40 mb-4 block">0{i + 1}</span>
                                <h3 className="text-5xl font-serif mb-6">{item.title}</h3>
                                <p className="text-2xl text-white/60 font-light leading-relaxed">{item.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </section>

                {/* FOOTER */}
                <footer className="bg-black border-t border-white/10 pt-24 pb-12 px-6">
                    <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 mb-24">
                        <div className="col-span-1 md:col-span-1">
                            <div className="flex items-center gap-2 mb-6">
                                <ShieldCheck className="w-6 h-6 text-white" />
                                <span className="text-xl font-serif font-medium">MemVra</span>
                            </div>
                            <p className="text-white/40 leading-relaxed">
                                The trust layer for the autonomous web. <br />
                                San Francisco, CA.
                            </p>
                        </div>

                        <div>
                            <h4 className="font-medium mb-6">Product</h4>
                            <ul className="space-y-4 text-white/60">
                                <li><Link to="/verify" className="hover:text-white transition-colors">Verification</Link></li>
                                <li><Link to="/explore" className="hover:text-white transition-colors">Explorer</Link></li>
                                <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-medium mb-6">Company</h4>
                            <ul className="space-y-4 text-white/60">
                                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-medium mb-6">Legal</h4>
                            <ul className="space-y-4 text-white/60">
                                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                            </ul>
                        </div>
                    </div>

                    <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between pt-8 border-t border-white/10 text-white/40 text-sm">
                        <p>&copy; 2025 MemVra Inc. All rights reserved.</p>
                        <div className="flex gap-6 mt-4 md:mt-0">
                            <Github className="w-5 h-5 hover:text-white cursor-pointer transition-colors" />
                            <Twitter className="w-5 h-5 hover:text-white cursor-pointer transition-colors" />
                            <Linkedin className="w-5 h-5 hover:text-white cursor-pointer transition-colors" />
                        </div>
                    </div>
                </footer>

            </main>
        </div>
    );
}
