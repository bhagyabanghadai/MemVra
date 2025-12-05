import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import VerificationPortal from './pages/VerificationPortal';
import FactExplorer from './pages/FactExplorer';
import RecordFact from './pages/RecordFact';

import { AuthProvider } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import Dashboard from './pages/Dashboard';
import ProfilePage from './pages/ProfilePage';
import ProtectedRoute from './components/ProtectedRoute';
import ChatWithBrain from './pages/ChatWithBrain';
import FloatingChatWidget from './components/FloatingChatWidget';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <div className="min-h-screen bg-background text-foreground font-sans antialiased selection:bg-cyan-500/30">
            <Navbar />
            <main>
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/verify" element={<VerificationPortal />} />
                <Route path="/explore" element={<FactExplorer />} />
                <Route path="/record" element={<RecordFact />} />

                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/chat" element={<ChatWithBrain />} />

                <Route element={<ProtectedRoute />}>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/profile" element={<ProfilePage />} />
                </Route>
              </Routes>
            </main>

            {/* Floating Chat Widget - Available on all pages */}
            <FloatingChatWidget />
          </div>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
