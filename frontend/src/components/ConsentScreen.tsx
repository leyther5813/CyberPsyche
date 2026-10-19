import React, { useState } from 'react';
import { FileCheck, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

interface ConsentScreenProps {
  onSuccess: () => void;
}

export const ConsentScreen: React.FC<ConsentScreenProps> = ({ onSuccess }) => {
  const [accepted, setAccepted] = useState(false);
  const [is18, setIs18] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!is18 || !accepted) {
      setError('You must confirm age eligibility (18+) and accept research terms to participate.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await api.acceptConsent('1.0', true);
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'Failed to submit consent. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '680px', margin: '2rem auto 0', width: '100%' }}>
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
          <div style={{
            width: '2.75rem',
            height: '2.75rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: 'var(--color-primary-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-primary)',
            border: '1px solid var(--color-primary-border)'
          }}>
            <FileCheck size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem' }}>Informed Research Consent</h2>
            <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
              CyberPsyche Decision-Process Laboratory for Social-Engineering Resilience
            </p>
          </div>
        </div>

        <div style={{
          backgroundColor: '#f8fafc',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-md)',
          padding: '1.25rem',
          fontSize: '0.875rem',
          lineHeight: 1.6,
          color: 'var(--color-text-secondary)',
          maxHeight: '320px',
          overflowY: 'auto',
          marginBottom: '1.5rem'
        }}>
          <h4 style={{ color: 'var(--color-text)', marginBottom: '0.5rem' }}>Study Overview & Guidelines</h4>
          <p style={{ marginBottom: '0.75rem' }}>
            You are invited to participate in a human-behaviour cybersecurity evaluation study. This study examines decision-making processes when evaluating digital communications under simulated organizational and social contexts.
          </p>

          <h4 style={{ color: 'var(--color-text)', margin: '1rem 0 0.5rem' }}>Key Participation Conditions</h4>
          <ul style={{ paddingLeft: '1.25rem', marginBottom: '0.75rem' }}>
            <li style={{ marginBottom: '0.375rem' }}>
              <strong>Simulated Scenarios:</strong> All communications (emails, chats, links, attachments) are safe, synthetic simulations created for research purposes.
            </li>
            <li style={{ marginBottom: '0.375rem' }}>
              <strong>Zero Credential Collection:</strong> Never enter real passwords, bank details, OTPs, or private personal messages during this study.
            </li>
            <li style={{ marginBottom: '0.375rem' }}>
              <strong>Voluntary Participation:</strong> Participation is voluntary. You may stop or withdraw at any point without penalty.
            </li>
            <li style={{ marginBottom: '0.375rem' }}>
              <strong>Data Confidentiality & Pseudonymity:</strong> Your responses, decision timing, and evidence inspection patterns are recorded under a pseudonymous identifier for research analysis only.
            </li>
            <li>
              <strong>Age Requirement:</strong> You must be 18 years of age or older to participate.
            </li>
          </ul>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <div>{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem', marginBottom: '1.5rem' }}>
            <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={is18}
                onChange={(e) => setIs18(e.target.checked)}
                style={{ marginTop: '0.2rem', width: '1.1rem', height: '1.1rem', accentColor: 'var(--color-primary)' }}
              />
              <span style={{ fontSize: '0.875rem', color: 'var(--color-text)' }}>
                I confirm that I am at least 18 years of age.
              </span>
            </label>

            <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={accepted}
                onChange={(e) => setAccepted(e.target.checked)}
                style={{ marginTop: '0.2rem', width: '1.1rem', height: '1.1rem', accentColor: 'var(--color-primary)' }}
              />
              <span style={{ fontSize: '0.875rem', color: 'var(--color-text)' }}>
                I have read the information above and voluntarily consent to participate in this study.
              </span>
            </label>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '0.75rem' }}
            disabled={loading || !is18 || !accepted}
          >
            {loading ? 'Submitting Consent...' : (
              <>
                <CheckCircle2 size={18} /> Accept Consent & Proceed
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
