# Changelog

## 2026-11

Baseline release, consolidating the Principles, the format comparison and the paper into one structure.

- **Layers.** Core (`core/`), formats (`formats/`), profiles (`profiles/`) and local notes (`notes/`), one build, one ID namespace.
- **Formats.** The comparison dataset is now YAML (one file per category), with IDs `fmt.<slug>`, a `subset` field (was `profile`), computed `tested`, and fixtures in place of the test plan. New features: `fmt.fingering`, `fmt.stem-direction`, `fmt.time-signature-symbol`. Five fixtures are the paper's worked examples.
- **Core.** New domain `correct` (`correct.error-test`, `correct.in-place`, `correct.layer`, `correct.record`). New rules `declare.observations` and `read.ambiguous-marks`. Rules link to format features through `format_features`. Mark category treatment is derived from the formats data. `read.record-source-marks` states where the printed mark is kept.
- **Wording.** "Ask a reviewer", "flag" and "evident" are replaced by observations and the clear-error test. `workflow.ask-reviewer` is now `workflow.unclear-cases`, `workflow.report-transfer` is merged into `workflow.red-text`, and `editorial.comparing-sources` is now `editorial.collation`. The Notes' "not yet covered" list is "Outside this version".
- **Profiles.** `sos-2026-11` names its format, dialect and accepted extension. `openscore-2026-11` is a draft from OpenScore's published statements.
- **Build.** `requires` is now checked against strengths in every profile; accepted extensions are checked against the formats data; fixtures' expected treatments are checked against the derivation.
