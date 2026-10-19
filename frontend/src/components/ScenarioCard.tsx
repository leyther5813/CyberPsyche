import React from 'react';
import type { ScrubbedNextScenarioResponse } from '../types';
import { EmailScenario } from './EmailScenario';
import { ChatScenario } from './ChatScenario';

interface ScenarioCardProps {
  scenario: ScrubbedNextScenarioResponse;
}

export const ScenarioCard: React.FC<ScenarioCardProps> = ({ scenario }) => {
  const isEmail = scenario.channel.toLowerCase() === 'email';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {isEmail ? (
        <EmailScenario
          narrative={scenario.narrative}
          message={scenario.message}
          persona={scenario.persona}
          context={scenario.context}
        />
      ) : (
        <ChatScenario
          narrative={scenario.narrative}
          message={scenario.message}
          persona={scenario.persona}
          context={scenario.context}
        />
      )}
    </div>
  );
};
