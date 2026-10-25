# CyberPsyche Study Protocol

**Project:** A Decision-Process Laboratory for Social-Engineering Resilience
**Status:** Draft protocol — finalize and register or timestamp the analysis plan before collecting participant data.

## 1. Research question

Does a brief behavior-targeted intervention improve independent verification and transfer across social-engineering scenarios compared with a generic intervention of similar duration?

## 2. Study design

The planned study is a small, two-arm pilot:

- **Targeted intervention:** tailored to the participant's weakest measured mechanism.
- **Generic intervention:** a general verification tip sheet of comparable duration.

The intended pilot target in the project specification is 20–40 adult convenience-sample participants. This is a feasibility target, not a guarantee of adequate statistical power. Arm comparisons should be treated as exploratory unless a formal power analysis supports stronger claims.

## 3. Mechanisms and scenarios

The MVP focuses on three mechanisms:

- **AUTH:** apparent authority or institutional legitimacy.
- **URG:** urgency and pressure to act quickly.
- **REW:** promised reward or benefit.

Scenarios may use education/career, finance, and social/messaging contexts, with email and WhatsApp/SMS-style simulated channels.

Truth classes are malicious, genuine, and ambiguous. All organizations, identities, domains, and contact details must be fictional.

Scenario truth must be established by reviewed, schema-controlled data. An LLM must not determine truth or participant scores at runtime.

## 4. Planned participant flow

1. Present approved study information and obtain affirmative consent.
2. Collect only the minimum approved onboarding context.
3. Administer the baseline scenarios.
4. Record evidence interactions, decisions, and approved response fields.
5. Assign the intervention arm according to the pre-specified randomization procedure.
6. Deliver the targeted or generic intervention.
7. Administer retest scenarios.
8. Administer transfer scenarios that change context or channel while preserving the relevant mechanism.
9. Provide the debrief and privacy/withdrawal information.

The intended project flow uses baseline, intervention, retest, and transfer phases. The exact item counts, phase transitions, and feedback timing must match the implemented application and be frozen before data collection.

## 5. Scenario quality and review

Before participant use:

- Validate scenario structure against the scenario schema.
- Malicious scenarios should contain at least two high-diagnostic suspicious clues and at least one trustworthy-looking clue.
- Genuine scenarios should contain confirming evidence from an official channel.
- Ambiguous scenarios should contain balanced signals and should not be resolvable by one high-diagnostic item before an official-channel check.
- Match low- and high-pressure scenarios by family where required.
- Use distinct surface details for retest and transfer while preserving the target mechanism.
- Have two reviewers assess truth class, evidence quality, realism, safety, and ambiguity.
- Resolve disagreements and record the final scenario version before use.

## 6. Intervention

The intended targeted intervention lasts approximately 60–90 seconds and focuses on the participant's weakest measured mechanism, using two brief micro-exercises. The generic intervention should be comparable in duration and format.

Intervention wording should be pre-generated or human-reviewed and constrained to approved content. The intervention must not expose answers to upcoming scenarios. Record the intervention version and assignment for reproducibility.

## 7. Outcomes and measures

### Primary outcome

The planned primary outcome is the rate of independent verification, defined before analysis as the proportion of eligible decisions in which the participant chooses or completes the protocol-defined independent verification action.

The precise denominator, treatment of missing observations, and handling of repeated decisions must be finalized before data collection.

### Secondary and exploratory measures

- Decision quality against schema-controlled ground truth.
- Under-caution and over-caution.
- Evidence depth and evidence interactions.
- Pressure sensitivity.
- Mechanism-specific vulnerability.
- Response latency.
- Alignment between justification and coded reason categories.
- Transfer performance on changed contexts or channels.
- Calibration measures such as d-prime and criterion, only if the design and observations support their calculation.

Define every metric operationally before examining study outcomes. Do not present a single risk score as a diagnosis or definitive personal trait.

## 8. Data management

Use pseudonymous participant identifiers for behavioral data. Keep consent information separate from behavioral records where feasible. Limit researcher access and export only the fields needed for the approved analysis.

Document the data dictionary, exclusions, missing-data rules, retention period, deletion workflow, and backup/access controls before recruitment. Research exports must not expose direct identifiers or unnecessary free-text content.

## 9. Analysis plan

For the pilot:

- Report recruitment, completion, missingness, and protocol deviations.
- Summarize the primary outcome and relevant secondary measures with uncertainty intervals where appropriate.
- Report effect sizes and confidence intervals; avoid treating a small pilot as definitive evidence of effectiveness.
- Consider paired comparisons for within-participant phases.
- Consider mixed-effects logistic regression only if the sample size, outcome structure, and convergence support it.
- Treat between-arm estimates as exploratory at the planned pilot size.
- Document exclusions and deviations transparently.
- Report scenario-review agreement; Cohen's kappa may be used for suitable categorical ratings.

Finalize the hypotheses, outcome definitions, exclusions, and analysis decisions before collecting participant data. Do not select the primary analysis based on which result looks most favorable.

## 10. Ethics and participant safety

Recruit only after confirming institutional ethics requirements and finalizing approved consent and debrief materials. Participation must be voluntary. Do not collect real credentials, OTPs, payment details, private messages, or other secrets. Provide a clear explanation of the simulated nature of the task and the limits of withdrawal/deletion.

## 11. Reproducibility and reporting

Record the application version, scenario-library version, intervention wording version, randomization procedure, analysis code version, and any protocol deviations. Keep a dated copy of the finalized protocol and analysis plan.

The final report should describe the research question, methods, participant flow, scenario validation, outcomes, results, limitations, and reproducibility steps. Distinguish feasibility findings from evidence of efficacy and avoid overstating results from a small convenience sample.

## 12. Pre-study checklist

- [ ] Confirm institutional ethics requirements and obtain any required approval.
- [ ] Finalize participant information, consent, debrief, and contact details.
- [ ] Freeze hypotheses, primary outcome, exclusions, and analysis plan.
- [ ] Review and validate the complete scenario set.
- [ ] Verify randomization, phase order, and feedback timing.
- [ ] Verify authorization, privacy, deletion, and pseudonymized exports.
- [ ] Test the full participant flow using test accounts and synthetic data.
- [ ] Confirm backups and record the application and scenario versions.

**Status:** This protocol is a draft and is not evidence that the study is approved or that every planned procedure is implemented.
