import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, Search, Home, PenTool, LogIn, LayoutDashboard } from 'lucide-react';
import { cn } from '../lib/utils';

export default function Navbar() {
    const location = useLocation();
    const { isAuthenticated } = useAuth();

    const NavItem = ({ to, icon: Icon, label }: { to: string; icon: any; label: string }) => {
        const isActive = location.pathname === to;
        return (
            <Link
                to={to}
                className={cn(
                    "flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-300",
                    isActive
                        ? "bg-white text-black font-medium"
                        : "text-white/60 hover:text-white hover:bg-white/5"
                )}
            >
                <Icon className="w-4 h-4" />
                <span className="text-sm">{label}</span>
            </Link>
        );
    };

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-black/50 backdrop-blur-xl">
            <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
                <Link to="/" className="flex items-center gap-3 group">
                    <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center group-hover:scale-105 transition-transform">
                        <ShieldCheck className="w-5 h-5 text-black" />
                    </div>
                    <span className="text-xl font-serif font-medium tracking-tight text-white">
                        MemVra
                    </span>
                </Link>

                <div className="flex items-center gap-2">
                    <NavItem to="/" icon={Home} label="Home" />
                    <NavItem to="/verify" icon={ShieldCheck} label="Verify" />
                    <NavItem to="/explore" icon={Search} label="Explore" />
                    <NavItem to="/record" icon={PenTool} label="Record" />

                    <div className="w-px h-6 bg-white/10 mx-2" />

                    {isAuthenticated ? (
                        <NavItem to="/dashboard" icon={LayoutDashboard} label="Dashboard" />
                    ) : (
                        <NavItem to="/login" icon={LogIn} label="Login" />
                    )}
                </div>
            </div>
        </nav>
    );
}
