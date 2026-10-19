import React, { useState } from 'react';
import { Search, Eye, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import type { EvidenceItemScrubbed, EvidenceItemRevealed } from '../types';
import { api } from '../services/api';

interface EvidenceListProps {
  sessionId: string;
  scenarioId: string;
  availableEvidence: EvidenceItemScrubbed[];
  revealedEvidenceMap: Record<string, EvidenceItemRevealed>;
  onEvidenceRevealed: (revealed: EvidenceItemRevealed) => void;
  disabled?: boolean;
}

export const EvidenceList: React.FC<EvidenceListProps> = ({
  sessionId,
  scenarioId,
  availableEvidence,
  revealedEvidenceMap,
  onEvidenceRevealed,
  disabled = false,
}) => {
  const [openingId, setOpeningId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleOpenEvidence = async (item: EvidenceItemScrubbed) => {
    if (disabled || revealedEvidenceMap[item.id] || openingId === item.id) {
      return;
    }

    setOpeningId(item.id);
    setError(null);

    try {
      const res = await api.logEvent(sessionId, {
        scenario_id: scenarioId,
        event_type: 'open_evidence',
        payload: { evidence_id: item.id },
      });

      if (res.revealed_evidence) {
        onEvidenceRevealed(res.revealed_evidence);
      } else {
        onEvidenceRevealed({
          id: item.id,
          label: item.label,
          value: 'Evidence inspected successfully.',
        });
      }
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to inspect evidence item.'
      );
    } finally {
      setOpeningId(null);
    }
  };

  if (!availableEvidence || availableEvidence.length === 0) {
    return null;
  }

  return (
    <div className="card" style={{ padding: '1.25rem' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          marginBottom: '0.875rem',
        }}
      >
        <Search size={18} color="var(--color-primary)" />
        <h3 style={{ fontSize: '0.9375rem', fontWeight: 600 }}>
          Inspectable Evidence Clues
        </h3>
        <span
          style={{
            fontSize: '0.75rem',
            color: 'var(--color-text-muted)',
          }}
        >
          (Optional independent investigation)
        </span>
      </div>

      {error && (
        <div
          className="alert alert-error"
          style={{
            padding: '0.5rem 0.75rem',
            fontSize: '0.8125rem',
          }}
        >
          <AlertCircle size={14} /> {error}
        </div>
      )}

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem',
        }}
      >
        {availableEvidence.map((item) => {
          const revealed = revealedEvidenceMap[item.id];
          const isOpening = openingId === item.id;

          return (
            <div
              key={item.id}
              style={{
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                padding: '0.875rem 1rem',
                backgroundColor: revealed ? '#f8fafc' : '#ffffff',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem',
                transition: 'all 0.15s ease',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }}
              >
                <div
                  style={{
                    fontSize: '0.875rem',
                    fontWeight: 500,
                    color: 'var(--color-text)',
                  }}
                >
                  {item.label}
                </div>

                {revealed ? (
                  <span
                    className="badge badge-neutral"
                    style={{ fontSize: '0.75rem' }}
                  >
                    <CheckCircle2
                      size={12}
                      color="var(--color-primary)"
                    />{' '}
                    Inspected
                  </span>
                ) : (
                  <button
                    type="button"
                    onClick={() => handleOpenEvidence(item)}
                    className="btn btn-outline"
                    style={{
                      padding: '0.3rem 0.75rem',
                      fontSize: '0.8125rem',
                    }}
                    disabled={disabled || isOpening}
                  >
                    {isOpening ? (
                      <>
                        <Loader2 size={14} className="spin" /> Inspecting...
                      </>
                    ) : (
                      <>
                        <Eye size={14} /> Open evidence
                      </>
                    )}
                  </button>
                )}
              </div>

              {revealed && (
                <div
                  style={{
                    padding: '0.625rem 0.875rem',
                    backgroundColor: '#ffffff',
                    border: '1px solid #cbd5e1',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.8125rem',
                    fontFamily: 'monospace',
                    color: 'var(--color-text-secondary)',
                    wordBreak: 'break-all',
                  }}
                >
                  {revealed.value}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};