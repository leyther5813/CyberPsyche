import React from 'react';
import { MessageSquare, Paperclip, User } from 'lucide-react';
import type { ScenarioMessage } from '../types';

interface ChatScenarioProps {
  narrative: string;
  message: ScenarioMessage;
  persona?: string;
  context: string;
}

export const ChatScenario: React.FC<ChatScenarioProps> = ({ narrative, message, persona, context }) => {
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
        {persona && (
          <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '0.25rem' }}>
            Recipient Persona: {persona}
          </div>
        )}
      </div>

      {/* Realistic Simulated Chat Container */}
      <div style={{
        backgroundColor: '#ffffff',
        border: '1px solid #cbd5e1',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-sm)',
        maxWidth: '560px',
        margin: '0 auto',
        width: '100%',
        overflow: 'hidden'
      }}>
        {/* Chat Window Top Bar */}
        <div style={{
          backgroundColor: 'var(--color-primary)',
          color: '#ffffff',
          padding: '0.75rem 1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          <div style={{
            width: '2.25rem',
            height: '2.25rem',
            borderRadius: '50%',
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <User size={18} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontSize: '0.9375rem', fontWeight: 600 }}>
              {message.sender_display || 'Sender'}
            </div>
            <div style={{ fontSize: '0.75rem', opacity: 0.85, display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
              <MessageSquare size={12} /> Instant Messaging ({context})
            </div>
          </div>
        </div>

        {/* Messaging Area */}
        <div style={{
          padding: '1.25rem',
          backgroundColor: '#f8fafc',
          minHeight: '180px',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {/* Incoming Message Bubble */}
          <div style={{
            alignSelf: 'flex-start',
            maxWidth: '85%',
            backgroundColor: '#ffffff',
            border: '1px solid #e2e8f0',
            borderRadius: '1rem 1rem 1rem 0.125rem',
            padding: '0.875rem 1.125rem',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
            fontSize: '0.9375rem',
            lineHeight: 1.5,
            color: '#1e293b',
            whiteSpace: 'pre-wrap'
          }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-primary)', marginBottom: '0.25rem' }}>
              {message.sender_display}
            </div>
            {message.body}

            {/* Attached media/link card if present */}
            {message.attachment && (
              <div style={{
                marginTop: '0.75rem',
                padding: '0.625rem 0.75rem',
                backgroundColor: '#eff6ff',
                border: '1px solid #bfdbfe',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                fontSize: '0.8125rem'
              }}>
                <Paperclip size={14} color="var(--color-primary)" />
                <span style={{ fontWeight: 500, color: 'var(--color-primary)', wordBreak: 'break-all' }}>
                  {message.attachment}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
