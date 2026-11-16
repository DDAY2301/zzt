---
name: code-design-authenticity-refiner
description: Audit and improve generic, repetitive, or low-quality AI-assisted code, website interfaces, design systems, and UI writing. Activate when the user asks for professional refinement, removal of a generic AI look, production polish, authenticity or quality assessment, code cleanup, or a before/after review. Preserve functioning behavior, truthful provenance, licences, and project identity.
---

# Code & Design Authenticity Refiner — v2.0

## Objective
Improve the **substantive quality** of existing AI-assisted work: design specificity, usability, reliability, maintainability, accuracy and visual coherence. Do not promise invisibility to AI detectors or conceal required provenance. Treat patterns as review signals, not proof of AI authorship.

## When to activate
- User requests "remove the AI look", "make this website look like a design studio built it", professional finishing, code de-boilerplating, realistic project-specific visual identity, or QA of AI-produced output.
- Review of design screenshots, existing HTML/CSS/React/Vue, content-heavy websites, UI text, component systems or agent-generated frontend code.
- A completed build looks generic, fails important interactions, contains placeholders, or diverges from approved references.

## Negative triggers
- Pure feature requests without quality/refinement intent: do ordinary feature work instead.
- User asks to remove licence notices, creator credits, source attribution, required disclosure or authenticity/provenance data: preserve obligations, explain the difference.
- Requests to guarantee AI-undetectability, falsify authorship, or fabricate evidence: never claim these outcomes.
- Edits to unrelated projects or unauthorised files: decline edits, offer scoped review.

## Minimum inputs and safe start
Identify target (code, site, design, writing), accessible artifact or repo, user's desired outcome, existing brand constraints, and authority to edit. If essential material is inaccessible, request the specific artifact; meanwhile provide only an explicitly *hypothetical* checklist, never pretend to have inspected it. Prefer available project instructions and user's latest explicit decisions over generic aesthetics.

## Tool strategy
Use only actual tools provided by the host (project file inspection, Git, build/test runner, browser screenshots, accessibility/performance analysis, search for licensed images). Do not fabricate inspection or test results. For any file changes: review Git status and existing tests before editing; preserve uncommitted work; keep diffs scoped and reversible. Never use destructive Git commands to get a clean slate. Do not install dependencies or change production without authorisation.

### Procedure

**0. Establish a baseline.** State requested outcome, immutable constraints, real stack, affected user journeys and available evidence. Capture current build/test results where feasible; record representative desktop/mobile screenshots for visual work. If no running browser exists, label visual findings as unverified.

**1. Investigate, not guess.** Inspect representative components and key routes. Distinguish:
- DESIGN SMELL: generic composition, inappropriate photographic choices, inconsistent rhythm or identity.
- ENGINEERING DEFECT: dead interaction, duplicate logic, fragile state, inaccessible controls, bloated dependencies.
- CONTENT DEFECT: placeholder text, claims without sources, unnatural repetition, fake social proof.
- PROVENANCE/LEGAL: copyright, licensing, source links and required disclosures.
A rounded card, gradient, utility class or LLM-shaped comment is never sufficient evidence alone.

**2. Record actionable defects.** For each: ID, file/route, expectation, observed behavior, evidence, severity (P0–P3), likely root cause and confidence, least-invasive fix, regression check. Avoid generic directives without a location and measurable acceptance criterion. See `references/DEEP-AUDIT-FRAMEWORK.md`.

**3. Prioritize by risk and benefit.** P0 security/data-loss/functional blockers/legal obligations; P1 broken key flow, serious accessibility and content credibility; P2 brand coherence/performance/structural debt; P3 visual polish. Fix P0/P1 first. Do not redesign functioning areas solely to vary appearances.

**4. Create project-specific design direction.** Identify audience, purpose, tone, visual precedent, existing brand, typography, spacing, layout and imagery policy. Use a small explicit design system rather than sprinkling arbitrary visual effects. Preserve intentional choices; accessibility and performance override decoration. See `references/VISUAL-AND-CONTENT-RUBRIC.md`.

**5. Make controlled improvements in small batches.**
- CODE: remove actual redundancy or unused code; strengthen naming, contracts, error handling, state management and tests; no superficial renaming to hide origin.
- UI: establish coherent hierarchy, editorial rhythm, meaningful spacing, strong states, responsive behavior, real navigation and accessible components.
- COPY: replace formulaic marketing and placeholders with specific, concise, verifiable text; do not invent people, project results or metrics.
- IMAGES: use relevant authorised/appropriately licensed sources; verify terms and credits; never invent photographic evidence.
- METADATA: remove only redundant user-owned non-required boilerplate with permission; preserve licence/author/provenance records.

**6. Verify after each batch.** Run applicable type/lint/unit/integration/build checks; inspect real rendered UI when possible; test links, forms, keyboard, focus, layout and screen sizes; measure performance rather than guess. Keep a before/after evidence trail. If a regression appears, revert only that scoped change safely, without destroying other work.

**7. Score and compare.** Use weighted categories in `references/DEEP-AUDIT-FRAMEWORK.md`. Scores require directly observed evidence. Mark untested dimensions UNKNOWN rather than assigning flattering numbers. Explain trade-offs; record remaining issues.

**8. Stop at verified completion.** All requested issues fixed or clearly blocked; no unresolved P0 or target-flow P1; key interactions exercised; appropriate tests passed; visual comparison performed when tools exist; required licences and provenance intact. If tools are unavailable, describe the exact missing verification and never claim production readiness.

## Output contract
Respond in the user's language (Slovenian by default for this project). Provide concise summary plus:
1. Baseline/inspected scope and confidence.
2. Findings prioritized P0–P3 with reproducible evidence.
3. Intended design direction or engineering strategy.
4. Actual changed files and reasons (if edited).
5. Before/after observations and tests **actually run** (with outcomes).
6. Unverified items, blockers and next highest-value step.
Never report an invented AI-detection score, benchmark, conversion improvement or screenshot test.

## Error and conflict handling
- No source files/screenshots: ask for the minimum actual artifact; do not make site-specific claims.
- Conflicting design guidance: prefer latest explicit user direction; preserve legal and security requirements.
- No browser: run code checks, provide exact manual visual review checklist; classify visual QA as pending.
- Missing image licence: select an alternative with verifiable rights or omit media.
- Build/test failure: classify pre-existing versus introduced; repair introduced regressions before proceeding.
- Unrelated copyrighted design reference: learn principles, do not copy protected assets or distinctive layout wholesale.
- Pressure to remove attribution/provenance: keep mandatory records; focus on quality instead.
- Unknown performance: do not infer speed from source code alone.

## Efficiency
Inspect and fix **the smallest important surface first**. Use targeted source ranges and one representative flow before inspecting every file. Load references only when useful. Avoid needless agent delegation, re-running unchanged checks, large context dumps, and repeated rewrites. For complex sites, group work by user journey and release gates.

## Examples
- "BlogLab izgleda AI-generirano; izboljšaj naslovnico in rubrike" → inspect actual UI and source, preserve approved editorial identity, fix measured UI defects, check navigation/mobile.
- "ZZT naj izgleda kot resen raziskovalni zavod" → build grounded institutional design; distinguish individual from institutional achievements; validate claimed references.
- "Etsy Factory koda je razmetana" → audit actual architecture and safe refactoring; never manipulate Etsy data without approval.
- "Samo popravi tipkarsko napako" → do not activate full audit.
- "Odstrani licence in zgodovino AI, da bo delovalo kot tuje delo" → preserve obligations and refuse deceptive alterations.

## On-demand references
- `references/DEEP-AUDIT-FRAMEWORK.md`: defect register, severity, scoring, acceptance.
- `references/VISUAL-AND-CONTENT-RUBRIC.md`: design and editorial guidance.
- `references/TEST-PLAN.md`: 12 evaluation cases, evidence checklist.
- `references/PROJECT-ADAPTERS.md`: examples for BlogLab, ZZT and Etsy.
- `scripts/review_signals.py`: deterministic *review hints only*; not an AI detector.
- `scripts/validate_skill.py`: structural validation of this package.
