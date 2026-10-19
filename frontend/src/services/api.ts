import type {
  AuthResponse,
  ConsentRequest,
  DigitalContextRequest,
  SessionResponse,
  NextScenarioApiResponse,
  BehaviourEventDTO,
  DecisionSubmissionDTO,
  DecisionOutcomeResponseDTO,
  InterventionContentResponse,
  ResilienceProfileResponse,
} from '../types';

const API_BASE = '/api/v1';

let authToken: string | null = localStorage.getItem('cyberpsyche_token');

export const setAuthToken = (token: string | null) => {
  authToken = token;
  if (token) {
    localStorage.setItem('cyberpsyche_token', token);
  } else {
    localStorage.removeItem('cyberpsyche_token');
  }
};

export const getAuthToken = () => authToken;

const getHeaders = (isJson = true): HeadersInit => {
  const headers: Record<string, string> = {};
  if (isJson) {
    headers['Content-Type'] = 'application/json';
  }
  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }
  return headers;
};

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `HTTP ${res.status} ${res.statusText}`;
    try {
      const errJson = await res.json();
      if (errJson && errJson.detail) {
        errorDetail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
      }
    } catch {
      // ignore json parse error
    }
    throw new Error(errorDetail);
  }
  return res.json();
}

export const api = {
  register: async (email: string, password: string): Promise<AuthResponse> => {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ email, password }),
    });
    const data = await handleResponse<AuthResponse>(res);
    setAuthToken(data.access_token);
    return data;
  },

  login: async (email: string, password: string): Promise<AuthResponse> => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ email, password }),
    });
    const data = await handleResponse<AuthResponse>(res);
    setAuthToken(data.access_token);
    return data;
  },

  logout: async (): Promise<void> => {
    try {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: getHeaders(),
      });
    } finally {
      setAuthToken(null);
    }
  },

  acceptConsent: async (version = '1.0', accepted = true): Promise<{ status: string }> => {
    const res = await fetch(`${API_BASE}/consent`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ version, accepted } as ConsentRequest),
    });
    return handleResponse(res);
  },

  updateContext: async (context: DigitalContextRequest): Promise<{ status: string }> => {
    const res = await fetch(`${API_BASE}/context`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(context),
    });
    return handleResponse(res);
  },

  startSession: async (arm = 'targeted', form_assignment = 'Form_A'): Promise<SessionResponse> => {
    const res = await fetch(`${API_BASE}/sessions`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ arm, form_assignment }),
    });
    return handleResponse(res);
  },

  getNextScenario: async (sessionId: string): Promise<NextScenarioApiResponse> => {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/next`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(res);
  },

  logEvent: async (sessionId: string, dto: BehaviourEventDTO): Promise<{ event_id: string; status: string; revealed_evidence?: { id: string; label: string; value: string } }> => {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/events`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(dto),
    });
    return handleResponse(res);
  },

  submitDecision: async (sessionId: string, dto: DecisionSubmissionDTO): Promise<DecisionOutcomeResponseDTO> => {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/decision`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(dto),
    });
    return handleResponse(res);
  },

  getIntervention: async (sessionId: string): Promise<InterventionContentResponse> => {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/intervention`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(res);
  },

  completeIntervention: async (sessionId: string, practiceScore = 100): Promise<{ session_id: string; status: string; next_phase: string }> => {
    const res = await fetch(`${API_BASE}/intervention/complete`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ session_id: sessionId, practice_score: practiceScore }),
    });
    return handleResponse(res);
  },

  getProfile: async (sessionId: string): Promise<ResilienceProfileResponse> => {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/profile`, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(res);
  },
};
