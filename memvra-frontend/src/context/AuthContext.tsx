import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface AuthContextType {
    token: string | null;
    isAuthenticated: boolean;
    login: (token: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        // Check if user is authenticated - non-blocking
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const response = await fetch('/v1/dashboard/keys', {
                credentials: 'include'
            });
            if (response.ok) {
                setToken('authenticated');
            }
        } catch (error) {
            // Silently fail - backend not available or user not authenticated
            console.log('Not authenticated or backend unavailable');
        }
    };

    const login = (newToken: string) => {
        setToken(newToken);
    };

    const logout = async () => {
        try {
            await fetch('/v1/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });
        } catch (e) {
            console.error('Logout failed', e);
        }
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
