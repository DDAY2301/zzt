# Deep audit, prioritization and evidence

## Audit scope
Identify affected product, user journeys, primary pages, framework, release status and stable baseline. Build a traceability map from user requirements to tests. Do not equate visual style markers with evidence of AI authorship.

### Ten audit lenses
1. **Project identity:** site purpose, audience, visual language, adherence to approved reference.
2. **Information architecture:** meaningful routes, discoverability, hierarchy and no dead ends.
3. **Visual craft:** type hierarchy, layout rhythm, alignment, color, spacing, imagery, responsive compositions, interaction states.
4. **Functional integrity:** links, navigation, search, forms, filters, calendar, error/empty/loading states.
5. **Code quality:** cohesion, typed contracts, duplication, tests, unnecessary dependencies, state ownership.
6. **Content credibility:** accuracy, natural language, citations, chronology, no invented testimonials/metrics.
7. **Accessibility:** keyboard/focus, contrast, semantic headings/labels, image alternatives, motion, zoom.
8. **Performance:** actual LCP/INP/CLS or local lab proxies; images, fonts, JS and caching.
9. **Security/privacy:** input validation, auth, secrets, safe logging, user data minimization.
10. **Provenance and licensing:** rights to assets/code, attribution, content origin records and legal disclosures.

## Defect register template
| ID | Scope | Expected | Observed evidence | Priority | Root cause / confidence | Minimal fix | Verification | Status |
|---|---|---|---|---|---|---|---|---|
| UI-001 | `/events` mobile | filter usable at 360px | screenshot shows clipped control | P1 | hard-coded width / high | use responsive width | viewport + keyboard test | OPEN |

**P0** Critical security, data loss, illegal attribution removal, irreversible breaking change.  
**P1** Main journey broken, severe accessibility blocker, fabricated claim, critical integration failure.  
**P2** Significant design inconsistency, maintenance debt, measurably weak page performance.  
**P3** Small polish, optional aesthetic refinement, low-risk microcopy issue.

## Evidence ladder
- **E0** Hypothesis (not inspected)
- **E1** Static code/text observation
- **E2** Built or unit-tested
- **E3** Browser/functional test observed
- **E4** Real integration or production outcome observed

Record evidence level for each important claim. Never promote evidence by inference (e.g., built != user journey works, green unit tests != live backend works).

## Output-quality rubric (0–100)
Assess each available axis on a 0–5 scale; weighted points = score/5 × weight. UNKNOWN is not zero; state coverage separately. Do not compute an overall grade if any critical axis is UNKNOWN or P0/P1 blocks the evaluated goal.

| Dimension | Weight | Evidence needed |
|---|---:|---|
| Design specificity and coherence | 20 | actual screens + approved design brief |
| Functional completeness | 20 | exercised required user journeys |
| Code reliability/maintainability | 15 | code inspection + tests |
| Content accuracy and naturalness | 15 | source references + editorial review |
| Accessibility | 10 | tools + manual keyboard/zoom/focus checks |
| Performance | 10 | reproducible measurements |
| Security, rights and provenance | 10 | applicable audit + asset records |

Mark result **DESIGN-REVIEW ONLY**, **IMPLEMENTED**, **TESTED**, **RELEASE CANDIDATE** or **PRODUCTION VERIFIED**; never skip an evidence stage. Aesthetic scores are informed professional assessments, not objective scientific measures.

## Change management / acceptance
Before: list immutable constraints, screenshot/test baseline, backups/Git status; define expected result. After: smallest diff, tests, visual comparison, no new critical issues, source/rights records retained, rollback method. Fix priority P0→P1→P2→P3. When no screenshot available, avoid false 'visual pass' claim.

## Skill design evaluation (separate from product assessment)
Scope/trigger clarity 20%, workflow effectiveness 20%, output reliability 20%, error handling 15%, test coverage 15%, context efficiency 10%. Scores from static review are not proof of runtime performance; run identical cases to compare v1 vs v2.
