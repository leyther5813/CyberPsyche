import React, { useEffect, useState } from 'react';
import { Award, ShieldCheck, Loader2, AlertCircle, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import type { ResilienceProfileResponse } from '../types';

interface ProfileDebriefScreenProps {
  sessionId: string;
  onRestart: () => void;
}

export const ProfileDebriefScreen: React.FC<ProfileDebriefScreenProps> = ({ sessionId, onRestart }) => {
  const [data, setData] = useState<ResilienceProfileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    const fetchProfile = async () => {
      try {
        const res = await api.getProfile(sessionId);
        if (isMounted) setData(res);
      } catch (err: any) {
        if (isMounted) setError(err.message || 'Failed to load resilience profile.');
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchProfile();
    return () => { isMounted = false; };
  }, [sessionId]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 1rem' }}>
        <Loader2 size={32} className="spin" color="var(--color-primary)" style={{ margin: '0 auto 1rem' }} />
        <p style={{ color: 'var(--color-text-muted)' }}>Calculating research resilience profile metrics...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="card" style={{ maxWidth: '600px', margin: '2rem auto' }}>
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <div>{error || 'Unable to display profile summary.'}</div>
        </div>
        <button onClick={() => window.location.reload()} className="btn btn-secondary">
          Retry Loading
        </button>
      </div>
    );
  }

  const { profile } = data;
  const phases = ['baseline', 'retest', 'transfer'];

  return (
    <div style={{ maxWidth: '800px', margin: '2rem auto 0', width: '100%' }}>
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.875rem',
          paddingBottom: '1.25rem',
          borderBottom: '1px solid var(--color-border)',
          marginBottom: '1.5rem'
        }}>
          <div style={{
            width: '3.25rem',
            height: '3.25rem',
            borderRadius: '50%',
            backgroundColor: 'var(--color-primary-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-primary)',
            border: '1px solid var(--color-primary-border)'
          }}>
            <Award size={28} />
          </div>
          <div>
            <span className="badge badge-blue" style={{ marginBottom: '0.25rem' }}>
              Study Completed
            </span>
            <h2 style={{ fontSize: '1.375rem', color: 'var(--color-primary)' }}>
              Social-Engineering Resilience Profile
            </h2>
          </div>
        </div>

        {/* Behavioral Metrics Matrix */}
        <h3 style={{ fontSize: '1rem', marginBottom: '1rem' }}>Behavioral Research Dimensions Across Study Phases</h3>

        <div style={{ overflowX: 'auto', marginBottom: '1.75rem' }}>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            fontSize: '0.875rem',
            textAlign: 'left'
          }}>
            <thead>
              <tr style={{ backgroundColor: '#f8fafc', borderBottom: '2px solid var(--color-border)' }}>
                <th style={{ padding: '0.75rem 1rem', color: 'var(--color-text)' }}>Research Dimension</th>
                {phases.map(ph => (
                  <th key={ph} style={{ padding: '0.75rem 1rem', textTransform: 'capitalize', color: 'var(--color-primary)' }}>
                    {ph} Phase
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid var(--color-border)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>Scenarios Evaluated</td>
                {phases.map(ph => (
                  <td key={ph} style={{ padding: '0.75rem 1rem' }}>{profile[ph]?.count ?? 0}</td>
                ))}
              </tr>
              <tr style={{ borderBottom: '1px solid var(--color-border)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>Decision Quality Mean</td>
                {phases.map(ph => (
                  <td key={ph} style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>
                    {profile[ph] ? `${(profile[ph].decision_quality_mean * 100).toFixed(1)}%` : 'N/A'}
                  </td>
                ))}
              </tr>
              <tr style={{ borderBottom: '1px solid var(--color-border)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>Out-of-Band Verification Rate</td>
                {phases.map(ph => (
                  <td key={ph} style={{ padding: '0.75rem 1rem' }}>
                    {profile[ph] ? `${(profile[ph].verification_rate * 100).toFixed(1)}%` : 'N/A'}
                  </td>
                ))}
              </tr>
              <tr style={{ borderBottom: '1px solid var(--color-border)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>Under-Caution Occurrences</td>
                {phases.map(ph => (
                  <td key={ph} style={{ padding: '0.75rem 1rem' }}>{profile[ph]?.under_caution_count ?? 0}</td>
                ))}
              </tr>
              <tr style={{ borderBottom: '1px solid var(--color-border)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>Over-Caution Occurrences</td>
                {phases.map(ph => (
                  <td key={ph} style={{ padding: '0.75rem 1rem' }}>{profile[ph]?.over_caution_count ?? 0}</td>
                ))}
              </tr>
              <tr>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>Evidence Inspection Depth</td>
                {phases.map(ph => (
                  <td key={ph} style={{ padding: '0.75rem 1rem' }}>
                    {profile[ph] ? `${(profile[ph].evidence_depth_mean * 100).toFixed(1)}%` : 'N/A'}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>

        {/* Debrief Notice */}
        <div style={{
          backgroundColor: '#eff6ff',
          border: '1px solid #bfdbfe',
          borderRadius: 'var(--radius-md)',
          padding: '1.25rem',
          marginBottom: '1.5rem',
          fontSize: '0.875rem',
          lineHeight: 1.6
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: 'var(--color-primary)' }}>
            <ShieldCheck size={20} />
            <h4 style={{ fontWeight: 600 }}>Research Debrief Statement</h4>
          </div>
          <p style={{ marginBottom: '0.75rem' }}>
            Thank you for participating in the CyberPsyche Decision-Process Laboratory study.
          </p>
          <ul style={{ paddingLeft: '1.25rem', margin: 0, color: 'var(--color-text-secondary)' }}>
            <li style={{ marginBottom: '0.375rem' }}>
              All communications presented throughout the study were fully synthetic, safe simulations designed to assess decision-making under social-engineering mechanisms (authority, urgency, and reward pressure).
            </li>
            <li style={{ marginBottom: '0.375rem' }}>
              No real accounts, credentials, or personal messages were used or collected.
            </li>
            <li>
              Your contributions provide valuable empirical insights into human-behaviour resilience and out-of-band verification strategies.
            </li>
          </ul>
        </div>

        <button
          onClick={onRestart}
          className="btn btn-outline"
          style={{ width: '100%', padding: '0.75rem' }}
        >
          <RefreshCw size={16} /> Start New Study Session
        </button>
      </div>
    </div>
  );
};
