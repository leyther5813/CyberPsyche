import React, { useState, useEffect } from 'react';
import { Loader2, AlertCircle, ArrowRight, ShieldAlert } from 'lucide-react';
import type { ScrubbedNextScenarioResponse, EvidenceItemRevealed, NextScenarioApiResponse } from '../types';
import { api } from '../services/api';
import { ScenarioCard } from './ScenarioCard';
import { EvidenceList } from './EvidenceList';
import { ActionSelector } from './ActionSelector';
import { ReasoningInput } from './ReasoningInput';
import { ConfidenceSelector } from './ConfidenceSelector';
import { InterventionScreen } from './InterventionScreen';
import { ProfileDebriefScreen } from './ProfileDebriefScreen';

interface StudyShellProps {
  sessionId: string;
  onRestart: () => void;
  onLogout?: () => void;
}

export const StudyShell: React.FC<StudyShellProps> = ({ sessionId, onRestart, onLogout }) => {
  const [currentScenario, setCurrentScenario] = useState<ScrubbedNextScenarioResponse | null>(null);
  const [currentPhase, setCurrentPhase] = useState<string>('baseline');
  const [scenarioIndex, setScenarioIndex] = useState<number>(1);
  const [loadingScenario, setLoadingScenario] = useState<boolean>(true);
  
  // Decision form state
  const [revealedEvidenceMap, setRevealedEvidenceMap] = useState<Record<string, EvidenceItemRevealed>>({});
  const [selectedAction, setSelectedAction] = useState<string | null>(null);
  const [reasonTags, setReasonTags] = useState<string[]>([]);
  const [freeText, setFreeText] = useState<string>('');
  const [confidence, setConfidence] = useState<number>(3);
  
  // Submission & latency tracking
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [startTime, setStartTime] = useState<number>(Date.now());

  // Fetch next scenario from backend
  const fetchNext = async () => {
    setLoadingScenario(true);
    setError(null);
    try {
      const res: NextScenarioApiResponse = await api.getNextScenario(sessionId);

      if ('status' in res && (res.status === 'phase_completed' || res.status === 'phase_transition')) {
        // Phase transition state machine
        setCurrentPhase(res.current_phase);
        setCurrentScenario(null);
        if (res.current_phase === 'transfer' || res.current_phase === 'retest' || res.current_phase === 'baseline') {
          // Automatic transition to active scenario phase without requiring manual refresh
          setScenarioIndex(1);
          const nextRes: NextScenarioApiResponse = await api.getNextScenario(sessionId);
          if ('scenario_id' in nextRes) {
            const scResp = nextRes as ScrubbedNextScenarioResponse;
            setCurrentScenario(scResp);
            setCurrentPhase(scResp.phase);
            setRevealedEvidenceMap({});
            setSelectedAction(null);
            setReasonTags([]);
            setFreeText('');
            setConfidence(3);
            setStartTime(Date.now());
          }
        }
      } else if ('scenario_id' in res) {
        // Scenario response
        const scResp = res as ScrubbedNextScenarioResponse;
        if (scResp.phase !== currentPhase) {
          setScenarioIndex(1);
        }
        setCurrentScenario(scResp);
        setCurrentPhase(scResp.phase);
        // Reset local decision form state
        setRevealedEvidenceMap({});
        setSelectedAction(null);
        setReasonTags([]);
        setFreeText('');
        setConfidence(3);
        setStartTime(Date.now());
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch next scenario.');
    } finally {
      setLoadingScenario(false);
    }
  };

  useEffect(() => {
    fetchNext();
  }, [sessionId]);

  const handleEvidenceRevealed = (revealed: EvidenceItemRevealed) => {
    setRevealedEvidenceMap(prev => ({ ...prev, [revealed.id]: revealed }));
  };

  const handleToggleTag = (tag: string) => {
    setReasonTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  };

  const handleSubmitDecision = async () => {
    if (!currentScenario) return;

    if (!selectedAction) {
      setError('Please select a response action before submitting.');
      return;
    }

    setSubmitting(true);
    setError(null);

    const latency_ms = Math.max(0, Date.now() - startTime);

    try {
      await api.submitDecision(sessionId, {
        scenario_id: currentScenario.scenario_id,
        action: selectedAction,
        reason_tags: reasonTags,
        free_text: freeText,
        confidence: confidence,
        latency_ms: latency_ms,
      });

      // Increment local count and fetch next scenario
      setScenarioIndex(prev => prev + 1);
      await fetchNext();
    } catch (err: any) {
      // Preserve user input on error, do NOT silently advance!
      setError(err.message || 'Failed to record decision. Please retry.');
    } finally {
      setSubmitting(false);
    }
  };

  // Phase tracker items
  const phasesOrder = [
    { id: 'baseline', label: 'Baseline Phase' },
    { id: 'intervention', label: 'Intervention' },
    { id: 'retest', label: 'Retest Phase' },
    { id: 'transfer', label: 'Transfer Phase' },
    { id: 'profile', label: 'Debrief Profile' },
  ];

  const getStepClass = (phaseId: string) => {
    const currentIdx = phasesOrder.findIndex(p => p.id === currentPhase);
    const targetIdx = phasesOrder.findIndex(p => p.id === phaseId);

    if (currentIdx === targetIdx) return 'step-item active';
    if (currentIdx > targetIdx) return 'step-item completed';
    return 'step-item';
  };

  if (currentPhase === 'intervention') {
    return (
      <div className="container">
        <InterventionScreen
          sessionId={sessionId}
          onComplete={() => {
            setScenarioIndex(1);
            fetchNext();
          }}
        />
      </div>
    );
  }

  if (currentPhase === 'profile') {
    return (
      <div className="container">
        <ProfileDebriefScreen sessionId={sessionId} onRestart={onRestart} />
      </div>
    );
  }

  return (
    <div className="container" style={{ maxWidth: '960px' }}>
      {/* Phase Tracker */}
      <div className="step-tracker">
        {phasesOrder.map((ph, idx) => (
          <div key={ph.id} className={getStepClass(ph.id)}>
            <div className="step-bubble">{idx + 1}</div>
            <div className="step-label">{ph.label}</div>
          </div>
        ))}
      </div>

      {loadingScenario ? (
        <div style={{ textAlign: 'center', padding: '4rem 1rem' }}>
          <Loader2 size={36} className="spin" color="var(--color-primary)" style={{ margin: '0 auto 1rem' }} />
          <p style={{ color: 'var(--color-text-muted)' }}>Loading active research scenario...</p>
        </div>
      ) : error && !currentScenario ? (
        <div className="card">
          <div className="alert alert-error">
            <AlertCircle size={18} />
            <div>{error}</div>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1rem', flexWrap: 'wrap' }}>
            <button onClick={fetchNext} className="btn btn-secondary">
              Retry Loading Scenario
            </button>
            {onLogout && (
              <button onClick={onLogout} className="btn btn-primary">
                Return to Sign In
              </button>
            )}
          </div>
        </div>
      ) : currentScenario ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Active Phase Badge & Scenario Counter */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: '#ffffff',
            padding: '0.875rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--color-border)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <span className="badge badge-blue">
                {currentScenario.phase.toUpperCase()} PHASE
              </span>
              <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--color-text)' }}>
                Scenario {scenarioIndex} of 6
              </span>
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
              Channel: <span style={{ fontWeight: 600, textTransform: 'capitalize' }}>{currentScenario.channel}</span>
            </div>
          </div>

          {/* Scenario Presentation Card (Email/Chat) */}
          <ScenarioCard scenario={currentScenario} />

          {/* Evidence Inspection Component */}
          <EvidenceList
  	sessionId={sessionId}
  	scenarioId={currentScenario.scenario_id}
  	availableEvidence={currentScenario.available_evidence}
  	revealedEvidenceMap={revealedEvidenceMap}
  	onEvidenceRevealed={handleEvidenceRevealed}
  	disabled={submitting || loadingScenario}
	/>
          {/* Action Selection Component */}
          <ActionSelector
            availableActions={currentScenario.available_actions}
            selectedAction={selectedAction}
            onSelectAction={setSelectedAction}
          />

          {/* Reasoning Input Component */}
          <ReasoningInput
            selectedTags={reasonTags}
            freeText={freeText}
            onToggleTag={handleToggleTag}
            onFreeTextChange={setFreeText}
          />

          {/* Confidence Rating Component */}
          <ConfidenceSelector
            confidence={confidence}
            onChangeConfidence={setConfidence}
          />

          {error && (
            <div className="alert alert-error">
              <AlertCircle size={18} />
              <div>{error}</div>
            </div>
          )}

          {/* Submit Decision Footer */}
          <div className="card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ShieldAlert size={16} color="var(--color-primary)" />
              <span>Decisions are final upon submission. No correctness feedback is displayed during research phase.</span>
            </div>

            <button
              type="button"
              onClick={handleSubmitDecision}
              className="btn btn-primary"
              style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem' }}
              disabled={submitting || !selectedAction}
            >
              {submitting ? (
                <>
                  <Loader2 size={18} className="spin" /> Submitting Decision...
                </>
              ) : (
                <>
                  Record Decision & Proceed <ArrowRight size={18} />
                </>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--color-text-muted)' }}>No active scenario found for phase: {currentPhase}.</p>
          <button onClick={fetchNext} className="btn btn-secondary" style={{ marginTop: '1rem' }}>
            Refresh Scenario State
          </button>
        </div>
      )}
    </div>
  );
};
