import React from 'react';
import { MessageSquare } from 'lucide-react';

interface ReasoningInputProps {
  selectedTags: string[];
  freeText: string;
  onToggleTag: (tag: string) => void;
  onFreeTextChange: (text: string) => void;
}

const REASON_TAG_OPTIONS = [
  'Sender identity or email domain appears unexpected',
  'Message creates urgent time pressure or threat',
  'Promises financial reward, voucher, or prize',
  'Requires verification on official institutional portal',
  'Content matches expected routine communication',
  'Insufficient evidence to take immediate action',
  'Followed standard organizational policy',
];

export const ReasoningInput: React.FC<ReasoningInputProps> = ({
  selectedTags,
  freeText,
  onToggleTag,
  onFreeTextChange,
}) => {
  return (
    <div className="card" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.875rem' }}>
        <MessageSquare size={18} color="var(--color-primary)" />
        <h3 style={{ fontSize: '0.9375rem', fontWeight: 600 }}>Decision Rationale & Reasoning</h3>
      </div>

      <div style={{ marginBottom: '1.25rem' }}>
        <label className="form-label" style={{ marginBottom: '0.5rem' }}>
          Select key factors that influenced your decision (optional tags):
        </label>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {REASON_TAG_OPTIONS.map((tag) => {
            const isSelected = selectedTags.includes(tag);
            return (
              <button
                key={tag}
                type="button"
                onClick={() => onToggleTag(tag)}
                style={{
                  padding: '0.375rem 0.75rem',
                  fontSize: '0.8125rem',
                  borderRadius: '9999px',
                  border: isSelected ? '1px solid var(--color-primary)' : '1px solid var(--color-border)',
                  backgroundColor: isSelected ? 'var(--color-primary-light)' : '#ffffff',
                  color: isSelected ? 'var(--color-primary)' : 'var(--color-text-secondary)',
                  fontWeight: isSelected ? 600 : 400,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {isSelected ? '✓ ' : '+ '} {tag}
              </button>
            );
          })}
        </div>
      </div>

      <div className="form-group" style={{ marginBottom: 0 }}>
        <label className="form-label" htmlFor="free-text-reasoning">
          What made you choose this action? (Brief free-text explanation)
        </label>
        <textarea
          id="free-text-reasoning"
          className="form-textarea"
          rows={3}
          placeholder="Describe why you took this action and what clues or considerations influenced you..."
          value={freeText}
          onChange={(e) => onFreeTextChange(e.target.value)}
        />
      </div>
    </div>
  );
};
