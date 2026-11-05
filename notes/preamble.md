These Notes say how **our project** works with the [Transcription Principles](principles-framework.md): house style, tool settings, workflow, report format and suggestions for downstream editorial work. They are the local-notes layer for the Scores of Scores profile (`sos-2026-11`). Rules in the core are cited by ID, for example `read.preserve-errors`; the full list, with the strength each has in our profile, is the [rules table](principles-rules.md). These Notes replace the previous Transcription Guide (superseded; it survives in the repository history).

## How to read these Notes

- **Notes narrow, never override.** If a Note conflicts with a core rule or with the profile, the rule and profile win. Report the conflict so the Note can be fixed. A Note can never add a normalisation (`normalise.closed-list`).
- **Every Note has a kind:**
  - **presentation:** a choice among the normalisations the profile permits.
  - **tool:** settings and palette entries that may change between apps and versions.
  - **house:** a house convention (placement, scope, workflow, report format).
  - **editorial:** a suggestion for downstream editorial work. It is never applied in the version of record (VoR).
- **Each Note has a permanent ID,** `<area>.<slug>`, and may say which core rules it `applies` to. Earlier section-and-number codes from the previous guide are kept as aliases and listed in the concordance at the end.
- **This document is generated** from `notes/registry.yaml` by `python3 tools/build.py`. Edit the registry, not this file.
