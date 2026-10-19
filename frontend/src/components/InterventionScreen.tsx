import React, { useEffect, useState } from 'react';
import { BookOpen, CheckCircle2, Loader2, AlertCircle, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import type { InterventionContentResponse } from '../types';

interface InterventionScreenProps {
  sessionId: string;
  onComplete: () => void;
}

export const InterventionScreen: React.FC<InterventionScreenProps> = ({ sessionId, onComplete }) => {
  const [data, setData] = useState<InterventionContentResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    const fetchIntervention = async () => {
      try {
        const res = await api.getIntervention(sessionId);
        if (isMounted) setData(res);
      } catch (err: any) {
        if (isMounted) setError(err.message || 'Failed to load educational intervention content.');
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchIntervention();
    return () => { isMounted = false; };
  }, [sessionId]);

  const handleFinish = async () => {
    setSubmitting(true);
    setError(null);
    try {
      await api.completeIntervention(sessionId, 100);
      onComplete();
    } catch (err: any) {
      setError(err.message || 'Failed to complete intervention phase.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 1rem' }}>
        <Loader2 size={32} className="spin" color="var(--color-primary)" style={{ margin: '0 auto 1rem' }} />
        <p style={{ color: 'var(--color-text-muted)' }}>Loading educational module...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="card" style={{ maxWidth: '600px', margin: '2rem auto' }}>
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <div>{error || 'Unable to display intervention content.'}</div>
        </div>
        <button onClick={() => window.location.reload()} className="btn btn-secondary">
          Retry Loading
        </button>
      </div>
    );
  }

  const { content } = data;

  return (
    <div style={{ maxWidth: '720px', margin: '2rem auto 0', width: '100%' }}>
      <div className="card">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          paddingBottom: '1.25rem',
          borderBottom: '1px solid var(--color-border)',
          marginBottom: '1.5rem'
        }}>
          <div style={{
            width: '3rem',
            height: '3rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: 'var(--color-primary-light)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-primary)',
            border: '1px solid var(--color-primary-border)'
          }}>
            <BookOpen size={26} />
          </div>
          <div>
            <span className="badge badge-yellow" style={{ marginBottom: '0.25rem' }}>
              Educational Briefing
            </span>
            <h2 style={{ fontSize: '1.375rem', color: 'var(--color-primary)' }}>
              {content.title}
            </h2>
          </div>
        </div>

        <div style={{ fontSize: '0.9375rem', lineHeight: 1.7, color: 'var(--color-text-secondary)', marginBottom: '1.75rem' }}>
          <p style={{ marginBottom: '1.25rem' }}>{content.body}</p>

          {content.exercises && content.exercises.length > 0 && (
            <div style={{
              backgroundColor: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: 'var(--radius-md)',
              padding: '1.25rem'
            }}>
              <h4 style={{ color: 'var(--color-text)', fontSize: '0.875rem', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                Key Practice Takeaway
              </h4>
              <ul style={{ paddingLeft: '1.25rem', margin: 0 }}>
                {content.exercises.map((ex, i) => (
                  <li key={i} style={{ marginBottom: '0.375rem', fontSize: '0.875rem' }}>
                    {ex}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <button
          onClick={handleFinish}
          className="btn btn-primary"
          style={{ width: '100%', padding: '0.875rem', fontSize: '0.9375rem' }}
          disabled={submitting}
        >
          {submitting ? 'Completing Module...' : (
            <>
              <CheckCircle2 size={18} /> Complete Briefing & Continue to Retest Phase <ArrowRight size={18} />
            </>
          )}
        </button>
      </div>
    </div>
  );
};
