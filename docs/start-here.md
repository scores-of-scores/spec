# Start here

*Version 2026-11. A short orientation to the Transcription Principles, the format evidence and the Notes for Transcribers, for people meeting them for the first time.*

## What this is

Scores of Scores aims to give the public domain repertoire an open, citable digital encoding. Each score is transcribed from one printed source, exactly as that source prints it, so that other people and programs can build on it without having to check it against the page first.

This repository holds the **rules** that make such a transcription trustworthy, the **evidence** of what each encoding format can express, and the **profiles** that record two projects' different choices over the same rules. The rules are written so that another project can adopt them and make different choices.

## Who it is for

- **Transcribers and reviewers** follow the rules and the local Notes day to day.
- **Editors and editorial projects** build on the result. Because a transcription never chooses between readings, completes or interprets, an edition can start from a fixed, exact record and keep its own decisions separate and visible.
- **Other projects** can adopt the core rules and the formats data unchanged and write their own profile.

## Six ideas that explain the rest

1. **A transcription records; it does not edit.** Errors in the source are kept as printed and recorded as observations, never fixed silently (`read.preserve-errors`, `stance.judgement-stays-out`).
2. **There are three tiers of decision.** *Transcription* needs no musical judgement and no second source. *Presentation* is systematic, reversible and changes nothing notated. *Editorial* needs judgement or another source, and is not done in the transcription.
3. **Presentation choices are a closed list.** Only the registered normalisations (`normalise.*`) are allowed, each one stated once per transcription (`normalise.closed-list`).
4. **When in doubt, preserve.** If it is unclear which tier a decision falls in, keep what the source prints and record an observation (`stance.doubt-means-preserve`, `declare.observations`).
5. **Only a clear error can be corrected, and a test decides what is clear.** The test is in the core (`correct.error-test`). A profile chooses whether a correction is made in the transcription or in a separate layer, and every correction is recorded (`correct.in-place`, `correct.layer`, `correct.record`).
6. **The format sets the limit.** What a format cannot express is derived from the formats data, not asserted, and a deviation from the source is always reported (`declare.report-deviations`).

## How the documents fit together

| Layer | What it holds | Where |
|---|---|---|
| Core | The rules, how they relate, the three tiers | [Principles framework](principles-framework.md) and [rules table](principles-rules.md) |
| Formats | What four formats can express, linked to the rules | [Format support](format-support.md) and the [format reader](../site/formats.html) |
| Profile | A project's choices: strengths, precedence, aims, format of record | The profiles `sos-2026-11` and `openscore-2026-11`, shown in the rules table |
| Local notes | Tool settings, house style, workflow, report format | [Notes for Transcribers](notes-for-transcribers.md) |

Every rule, Note, format feature and fixture has a permanent ID. Cite by ID. Notes may narrow what the profile allows but never override it. The terms are defined in the [glossary](glossary.md).

## If you are building an edition on top of this

Start from a pinned version of the transcription, work in your own project, and record every change there, using an established scheme such as the editorial markup in MEI or TEI. The Notes in the area *Editorial matters* (`editorial.*`) say which kinds of intervention (harmonising parts, suggested accidentals, choosing between sources, dropping the source's own brackets) belong to you rather than to the transcription.

## Scope of this version

Version 2026-11 covers printed sources in the KRN version of record. Lyrics, piano pedalling, articulations, repeats, rehearsal marks, hairpins, ornaments other than grace notes, and courtesy accidentals already in the source have no Note yet; for them the core rules apply unchanged. Manuscripts are out of scope.
