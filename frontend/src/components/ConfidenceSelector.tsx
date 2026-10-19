import React from 'react';
import { Gauge } from 'lucide-react';

interface ConfidenceSelectorProps {
  confidence: number;
  onChangeConfidence: (value: number) => void;
}

export const ConfidenceSelector: React.FC<ConfidenceSelectorProps> = ({
  confidence,
  onChangeConfidence,
}) => {
  return (
    <div className="card" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.875rem' }}>
        <Gauge size={18} color="var(--color-primary)" />
        <h3 style={{ fontSize: '0.9375rem', fontWeight: 600 }}>Decision Confidence Level</h3>
        <span style={{ fontSize: '0.75rem', color: '#dc2626' }}>* Required</span>
      </div>

      <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)', marginBottom: '0.875rem' }}>
        How confident are you in your selected action choice?
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.5rem' }}>
        {[1, 2, 3, 4, 5].map((val) => {
          const isSelected = confidence === val;
          return (
            <button
              key={val}
              type="button"
              onClick={() => onChangeConfidence(val)}
              style={{
                padding: '0.75rem 0.5rem',
                borderRadius: 'var(--radius-md)',
                border: isSelected ? '2px solid var(--color-primary)' : '1px solid var(--color-border)',
                backgroundColor: isSelected ? 'var(--color-primary-light)' : '#ffffff',
                color: isSelected ? 'var(--color-primary)' : 'var(--color-text)',
                fontWeight: isSelected ? 700 : 500,
                fontSize: '1rem',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '0.25rem',
                transition: 'all 0.15s ease'
              }}
            >
              <span>{val}</span>
              <span style={{ fontSize: '0.6875rem', fontWeight: 400, color: 'var(--color-text-muted)' }}>
                {val === 1 && 'Not confident'}
                {val === 3 && 'Moderate'}
                {val === 5 && 'Very confident'}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
