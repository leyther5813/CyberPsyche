import React from 'react';
import { Shield, Sun, LogOut } from 'lucide-react';
import type { User } from '../types';

interface NavbarProps {
  user: User | null;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ user, onLogout }) => {
  return (
    <header style={{
      backgroundColor: '#ffffff',
      borderBottom: '1px solid var(--color-border)',
      boxShadow: 'var(--shadow-sm)',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div className="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingTop: '0.875rem',
        paddingBottom: '0.875rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            width: '2.5rem',
            height: '2.5rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: 'var(--color-primary-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-primary)',
            border: '1px solid var(--color-primary-border)'
          }}>
            <Shield size={22} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <h1 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--color-primary)', letterSpacing: '-0.01em' }}>
                CyberPsyche
              </h1>
              <span className="badge badge-yellow" style={{ fontSize: '0.6875rem' }}>
                <Sun size={12} /> LAB
              </span>
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', margin: 0 }}>
              Social-Engineering Resilience Decision Laboratory
            </p>
          </div>
        </div>

        {user && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)', textAlign: 'right' }}>
              <span style={{ fontWeight: 500, color: 'var(--color-text)' }}>Participant</span>
              <div style={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                {user.email_hash.substring(0, 10)}...
              </div>
            </div>
            <button
              onClick={onLogout}
              className="btn btn-outline"
              style={{ padding: '0.4rem 0.75rem', fontSize: '0.8125rem' }}
              title="Sign Out"
            >
              <LogOut size={16} /> Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
