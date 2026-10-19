import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { AuthScreen } from './components/AuthScreen';
import { ConsentScreen } from './components/ConsentScreen';
import { OnboardingScreen } from './components/OnboardingScreen';
import { StudyShell } from './components/StudyShell';
import type { User, AuthResponse } from './types';
import { api, getAuthToken } from './services/api';
import { Loader2 } from 'lucide-react';

type AppStep = 'auth' | 'consent' | 'onboarding' | 'study';

export function App() {
  const [step, setStep] = useState<AppStep>('auth');
  const [user, setUser] = useState<User | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(localStorage.getItem('cyberpsyche_session_id'));
  const [initializing, setInitializing] = useState(true);

  useEffect(() => {
    const token = getAuthToken();
    if (token) {
      const savedSessionId = localStorage.getItem('cyberpsyche_session_id');
      if (savedSessionId) {
        setSessionId(savedSessionId);
        setStep('study');
      } else {
        setStep('consent');
      }
    }
    setInitializing(false);
  }, []);

  const handleAuthSuccess = (authData: AuthResponse) => {
    setUser(authData.user);
    setStep('consent');
  };

  const handleConsentSuccess = () => {
    setStep('onboarding');
  };

  const handleOnboardingSuccess = async () => {
    try {
      const sessionRes = await api.startSession('targeted', 'Form_A');
      setSessionId(sessionRes.session_id);
      localStorage.setItem('cyberpsyche_session_id', sessionRes.session_id);
      setStep('study');
    } catch (err: any) {
      alert(`Failed to create session: ${err.message}`);
    }
  };

  const handleLogout = async () => {
    await api.logout();
    setUser(null);
    setSessionId(null);
    localStorage.removeItem('cyberpsyche_session_id');
    setStep('auth');
  };

  const handleRestartStudy = () => {
    setSessionId(null);
    localStorage.removeItem('cyberpsyche_session_id');
    setStep('consent');
  };

  if (initializing) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <Loader2 size={36} className="spin" color="var(--color-primary)" />
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: 'var(--color-bg)' }}>
      <Navbar user={user} onLogout={handleLogout} />

      <main style={{ flex: 1, paddingBottom: '3rem' }}>
        {step === 'auth' && <AuthScreen onSuccess={handleAuthSuccess} />}
        {step === 'consent' && <ConsentScreen onSuccess={handleConsentSuccess} />}
        {step === 'onboarding' && <OnboardingScreen onSuccess={handleOnboardingSuccess} />}
        {step === 'study' && sessionId && (
          <StudyShell sessionId={sessionId} onRestart={handleRestartStudy} onLogout={handleLogout} />
        )}
      </main>

      <footer style={{
        backgroundColor: '#ffffff',
        borderTop: '1px solid var(--color-border)',
        padding: '1rem',
        textAlign: 'center',
        fontSize: '0.75rem',
        color: 'var(--color-text-muted)'
      }}>
        CyberPsyche Laboratory &copy; 2026 — Decision-Process Laboratory for Social-Engineering Resilience
      </footer>
    </div>
  );
}

export default App;
