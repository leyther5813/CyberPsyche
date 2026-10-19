export interface User {
  id: string;
  email_hash: string;
  role: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
}

export interface ConsentRequest {
  version: string;
  accepted: boolean;
}

export interface DigitalContextRequest {
  life_stage?: string;
  activities: string[];
  cyber_level?: string;
  interests: string[];
}

export interface SessionResponse {
  session_id: string;
  arm: string;
  form_assignment: string;
  current_phase: string;
  status: string;
}

export interface EvidenceItemScrubbed {
  id: string;
  label: string;
}

export interface EvidenceItemRevealed {
  id: string;
  label: string;
  value: string;
}

export interface ScenarioMessage {
  sender_display?: string;
  body?: string;
  attachment?: string;
}

export interface ScrubbedNextScenarioResponse {
  session_id: string;
  scenario_id: string;
  phase: string;
  context: string;
  channel: string;
  persona: string;
  pressure: string;
  narrative: string;
  message: ScenarioMessage;
  available_evidence: EvidenceItemScrubbed[];
  available_actions: string[];
}

export interface PhaseTransitionResponse {
  session_id: string;
  status: string;
  current_phase: string;
  message: string;
}

export type NextScenarioApiResponse = ScrubbedNextScenarioResponse | PhaseTransitionResponse;

export interface BehaviourEventDTO {
  scenario_id: string;
  event_type: string;
  payload?: Record<string, any>;
  ts?: string;
}

export interface DecisionSubmissionDTO {
  scenario_id: string;
  action: string;
  reason_tags: string[];
  free_text?: string;
  confidence: number;
  latency_ms: number;
}

export interface DecisionOutcomeResponseDTO {
  decision_id: string;
  status: string;
}

export interface InterventionContentResponse {
  session_id: string;
  arm: string;
  lesson_code: string;
  content: {
    title: string;
    body: string;
    exercises: string[];
  };
}

export interface PhaseMetrics {
  count: number;
  decision_quality_mean: number;
  verification_rate: number;
  under_caution_count: number;
  over_caution_count: number;
  evidence_depth_mean: number;
}

export interface ResilienceProfileResponse {
  session_id: string;
  completed_at: string | null;
  profile: Record<string, PhaseMetrics>;
}
