import React from 'react';
import { MousePointerClick } from 'lucide-react';

interface ActionSelectorProps {
  availableActions: string[];
  selectedAction: string | null;
  onSelectAction: (action: string) => void;
}

const ACTION_DESCRIPTIONS: Record<string, { label: string; description: string }> = {
  PROCEED: {
    label: 'Proceed / Click Link / Open Attachment',
    description: 'Follow instructions or open attachments directly in the communication.'
  },
  IGNORE: {
    label: 'Ignore / Delete Message',
    description: 'Take no action and discard the message without responding.'
  },
  REPLY_TO_SENDER: {
    label: 'Reply to Sender Directly',
    description: 'Respond using the email address or message contact provided.'
  },
  VERIFY_INDEPENDENTLY: {
    label: 'Verify Independently Out-of-Band',
    description: 'Check official portal, call known phone number, or visit website directly.'
  },
  REPORT: {
    label: 'Report to IT / Security / Platform',
    description: 'Submit message to organizational security team or abuse reporting.'
  },
  ASK_TRUSTED_PERSON: {
    label: 'Consult Supervisor / Trusted Colleague',
    description: 'Seek second opinion from a supervisor, peer, or family member.'
  },
  GATHER_MORE_EVIDENCE: {
    label: 'Gather Additional Evidence First',
    description: 'Inspect message headers, sender history, or metadata before deciding.'
  },
  UNSURE: {
    label: 'Unsure / Cannot Determine',
    description: 'Uncertain about message authenticity or appropriate next step.'
  }
};

export const ActionSelector: React.FC<ActionSelectorProps> = ({
  availableActions,
  selectedAction,
  onSelectAction,
}) => {
  const actionsToDisplay = availableActions && availableActions.length > 0
    ? availableActions
    : Object.keys(ACTION_DESCRIPTIONS);

  return (
    <div className="card" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.875rem' }}>
        <MousePointerClick size={18} color="var(--color-primary)" />
        <h3 style={{ fontSize: '0.9375rem', fontWeight: 600 }}>Select Response Action</h3>
        <span style={{ fontSize: '0.75rem', color: '#dc2626' }}>* Required</span>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
        gap: '0.75rem'
      }}>
        {actionsToDisplay.map((actKey) => {
          const info = ACTION_DESCRIPTIONS[actKey] || { label: actKey, description: '' };
          const isSelected = selectedAction === actKey;

          return (
            <button
              key={actKey}
              type="button"
              onClick={() => onSelectAction(actKey)}
              style={{
                textAlign: 'left',
                padding: '0.875rem 1rem',
                borderRadius: 'var(--radius-md)',
                border: isSelected ? '2px solid var(--color-primary)' : '1px solid var(--color-border)',
                backgroundColor: isSelected ? 'var(--color-primary-light)' : '#ffffff',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.25rem'
              }}
            >
              <div style={{
                fontSize: '0.875rem',
                fontWeight: 600,
                color: isSelected ? 'var(--color-primary)' : 'var(--color-text)'
              }}>
                {info.label}
              </div>
              {info.description && (
                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', lineHeight: 1.35 }}>
                  {info.description}
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
