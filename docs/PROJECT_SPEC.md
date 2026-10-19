# CyberPsyche

### A Decision-Process Laboratory for Social-Engineering Resilience

*Project Specification v1.0: research design, system design, build plan and write-up guide*

---

## 0. How to use this document

This is your single reference from idea to finished, evaluated project. Read Sections 1-6 to understand *what* and *why*, Sections 7-17 to *build* it, Sections 18-21 to *secure, evaluate and ethically run* it, and Sections 22-25 to *package it* for your Master's applications. Anything marked **\[VERIFY\]** must be checked by you (citations, ethics rules at your institution).

**Guiding principle:** a small project that is *finished, evaluated and honestly reported* beats a large unbuilt vision. Everything marked "Future Work" is deliberately out of scope.

---

## 1. Abstract (use this in README, CV and SOP)

CyberPsyche is an AI-assisted simulation platform that studies how people make security decisions under social-engineering pressure. It generates context-aware scenarios from a controlled schema (manipulation mechanism, channel, ground truth, pressure level), records evidence-seeking and verification behaviour alongside self-reported reasoning, delivers targeted micro-interventions, and evaluates whether improved behaviour transfers to unseen contexts. By including genuine and ambiguous scenarios, it separates *under-caution* from *over-caution* and aims to promote calibrated trust rather than blanket suspicion. A pilot study with a randomized two-arm design evaluates targeted versus generic training.

---

## 2. Problem and motivation

- Most breaches involve a human decision at some point; technical controls cannot fully remove it.
- Common awareness training is generic ("don't click suspicious links"), measures only click/no-click, and rarely tests whether learning survives a change of context.
- Large-scale field evidence suggests embedded phishing training can have limited effect **\[VERIFY: Lain et al., IEEE S&P 2022\]**.
- Most tools teach people to *reject* suspicious things. Real life also contains genuine urgent requests (bank alerts, college deadlines). Blanket suspicion causes missed legitimate actions and fatigue.

**Gap CyberPsyche addresses:** measuring the *decision process* (what evidence was sought, whether verification was independent, what reasoning was given) and testing *transfer* of a verification strategy across contexts, while penalizing both gullibility and paranoia.

**Positioning against existing work:** open-source social-engineering simulators (e.g., Pretexta, DECEIVER) emphasize AI roleplay, realistic scenarios and feedback. CyberPsyche is not a roleplay or quiz tool. Its contribution is the **instrumented decision loop + intervention + transfer experiment**.

---

## 3. Research question, hypotheses, objectives

**Primary research question (RQ1)** Does a short, behaviour-targeted intervention improve users' independent-verification behaviour in social-engineering scenarios, and does the improvement transfer to a different context and channel?

**Secondary questions**

- **RQ2:** Does pressure (time urgency, authority) degrade decision quality, and which mechanism degrades it most?
- **RQ3:** Does the intervention improve *calibration* (fewer unsafe actions on malicious items without more rejections of genuine items)?
- **RQ4:** Is a targeted intervention (based on the user's own weak mechanism) better than a generic tip sheet?

**Hypotheses**

- **H1:** Independent-verification rate increases from baseline to immediate retest.
- **H2:** The gain persists in the transfer phase (new context and channel) at a level above baseline.
- **H3:** Under-caution decreases without a significant increase in over-caution.
- **H4:** High-pressure variants produce lower decision quality than low-pressure variants of the same scenario.
- **H5 (exploratory):** The targeted arm outperforms the generic arm on transfer.

**Objectives**

1. Build a schema-driven scenario engine with controlled ground truth.
2. Build an instrumented simulation UI that logs behaviour, not just answers.
3. Implement rule-based behavioural scoring.
4. Implement intervention + retest + transfer pipeline.
5. Run a pilot study and report results honestly.
6. Engineer the platform securely.

---

## 4. Theoretical grounding (cite and position against these) **\[VERIFY all\]**

| Area | Source | Use in project |
| --- | --- | --- |
| Persuasion principles | Cialdini, *Influence* | Basis of mechanism taxonomy (authority, scarcity, social proof, reciprocity, commitment, liking) |
| Scam victimology | Stajano & Wilson, "Understanding scam victims: seven principles for systems security", CACM 2011 | Distraction, social compliance, herd, dishonesty, kindness, need-and-greed, time principles |
| Embedded phishing training | Kumaraguru et al. (PhishGuru) | Prior art for teaching at the "teachable moment" |
| Training effectiveness | Lain, Kostiainen, Čapkun, IEEE S&P 2022 | Motivates rigorous evaluation and transfer measurement |
| Detection under uncertainty | Signal Detection Theory (Green & Swets) | Formal basis for under-caution vs over-caution (sensitivity d′, criterion c) |
| Transfer of learning | Barnett & Ceci, 2002 taxonomy of transfer | Defines near vs far transfer |
| Dual-process thinking | Kahneman, *Thinking, Fast and Slow* | Why urgency pushes people toward fast, unverified decisions |

---

## 5. Scope

### 5.1 In scope (MVP)

- **Mechanisms (3):** Authority, Urgency (time pressure), Reward/Scarcity. (Authority + Urgency is the primary transfer pair.)
- **Contexts (3):** Education/Career (college, internship), Finance (UPI/bank), Social/Messaging.
- **Channels (2):** Email-style view, WhatsApp/SMS-style chat view.
- **Truth classes (3):** Malicious, Genuine, Ambiguous.
- **Core loop:** onboarding → baseline → evidence board → decision → justification → intervention → retest → transfer → profile.
- **Pressure levels:** Low / Medium / High (varied in wording, and optional timer).
- **Results dashboard** (individual profile + researcher aggregate view).
- Secure authentication and privacy-minimal data handling.

### 5.2 Out of scope (Future Work)

Voice/vishing, QR/physical scams, live AI-attacker chat, 5 experiment modes, 10+ mechanisms, gamification/badges, mobile app, multi-language, real-time adaptive difficulty. Mention these in the write-up only as future work.

---

## 6. Conceptual framework

### 6.1 Manipulation mechanisms (controlled taxonomy)

| Code | Mechanism | Example cue |
| --- | --- | --- |
| AUTH | Authority | "This is your bank's security department" |
| URG | Urgency / time pressure | "Complete within 10 minutes" |
| REW | Reward / scarcity | "Only 3 internship slots left; ₹50,000 scholarship" |

(Extension candidates: fear, familiarity, reciprocity, curiosity, commitment.) Each scenario is tagged with 1-2 mechanisms. A scenario can be **combined** (AUTH+URG).

### 6.2 Scenario truth classes

- **Malicious:** a real attack (simulated). Safe action: verify independently / report / ignore.
- **Genuine:** legitimate request. Safe action: verify then proceed (rejecting without checking = over-caution).
- **Ambiguous:** evidence insufficient. Safe action: gather more evidence / verify independently; proceeding or flat rejection are both unsafe.

### 6.3 Evidence model

Each scenario has evidence items, each tagged:

- `signal`: **suspicious / neutral / trustworthy / hidden-until-inspected**
- `diagnosticity`: how strongly it indicates the truth (high/medium/low)
- `cost`: effort to inspect (optional; supports "evidence-seeking effort")

Evidence types: sender address/number, domain, timestamp, link destination (shown as text, never a live link), attachment name, prior-communication check, official-channel check, language/tone, request type.

### 6.4 Action space

`PROCEED`, `IGNORE`, `REPLY_TO_SENDER`, `VERIFY_INDEPENDENTLY` (official site/app/known number), `REPORT`, `ASK_TRUSTED_PERSON`, `GATHER_MORE_EVIDENCE`, `UNSURE`. Each scenario defines which actions are **safe / acceptable / unsafe** (multiple defensible actions allowed).

### 6.5 Behavioural constructs and operational definitions (rule-based, no LLM diagnosis)

| Construct | Operational definition |
| --- | --- |
| Evidence-seeking depth | # distinct evidence items opened before deciding ÷ # available (and # diagnostic items opened) |
| Independent verification | Chose `VERIFY_INDEPENDENTLY` or opened the "official channel" evidence item before deciding |
| Decision quality | Action rated safe=1, acceptable=0.5, unsafe=0 (per scenario schema) |
| Under-caution | Unsafe action (PROCEED / REPLY_TO_SENDER) on a malicious item, or proceeding on ambiguous without verification |
| Over-caution | IGNORE/REPORT on a genuine item with no evidence inspected (or fewer than a threshold) |
| Pressure sensitivity | Decision quality(low pressure) − Decision quality(high pressure), matched by scenario family |
| Mechanism vulnerability | Mean decision quality per mechanism |
| Decision latency | Time from scenario load to action |
| Reasoning alignment | Whether selected reason tags are consistent with the evidence inspected (e.g., "I verified independently" without verifying = inconsistency) |
| Calibration (SDT) | d′ = z(hit rate on malicious "defended") − z(false-alarm rate on genuine "rejected"); criterion c shows bias toward suspicion or trust |
| Transfer | Retest/transfer decision quality and verification rate on items sharing a mechanism but differing in context/channel |

---

## 7. System architecture

```text
Frontend (React/Next.js)
   │  REST/JSON over HTTPS
Backend API (FastAPI)
   ├─ Auth & session service
   ├─ Scenario service  ──► Scenario Store (validated JSON/DB)
   │       └─ LLM Renderer (schema-constrained, wording only)
   ├─ Session orchestrator (phase state machine)
   ├─ Behaviour logger (event stream)
   ├─ Scoring engine (rule-based)
   ├─ Intervention selector (rules → lesson)
   └─ Analytics/export service
Database (PostgreSQL)
Analysis (Python: pandas, scipy, statsmodels) → figures + report
```

**Design principles**

1. **Ground truth lives in the schema, never in the LLM.**
2. **Behaviour labels come from rules, not LLM judgements.**
3. **Everything is simulated; no real links, credentials or OTPs.**
4. **Log events, derive metrics later** (append-only event log makes re-analysis possible).
5. **Pre-generate and human-review** all scenario text; do not generate live during a study (reproducibility and safety).

---

## 8. Scenario schema (the core asset)

```json
{
  "scenario_id": "EDU-AUTH-URG-MAL-01",
  "family_id": "AUTHURG-MAL-A",
  "phase_pool": "baseline",
  "context": "education_career",
  "channel": "email",
  "persona": "college student (fictional)",
  "truth": "malicious",
  "mechanisms": ["authority", "urgency"],
  "pressure": "high",
  "difficulty": "medium",
  "narrative": "Placement coordinator emails a shortlist notice.",
  "message": {
    "sender_display": "Placement Cell",
    "body": "Congratulations! You are shortlisted. Confirm within 20 minutes using the attached form.",
    "attachment": "registration-form.pdf.exe"
  },
  "evidence": [
    {"id": "e1", "label": "Sender address", "value": "placements@college-career.net", "signal": "suspicious", "diagnosticity": "high"},
    {"id": "e2", "label": "Official college domain", "value": "college.edu.in", "signal": "suspicious", "diagnosticity": "high"},
    {"id": "e3", "label": "Sent at", "value": "2:17 AM", "signal": "suspicious", "diagnosticity": "low"},
    {"id": "e4", "label": "Earlier emails from this sender", "value": "None found", "signal": "suspicious", "diagnosticity": "medium"},
    {"id": "e5", "label": "Official placement portal", "value": "No such notice listed", "signal": "suspicious", "diagnosticity": "high", "official_channel": true},
    {"id": "e6", "label": "Greeting uses your real name", "value": "Yes", "signal": "trustworthy", "diagnosticity": "low"}
  ],
  "actions": {
    "safe": ["VERIFY_INDEPENDENTLY", "REPORT", "IGNORE"],
    "acceptable": ["GATHER_MORE_EVIDENCE", "ASK_TRUSTED_PERSON"],
    "unsafe": ["PROCEED", "REPLY_TO_SENDER"]
  },
  "consequence_text": {
    "unsafe": "Opening the file would have installed malware (simulated).",
    "safe": "Verifying on the official portal revealed no such notice."
  },
  "teaching_point": "Authority claims should increase your need to verify.",
  "transfer_group": "AUTH_URG"
}
```

**Validation rules (enforced in code, with JSON Schema/Pydantic):**

- Malicious scenarios must contain ≥ 2 high-diagnosticity suspicious clues, ≥ 1 trustworthy-looking clue.
- Genuine scenarios must be verifiable via an `official_channel` evidence item that returns confirming information.
- Ambiguous scenarios must have balanced signals and no single high-diagnosticity item that resolves truth until the official channel is checked.
- No real domains, phone numbers, or brands that could cause harm; use fictional names.
- Every scenario has a `family_id` so matched low/high-pressure variants exist.

---

## 9. Scenario library design

### 9.1 Design matrix (example of the 36-scenario target)

| Dimension | Levels |
| --- | --- |
| Mechanism | AUTH, URG, REW (plus combos AUTH+URG, REW+URG) |
| Context | Education/Career, Finance, Social |
| Channel | Email, Chat |
| Truth | Malicious (≈50%), Genuine (≈30%), Ambiguous (≈20%) |
| Pressure | Low, Medium, High |

### 9.2 Pools (balanced and counterbalanced)

- **Pool B (baseline):** 8 scenarios
- **Pool R (retest):** 8 scenarios, *surface-different but same mechanism and context as B*
- **Pool T (transfer):** 8 scenarios, *same mechanism, different context and channel*
- **Pool D (delayed, optional):** 4 scenarios for 7-day retention
- Total ≈ 28-36 scenarios. Each participant sees a subset (e.g., 6 per phase) so a session is \~20-25 minutes.
- **Counterbalance:** randomly assign matched Form A/B between baseline and retest to avoid scenario-difficulty confounds.
- Each scenario written by hand/LLM-assisted, then **peer-reviewed by 2 people** for realism and correctness of truth labels.

### 9.3 Writing workflow

1. Write the structured schema entry by hand.
2. Use the LLM only to produce 2-3 wording variants of the message body (same facts, same clues).
3. Automated check: variants must not add/remove clues (compare to schema).
4. Human review → approve → freeze (version tag `scenario_set_v1`).

---

## 10. Session flow (state machine)

```text
CONSENT → ONBOARDING → PHASE 1 BASELINE (6)
        → PHASE 2 INTERVENTION (targeted or generic, randomized)
        → PHASE 3 IMMEDIATE RETEST (6)
        → PHASE 4 TRANSFER (6)
        → PHASE 5 PROFILE + DEBRIEF (+ optional delayed retest after 7 days)
```

**Per-scenario loop**

1. Show scenario in channel-styled UI (email or chat view).
2. Evidence board: user clicks items to reveal; each click logged with timestamp.
3. User selects action (can choose GATHER_MORE_EVIDENCE then continue).
4. User gives reasons (checkbox tags + optional free text) *and* confidence (1-5).
5. Reveal outcome, ground truth, and evidence explanation (immediate feedback in baseline can be disabled to avoid contaminating baseline; recommended: **no feedback in baseline, feedback only after Phase 1 completes**).

**Important design decision:** hide the ground truth in baseline and retest (no per-item feedback) so improvements come from the intervention, not from item-by-item correction.

---

## 11. Onboarding (minimal context only)

Collect: life stage, digital activities used (multi-select), self-rated cyber experience (5 levels), optional interest areas. Used **only** to choose contexts and wording (e.g., a student sees internship scenarios). Do **not** collect personality, bank details, passwords, OTPs, private messages. Age 18+ confirmation and consent shown first.

---

## 12. Role of AI (and its leash)

| Task | Done by | Notes |
| --- | --- | --- |
| Ground truth, mechanisms, evidence, safe actions | Schema (human-authored) | Never altered by LLM |
| Wording variants | LLM (pre-generated, human-reviewed) | JSON-schema output, temperature low |
| Persona/context personalization | Template + LLM wording | Facts unchanged |
| Mapping free-text reasons to tags | LLM **suggests**, controlled taxonomy **decides** | Used for exploratory analysis only; store tag + model version; manually audit a sample |
| Behaviour labels (under/over-caution, etc.) | Rules | Deterministic, reproducible |
| Feedback explanation text | Template filled from schema | Optionally polished by LLM |

**Safeguards:** prompt-injection-safe handling of user free text (treat as data, never as instructions), output validation against schema, content filter for real brands, logging of model + prompt version, and a no-LLM fallback so the system works offline.

---

## 13. Scoring and behavioural analysis (rules)

**Per-scenario outputs:** `decision_quality` (0/0.5/1), `under_caution`, `over_caution`, `verified_independently`, `evidence_depth`, `diagnostic_evidence_found`, `latency_ms`, `reason_alignment_flag`, `confidence`.

**Example rules**

```text
under_caution  = truth in {malicious} AND action in unsafe
              OR truth == ambiguous AND action == PROCEED AND no official_channel opened
over_caution   = truth == genuine AND action in {IGNORE, REPORT} AND evidence_opened < 2
verified       = action == VERIFY_INDEPENDENTLY OR official_channel item opened before action
overconfident_error = confidence >= 4 AND decision_quality == 0
```

**Profile (per participant, per phase):** mechanism-level quality, verification rate, evidence depth, pressure sensitivity, under/over-caution, calibration (d′, c), confidence-accuracy gap, transfer score. Display with confidence caveats; **never show a single "risk score"**. With few items per mechanism, show raw counts (e.g., 3/4) rather than precise percentages.

---

## 14. Intervention design

**Principle:** one idea, 60-90 seconds, tied to the user's weakest mechanism and demonstrated with the user's own baseline mistake.

**Targeted arm (rules choose lesson):**

| Weakness detected | Lesson | Micro-practice |
| --- | --- | --- |
| Low verification overall | "Verify on a channel you opened yourself, not the one the message gave you" | Pick the correct verification route for 2 examples |
| AUTH vulnerability | "Authority should increase verification, not reduce it" | Identify which source to confirm a claimed official |
| URG vulnerability | "Urgency is a cue to slow down; real institutions allow verification time" | Rewrite a rushed message into a safe response plan |
| REW vulnerability | "Unexpected rewards that need quick action or fees are red flags" | Spot the asks (fee/info/speed) in an offer |
| Over-caution | "Check before rejecting: genuine requests can be confirmed" | Practice confirming a legitimate notice |

**Generic arm:** a standard tip sheet (same length) covering general phishing advice, not tied to the user's weakness.

**Delivery:** short explanation → worked example → 2 micro-exercises with feedback. Content is static and reviewed, not generated live.

---

## 15. Study design (pilot)

- **Design:** randomized two-arm pilot (targeted vs generic intervention), within-subject across phases.
- **Participants:** 20-40 adult volunteers (students/peers), self-selected. Mention it clearly as a *convenience sample*.
- **Phases/measures:** Baseline → Intervention → Retest → Transfer → (Delayed retest at 7 days, optional).
- **Primary outcome:** independent-verification rate (baseline → retest → transfer).
- **Secondary outcomes:** decision quality, under-caution, over-caution, d′, pressure sensitivity, confidence calibration.
- **Analysis plan (write before collecting data):**
  - Descriptive stats with 95% CIs
  - Paired comparison (Wilcoxon signed-rank or paired t-test per distribution) for phase changes
  - Mixed-effects logistic regression: `verified ~ phase * arm + pressure + mechanism + (1|participant) + (1|scenario)`
  - Effect sizes (Cohen's d / odds ratios) with CIs rather than only p-values
  - Exploratory arm comparison flagged as underpowered
- **Threats to validity (state them):** small sample, self-selection, no real stakes (simulated vs real behaviour), demand characteristics (people know they're in a security study), practice effects, short retention, scenario-difficulty differences (mitigated by counterbalancing), authorship bias in scenario writing.
- **Pre-register** your hypotheses and analysis plan in a short document (OSF or a dated file in the repo).

---

## 16. Data model (PostgreSQL)

| Table | Key columns |
| --- | --- |
| `user` | id, email_hash/username, password_hash, role (participant/researcher/admin), created_at |
| `consent` | user_id, version, accepted_at |
| `digital_context` | user_id, life_stage, activities\[\], cyber_level, interests\[\] |
| `scenario` | id, family_id, context, channel, truth, mechanisms\[\], pressure, difficulty, pool, json_payload, version |
| `evidence_item` | id, scenario_id, label, value, signal, diagnosticity, official_channel |
| `session` | id, user_id, arm, form_assignment, started_at, completed_at, scenario_set_version |
| `session_scenario` | session_id, scenario_id, phase, order_idx |
| `behaviour_event` | id, session_id, scenario_id, event_type (view/open_evidence/action/reason/confidence), payload, ts |
| `decision` | session_id, scenario_id, action, reasons\[\], free_text, confidence, latency_ms |
| `scenario_outcome` | decision_id, decision_quality, under_caution, over_caution, verified, evidence_depth, flags |
| `intervention` | id, type (targeted/generic), lesson_code, content_version |
| `intervention_delivery` | session_id, intervention_id, completed_at, practice_score |
| `resilience_profile` | session_id, phase, metrics_json |
| `audit_log` | id, actor_id, action, resource, ts, ip_hash |

Pseudonymize participants in exports (random participant codes), keep consent separate from behavioural data.

---

## 17. API and UI

### 17.1 API (representative)

```text
POST /auth/register | /auth/login | /auth/logout
POST /consent
PUT  /context
POST /sessions                      -> create session, assign arm/form
GET  /sessions/{id}/next            -> next scenario (no truth fields exposed)
POST /sessions/{id}/events          -> log evidence-open, view, etc.
POST /sessions/{id}/decision        -> action + reasons + confidence
GET  /sessions/{id}/intervention
GET  /sessions/{id}/profile
GET  /research/export (role=researcher) -> pseudonymized CSV
```

**Server never sends `truth`, `signal` or `safe actions` to the client before the decision.** Evidence values are revealed only when requested.

### 17.2 Screens

1. Landing + consent
2. Onboarding (context form)
3. Simulation view (channel-styled message + evidence board + action panel)
4. Reasoning panel (tags + free text + confidence)
5. Feedback/explanation screen (after Phase 1, not per-item)
6. Learning Lab (intervention + micro-exercises)
7. Transfer challenge screen (labelled by mechanism)
8. Profile & timeline (baseline → retest → transfer)
9. Researcher dashboard (aggregate charts, export)
10. Settings/privacy (delete my data)

**UI tone:** clean research-lab dashboard (neutral palette, clear typography), not a "hacker" aesthetic. Accessible (keyboard navigation, contrast).

---

## 18. Security of the application (threat model + controls)

**Assets:** participant accounts, behavioural data, scenario ground truth, research exports. **Adversaries:** curious participant (trying to see answers), external attacker, malicious insider.

| Threat (STRIDE) | Mitigation |
| --- | --- |
| Spoofing | Strong password hashing (Argon2id/bcrypt), rate-limited login, optional MFA for researcher role |
| Tampering | Server-side scoring only; signed session tokens; parameterized queries / ORM |
| Repudiation | Append-only audit log |
| Information disclosure | Ground truth never sent early; role-based access control; pseudonymized exports; TLS everywhere |
| Denial of service | Rate limiting, request size limits |
| Elevation of privilege | RBAC checks on every endpoint; researcher endpoints isolated |
| XSS | Escape/sanitize all rendered scenario text and free text; strict CSP |
| CSRF | SameSite cookies + CSRF tokens (if using cookie sessions) |
| Injection / prompt injection | Input validation (Pydantic), parameterized SQL, treat free text as data in LLM calls |
| Secrets leakage | Environment-based secrets, no keys in repo, secret scanning |
| Dependency risk | Dependabot/pip-audit/npm audit in CI |

Add: secure headers (HSTS, X-Content-Type-Options, frame-ancestors), safe error messages, minimal data retention, and a short `THREAT_MODEL.md` using OWASP Top 10 / ASVS as the checklist. Run OWASP ZAP or Semgrep once and report findings.

---

## 19. Ethics, privacy and safety

- **Everything is simulated.** No real phishing messages, links, credentials, OTPs, or real brands; fictional organizations only.
- **Consent screen:** purpose, what is recorded, voluntary, can withdraw, data deletion, contact.
- **Minimization:** no sensitive personal data; pseudonymous IDs; free text warns "do not enter real personal details".
- **Debrief:** explain deception-free design, show results, give resources.
- **Approval:** if you collect data from people for a "study," check whether your institution requires ethics/IRB review **\[VERIFY\]** before running it. If not obtainable, frame it as a *usability/pilot evaluation* and say so honestly.
- **No harm:** avoid shaming; frame feedback around strategies, not personal failures.
- **Dual-use:** do not publish ready-to-use malicious payload templates; scenarios are educational and labelled.

---

## 20. Evaluation deliverables

1. **System evaluation:** unit/integration tests, scoring-rule tests, schema validation tests, security scan results.
2. **Scenario quality check:** inter-rater agreement (two reviewers label truth + realism; report Cohen's κ).
3. **Pilot results:** tables and figures: verification rate by phase/arm, decision quality by mechanism, under/over-caution, d′, pressure effect, transfer.
4. **Limitations section:** honest.
5. **Reproducibility:** analysis notebook + anonymized dataset (if consent allows) + scenario set version.

---

## 21. Technology stack and repository structure

**Stack:** Next.js/React + TypeScript, FastAPI (Python), PostgreSQL, SQLAlchemy/Alembic, Pydantic, Docker Compose, pytest, Playwright (optional), pandas/scipy/statsmodels/matplotlib, LLM API with JSON-schema outputs (used offline for pre-generation).

```text
cyberpsyche/
├─ README.md
├─ docs/
│  ├─ PROJECT_SPEC.md        (this document)
│  ├─ THREAT_MODEL.md
│  ├─ STUDY_PROTOCOL.md      (pre-registration + analysis plan)
│  ├─ ETHICS_AND_CONSENT.md
│  └─ architecture.png
├─ frontend/
├─ backend/
│  ├─ app/{api,core,models,services,scoring,intervention}
│  ├─ scenarios/{schema.json,set_v1/*.json}
│  └─ tests/
├─ analysis/
│  ├─ notebooks/
│  └─ data/ (anonymized)
└─ docker-compose.yml
```

---

## 22. Build plan (10 weeks, adjustable)

| Week | Goal | Deliverable |
| --- | --- | --- |
| 1 | Finalize research question, schema, scoring rules; read core papers | `schema.json`, rules doc, reading notes |
| 2 | Write and review scenario set v1 (24-36) | Frozen scenario set + κ agreement |
| 3 | Backend skeleton: auth, DB, scenario service, session state machine | API + tests |
| 4 | Frontend: simulation view, evidence board, action + reasoning | Working baseline phase |
| 5 | Event logging, scoring engine, profile computation | Metrics verified by tests |
| 6 | Intervention module (targeted + generic), retest, transfer phases | End-to-end session |
| 7 | Security hardening, threat model, scan, deploy (e.g., cloud VM/Docker) | Hardened build + report |
| 8 | Dry-run with 3-5 friends; fix usability; freeze version | Pilot-ready |
| 9 | Run pilot (20-40 participants), monitor data quality | Dataset |
| 10 | Analysis, figures, 2-4 page write-up, README, demo video | Final package |

**Milestone discipline:** if behind, cut scenarios, delayed retest, or researcher dashboard polish, never the transfer test or evaluation.

---

## 23. Packaging for Master's applications

**Portfolio package**

- GitHub repo with polished README (problem, architecture diagram, screenshots, how to run, security notes)
- 2-4 page report: *Introduction → Related Work → Design → Study → Results → Limitations → Future Work*
- 2-3 minute demo video
- Threat model and study protocol
- Optional: arXiv-style preprint or workshop-style short paper (e.g., usable-security venues such as SOUPS poster/WIPs, or a university symposium) **\[VERIFY venues\]**

**CV entry template (fill with real numbers only)**

> **CyberPsyche: Decision-Process Laboratory for Social-Engineering Resilience** | Python, FastAPI, React, PostgreSQL, LLM APIs
> 
> - Built a full-stack simulation platform logging evidence-seeking, verification and decision quality across \[N\] scenarios and \[N\] manipulation mechanisms.
> - Designed a schema-constrained scenario engine in which an LLM varies wording while ground truth (malicious/genuine/ambiguous) stays fixed.
> - Implemented a baseline → intervention → retest → transfer pipeline; ran a randomized pilot (n=\[N\]) measuring \[X\] change in independent-verification and \[X\] transfer to unseen contexts.
> - Secured the application using OWASP Top 10/ASVS practices (authN/Z, input validation, rate limiting, privacy-minimal data).

**SOP paragraph (adapt)**

> "I became interested in why users remain the most exploited layer despite awareness training. I built CyberPsyche to measure not only whether people fall for social engineering, but how they investigate, verify and justify decisions, and whether short targeted training transfers to new contexts. The pilot showed \[result\], and its limitations (e.g., small self-selected sample, simulated stakes) led me to want to study this at scale with proper experimental controls, which motivates my interest in human-centred security and AI-assisted adaptive training."

**Likely interview questions to prepare:** Why transfer? How do you know scenario labels are valid? Why rules instead of LLM scoring? What did you find and what didn't work? Threats to validity? How would you scale it? What are the ethical risks of simulations?

---

## 24. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Scope creep | Freeze MVP list (Section 5); everything else goes to Future Work |
| Weak scenario quality | Peer review, κ agreement, pilot dry-run |
| Too few participants | Report as pilot; use within-subject design; show CIs |
| LLM inconsistency | Pre-generate, schema validate, human approval |
| Demand effects/practice effects | Counterbalancing, no per-item feedback in baseline |
| Ethics approval delays | Start early; fall back to usability evaluation framing |
| Time overrun | Weekly milestones; cut polish, not evaluation |

---

## 25. Future work (mention, don't build)

Additional mechanisms (fear, familiarity, reciprocity); voice and QR channels; live AI attacker with guardrails; adaptive scenario selection based on a learned vulnerability model; multi-language/regional scam adaptation; longitudinal retention (weeks/months); real-world field deployment with organizations; physiological or interaction-signal measures; comparison with commercial phishing-training baselines.

---

## 26. Starter references **\[VERIFY exact details before citing\]**

1. Cialdini, R. B. *Influence: The Psychology of Persuasion.*
2. Stajano, F., & Wilson, P. (2011). Understanding scam victims: seven principles for systems security. *Communications of the ACM.*
3. Kumaraguru, P., et al. PhishGuru / embedded training studies (CMU).
4. Lain, D., Kostiainen, K., & Čapkun, S. (2022). Phishing in organizations: findings from a large-scale and long-term study. *IEEE S&P.*
5. Sheng, S., et al. (2007). Anti-Phishing Phil: the design and evaluation of a game that teaches people not to fall for phish. *SOUPS.*
6. Green, D. M., & Swets, J. A. *Signal Detection Theory and Psychophysics.*
7. Barnett, S. M., & Ceci, S. J. (2002). When and where do we apply what we learn? A taxonomy for far transfer. *Psychological Bulletin.*
8. Kahneman, D. *Thinking, Fast and Slow.*
9. OWASP Top 10 and OWASP ASVS.
10. Open-source simulators for comparison (e.g., Pretexta, DECEIVER).

---

## Appendix A: Three sample scenario families

**A. Education/Career, Email, AUTH+URG**

- Malicious: fake placement cell, lookalike domain, `.pdf.exe`, 20-minute deadline.
- Genuine: real placement office, official domain, verifiable on portal, "register by Friday".
- Ambiguous: unfamiliar recruiter via official-looking portal message; some clues good, some missing.

**B. Finance, Chat/SMS, AUTH+URG**

- Malicious: "bank officer" asks to share OTP to stop account block.
- Genuine: bank alert advising to open the official app to confirm a transaction (no data requested).
- Ambiguous: refund notice from a merchant with partial order details matching.

**C. Social/Messaging, Chat, REW+URG**

- Malicious: friend's hacked account sends a "vote for me, enter your code" request.
- Genuine: friend asks to join a group using a link and you can call them to confirm.
- Ambiguous: classmate account messages from a new number with a scholarship form.

## Appendix B: Reason tags (controlled list)

Sender looked trustworthy · Message felt urgent · Opportunity seemed valuable · I verified independently · I noticed suspicious wording · I trusted the person's identity · I lacked enough evidence · I feared consequences · I didn't want to miss out · I was unsure · Other (free text)

## Appendix C: Glossary

**Under-caution:** unsafe trust/action on a malicious or unverified item. **Over-caution:** rejecting a genuine item without checking. **Independent verification:** confirming through a channel you initiated (official app/site/known number). **Transfer:** keeping the safer strategy in a new context/channel. **Calibration:** matching caution to the true risk. **d′ / c:** SDT sensitivity and response bias.
