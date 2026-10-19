import React from 'react';
import { Mail, Paperclip, User } from 'lucide-react';
import type { ScenarioMessage } from '../types';

interface EmailScenarioProps {
  narrative: string;
  message: ScenarioMessage;
  persona: string;
  context: string;
}

export const EmailScenario: React.FC<EmailScenarioProps> = ({ narrative, message, persona, context }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Context Narrative Card */}
      <div style={{
        backgroundColor: '#f8fafc',
        borderLeft: '4px solid var(--color-primary)',
        padding: '0.875rem 1.125rem',
        borderRadius: '0 var(--radius-md) var(--radius-md) 0',
        fontSize: '0.875rem',
        lineHeight: 1.5,
        color: 'var(--color-text-secondary)'
      }}>
        <strong style={{ color: 'var(--color-primary)', fontSize: '0.8125rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Scenario Context
        </strong>
        <p style={{ marginTop: '0.25rem' }}>{narrative}</p>
      </div>

      {/* Realistic Simulated Email Client Container */}
      <div style={{
        backgroundColor: '#ffffff',
        border: '1px solid #cbd5e1',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
        overflow: 'hidden'
      }}>
        {/* Email Client Header */}
        <div style={{
          backgroundColor: '#f1f5f9',
          padding: '0.75rem 1.25rem',
          borderBottom: '1px solid #e2e8f0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#475569', fontSize: '0.8125rem', fontWeight: 600 }}>
            <Mail size={16} color="var(--color-primary)" /> Simulated Email Client
          </div>
          <span style={{ fontSize: '0.75rem', color: '#64748b', backgroundColor: '#ffffff', padding: '0.2rem 0.5rem', borderRadius: '4px', border: '1px solid #cbd5e1' }}>
            Context: {context}
          </span>
        </div>

        {/* Email Headers */}
        <div style={{ padding: '1.25rem', borderBottom: '1px solid #f1f5f9', display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '2.5rem',
              height: '2.5rem',
              borderRadius: '50%',
              backgroundColor: '#e2e8f0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#475569',
              fontWeight: 600,
              fontSize: '1rem'
            }}>
              <User size={20} />
            </div>
            <div>
              <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: 'var(--color-text)' }}>
                {message.sender_display || 'Sender'}
              </div>
              {persona && (
                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                  Recipient Persona: {persona}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Email Body */}
        <div style={{
          padding: '1.5rem 1.25rem',
          fontSize: '0.9375rem',
          lineHeight: 1.65,
          color: '#1e293b',
          whiteSpace: 'pre-wrap',
          minHeight: '120px'
        }}>
          {message.body}
        </div>

        {/* Attachment Card if present */}
        {message.attachment && (
          <div style={{
            margin: '0 1.25rem 1.25rem',
            padding: '0.75rem 1rem',
            backgroundColor: '#f8fafc',
            border: '1px solid #cbd5e1',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem'
          }}>
            <Paperclip size={18} color="var(--color-primary)" />
            <div style={{ fontSize: '0.875rem' }}>
              <span style={{ fontWeight: 500, color: 'var(--color-text)' }}>Attached Document: </span>
              <span style={{ color: 'var(--color-primary)', textDecoration: 'underline', fontFamily: 'monospace' }}>
                {message.attachment}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
