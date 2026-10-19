import React, { useState } from 'react';
import { UserCheck, AlertCircle, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import type { DigitalContextRequest } from '../types';

interface OnboardingScreenProps {
  onSuccess: () => void;
}

const LIFE_STAGES = [
  { id: 'student', label: 'Student / Trainee' },
  { id: 'early_career', label: 'Early Career (0–5 yrs)' },
  { id: 'mid_career', label: 'Mid Career (5–15 yrs)' },
  { id: 'senior', label: 'Senior Professional / Executive' },
  { id: 'other', label: 'Other' },
];

const DIGITAL_ACTIVITIES = [
  { id: 'email', label: 'Daily Work/Personal Email' },
  { id: 'online_banking', label: 'Online Financial/Banking Services' },
  { id: 'social_media', label: 'Social & Messaging Platforms' },
  { id: 'cloud_storage', label: 'Cloud Documents & File Sharing' },
  { id: 'remote_work', label: 'Remote Work Collaboration' },
  { id: 'online_shopping', label: 'Online E-commerce / Portals' },
];

const CYBER_LEVELS = [
  { id: 'novice', label: 'Novice (Basic computer user)' },
  { id: 'intermediate', label: 'Intermediate (Regular tech user, aware of basic risks)' },
  { id: 'advanced', label: 'Advanced (Tech professional or security-conscious)' },
];

const INTERESTS = ['Technology', 'Finance', 'Education', 'Gaming', 'Social', 'Career'];

export const OnboardingScreen: React.FC<OnboardingScreenProps> = ({ onSuccess }) => {
  const [lifeStage, setLifeStage] = useState('early_career');
  const [activities, setActivities] = useState<string[]>(['email', 'online_banking', 'social_media']);
  const [cyberLevel, setCyberLevel] = useState('intermediate');
  const [selectedInterests, setSelectedInterests] = useState<string[]>(['Technology', 'Career']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleActivity = (id: string) => {
    setActivities(prev =>
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  const toggleInterest = (interest: string) => {
    setSelectedInterests(prev =>
      prev.includes(interest) ? prev.filter(i => i !== interest) : [...prev, interest]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload: DigitalContextRequest = {
      life_stage: lifeStage,
      activities: activities,
      cyber_level: cyberLevel,
      interests: selectedInterests,
    };

    try {
      await api.updateContext(payload);
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'Failed to save onboarding preferences.');
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
            <UserCheck size={24} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem' }}>Participant Background Context</h2>
            <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
              Helps calibrate digital scenario realism across user cohorts
            </p>
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <div>{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Life Stage */}
          <div className="form-group">
            <label className="form-label">Current Life / Career Stage</label>
            <select
              className="form-select"
              value={lifeStage}
              onChange={(e) => setLifeStage(e.target.value)}
            >
              {LIFE_STAGES.map(s => (
                <option key={s.id} value={s.id}>{s.label}</option>
              ))}
            </select>
          </div>

          {/* Digital Activities */}
          <div className="form-group">
            <label className="form-label">Frequent Digital Activities (Select all that apply)</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '0.625rem' }}>
              {DIGITAL_ACTIVITIES.map(act => (
                <label
                  key={act.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.625rem',
                    padding: '0.625rem 0.875rem',
                    border: '1px solid var(--color-border)',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: activities.includes(act.id) ? 'var(--color-primary-light)' : 'var(--color-surface)',
                    borderColor: activities.includes(act.id) ? 'var(--color-primary-border)' : 'var(--color-border)',
                    cursor: 'pointer',
                    fontSize: '0.875rem'
                  }}
                >
                  <input
                    type="checkbox"
                    checked={activities.includes(act.id)}
                    onChange={() => toggleActivity(act.id)}
                    style={{ accentColor: 'var(--color-primary)' }}
                  />
                  <span>{act.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Cyber Level */}
          <div className="form-group">
            <label className="form-label">Self-Rated Cybersecurity Experience</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {CYBER_LEVELS.map(lvl => (
                <label
                  key={lvl.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.625rem',
                    padding: '0.625rem 0.875rem',
                    border: '1px solid var(--color-border)',
                    borderRadius: 'var(--radius-md)',
                    backgroundColor: cyberLevel === lvl.id ? 'var(--color-primary-light)' : 'var(--color-surface)',
                    borderColor: cyberLevel === lvl.id ? 'var(--color-primary-border)' : 'var(--color-border)',
                    cursor: 'pointer',
                    fontSize: '0.875rem'
                  }}
                >
                  <input
                    type="radio"
                    name="cyber_level"
                    value={lvl.id}
                    checked={cyberLevel === lvl.id}
                    onChange={() => setCyberLevel(lvl.id)}
                    style={{ accentColor: 'var(--color-primary)' }}
                  />
                  <span>{lvl.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Interests */}
          <div className="form-group">
            <label className="form-label">General Topics of Interest</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {INTERESTS.map(int => {
                const selected = selectedInterests.includes(int);
                return (
                  <button
                    key={int}
                    type="button"
                    onClick={() => toggleInterest(int)}
                    className={`btn ${selected ? 'btn-primary' : 'btn-outline'}`}
                    style={{ padding: '0.375rem 0.75rem', fontSize: '0.8125rem', borderRadius: '9999px' }}
                  >
                    {selected ? '✓ ' : '+ '} {int}
                  </button>
                );
              })}
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '0.75rem', marginTop: '1rem' }}
            disabled={loading}
          >
            {loading ? 'Saving Context...' : (
              <>
                Initialize Study Session <ArrowRight size={18} />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};
