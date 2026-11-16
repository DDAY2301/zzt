# Visual, UI copy and code quality patterns

## Design exploration (context-first)
Create a short project identity card: audience, information goals, emotion, visual references, things already approved, image rights and interaction needs. Never force an aesthetic because of presumed AI origins. Round corners, gradients, large headers, Inter and component grids are legitimate when purposeful; audit **misuse**, not existence.

### Visual craft checks
- **Typography:** no accidental monotony; readable text; hierarchy via weight/size/spacing; correct Slovenian diacritics where appropriate.
- **Grid:** purposeful alignment and widths; do not stretch content into empty megasections; editorial variety aligned to content purpose.
- **Color:** restrained palette with legible contrast; use brand colors consistently, not arbitrary decorative gradients.
- **Photos:** actual place/event/product; accurate alt text; correct license and credit; no irrelevant generic photos or invented documentary evidence.
- **Interaction:** state for loading/empty/error/hover/focus; keyboard navigation; link and button semantics; avoid clickable-looking inert elements.
- **Responsive:** check representative 360px, 390px, 768px, 1280px and 1440px widths, zoom and reduced motion when relevant. Sizes are examples, not a substitute for content-driven testing.
- **Content-density:** accessible scanability, no duplicated slogans, no filler panels, no placeholder counters/testimonials.
- **Consistency:** component contracts and design tokens coherent; enough variation to serve different content types.

### UI writing and factuality
Remove repetition and template phrases only when they diminish clarity. Write specific, human-readable and sourced descriptions. Verify legal names, dates, project stages, numbers, partners, quotations, event times and external links. No invention to fill empty cards. Never imply a draft project was funded or completed.

### Code observations (not origin detection)
Check for duplicated layout components, inconsistent state ownership, hardcoded UI fixture content in production, shadowed variables, dead branches, unused imports, arbitrary !important chains, excessive provider layers, hardcoded secrets, insecure integrations, absent tests and silent errors. Ignore stylistic markers when code is already readable, safe and appropriately tested.

### Provenance and obligations
Distinguish removable author-owned scratch comments from required copyright/licensing/attribution/provenance. C2PA Content Credentials concern verifiable provenance of media, not an aesthetic judgement. Preserve applicable disclosure and source records. Do not promise AI-undetectability.

### Measurement
For speed, use reproducible field/lab evidence. For accessible web UI, use WCAG 2.2 AA checks and real keyboard tests. For forms, test actual delivery only where explicitly authorized; unit tests or click animation alone do not establish delivery. For images, verify source rights and load behavior.
