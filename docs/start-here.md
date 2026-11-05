# Start here

*Version 2026-11 (draft). A short orientation to the Transcription Principles and the Notes for Transcribers, for people meeting them for the first time.*

## What this is

Scores of Scores aims to give the public domain repertoire an open, citable digital encoding. Each score is transcribed from one printed source, exactly as that source prints it, so that other people and programs can build on it without having to check it against the page first.

This repository holds the **rules** that make such a transcription trustworthy. They are written so that another project can adopt them and make different choices.

## Who it is for

- **Transcribers and reviewers** follow the rules and the local Notes day to day.
- **Editors and editorial projects** build on the result. Because a transcription never chooses between readings, corrects, completes or interprets, an edition can start from a fixed, exact record and keep its own decisions separate and visible.
- **Other projects** can adopt the core rules unchanged and write their own profile.

## Five ideas that explain the rest

1. **A transcription records; it does not edit.** Errors in the source are kept as printed and flagged, never fixed silently (`read.preserve-errors`, `stance.judgement-stays-out`).
2. **There are three tiers of decision.** *Transcription* needs no musical judgement and no second source. *Presentation* is systematic, reversible and changes nothing notated. *Editorial* needs judgement or another source, and is not done in the transcription.
3. **Presentation choices are a closed list.** Only the registered normalisations (`normalise.*`) are allowed, each one stated once per transcription. Nothing can be added locally (`normalise.closed-list`).
4. **When in doubt, preserve.** If it is unclear which tier a decision falls in, treat it as editorial: keep what the source prints, flag it, ask a reviewer (`stance.doubt-means-preserve`).
5. **What was deviated from is always reported.** The score together with its report is enough to recover what the source prints (`declare.report-deviations`).

## How the documents fit together

| Layer | What it holds | Where |
|---|---|---|
| Core | The rules, how they relate, the three tiers | [Principles framework](principles-framework.md) and [rules table](principles-rules.md) |
| Profile | A project's choices: how strong each rule is, which wins in a conflict, what is out of scope | The profile `sos-2026-11` (shown in the rules table) |
| Local notes | Tool settings, house style, workflow, report format, suggestions for editors | [Notes for Transcribers](notes-for-transcribers.md) |

Every rule and every Note has a permanent ID (for example `read.preserve-errors` or `workflow.ask-reviewer`). Cite by ID. Notes may narrow what the profile allows but never override it.

## If you are building an edition on top of this

Start from a pinned version of the transcription, work in your own project, and record every change there, using an established scheme such as the editorial markup in MEI or TEI. The Notes in the area *Editorial matters* (`editorial.*`) say how observations made during transcription are handed on, and which kinds of intervention (harmonising parts, suggested accidentals, choosing between sources, dropping the source's own brackets) belong to you rather than to the transcription.

## Glossary

| Term | Meaning |
|---|---|
| **VoR** | Version of record: the exact transcription of one source, errors included, identified by a pinned version. |
| **Tier** | Transcription, presentation or editorial: the three kinds of decision. |
| **Normalisation** | A registered presentation choice (for example beam grouping or clefs). The list is closed. |
| **Profile** | A project's choices over the core rules. |
| **MUST, SHOULD, MAY, OFF** | The strength of a rule in a profile. MUST: always. SHOULD: unless there is a recorded reason. MAY: at discretion. OFF: not adopted. |
| **Note kinds** | *Presentation* (a choice among permitted normalisations), *tool* (settings that may change between apps), *house* (a house convention), *editorial* (a suggestion for downstream work, never applied in the VoR). |
| **Sidecar** | The machine-readable metadata stored with each transcription: source, pages, tools, versions, and the normalisations applied. Its schema is not yet public. |
| **Corrections layer** | A separate layer for proposed fixes to clear source errors. The VoR keeps the error as printed; the corrected view is derived from the two. |
| **Mark category** | A kind of printed mark that is not transcribed by default (currently fingering, which some basic encoding formats do not express). Its treatment (transcribed, editorial or unsupported) is set in the core and can be reclassified by a profile. |
| **Observation** | Something a transcriber noticed (a likely error, a divergence between parts) recorded in the report, not acted on in the score. |

## Status

This is a draft (version 2026-11). The Notes list topics not yet covered, such as lyrics, pedalling, articulations, repeats and ornaments other than grace notes; until they are written, ask your reviewer and record the decision in the report (`workflow.ask-reviewer`). Manuscripts are out of scope for this profile.
