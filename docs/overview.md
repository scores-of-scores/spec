# Scores of Scores: project overview

*Version 2026-11. The wider project picture and the map of its documents. Documents marked "not yet public" are in preparation. For the published rules, start with [Start here](start-here.md).*

Scores of Scores provides an open, clear, digital encoding of the out-of-copyright works (and most editions) on IMSLP, stored so that people and programs can rely on, cite and improve them. This repository holds the project's governing documents as Markdown (and YAML and JSON), the single source from which other formats are built.

## Scope

| | |
|---|---|
| **Input** (assumed, not owned) | The source PDF. It is referenced by ID and hash, and the pages where each transcription sits are recorded. The scans are neither hosted nor controlled. |
| **What we produce** | Exact, pragmatically faithful transcriptions of one source each, as a version of record (VoR) in KRN, with metadata and an editorial report. A separate layer of corrections for clear source errors (`correct.layer`). Derived files (MusicXML, SVG and so on). |
| **What we provide to others** | A reliable, citable foundation for downstream work: pinned versions (`work@version`), hashes, a judgement-free collation of transcriptions of the same work, and the format evidence in `formats/`. |
| **What we run** | A platform of about 28K composer repos, an index, a public site and API, a review and corrections workflow, and long-term preservation (trust levels, signed releases, fixity, archiving). |
| **Out of scope** | Editorial work of any kind beyond the clear-error correction (critical or performing editions, choosing between readings, apparatus, performance practice) and hosting the source scans. |

## How the project is organised

Four layers, so that the core can be adopted by other projects with different priorities and different formats:

| Layer | Holds | Where |
|---|---|---|
| **Core** | The rules, their domains and themes, how they relate, the three tiers, the glossary | `core/` |
| **Formats** | What KRN, MusicXML, MuseScore's native format and MEI can express, with evidence, sources and fixtures | `formats/` |
| **Profile** | A project's choices: strengths, precedence, ranked aims, format of the version of record, scope | `profiles/` |
| **Local notes** | Tool settings, placement, workflow, report format, editorial suggestions | `notes/` |

Rules are cited by permanent ID, `domain.slug` (for example `read.preserve-errors`, `normalise.clef`); format features by `fmt.slug`. `python3 tools/build.py` validates the layers and the links between them and generates the documents, the data files, the format reader and the paper's tables.

```
Source PDF ──► Principles (core + profile, with format evidence) ──► Transcription (KRN, exact) ──► VoR (versioned, signed)
                      ▲                                                       │                            │
              Local notes (tools,                                             ├─► Corrections layer ───────┤
              workflow, report format)                                        │                            ▼
                                                                              └─► Derived files ──► Platform (index, site, API)
                                                                                                           │
                                                     Downstream editions ◄─────────────────────────────────┘  (pin work@version; out of scope)
```

## The documents

<!-- BEGIN docmap -->
| Document | Answers | Audience |
|---|---|---|
| [Start here](../docs/start-here.md) | A short orientation to the rules and how they fit together | Everyone |
| [Principles framework](../docs/principles-framework.md) | How the layers work, the tiers and boundary test, rule anatomy, relations, derived treatments, versioning, adoption | Anyone, including other projects |
| [Rules table](../docs/principles-rules.md) | Every rule, with its strength and relations in each profile, priorities and scope (generated) | Transcribers, reviewers, other projects |
| [Format support](../docs/format-support.md) | What each of four formats can express for each rule, and what follows in each profile (generated) | Profile authors, transcribers |
| [Format reader](../site/formats.html) | The full formats dataset as a searchable matrix, with worked cases and sources (generated) | Anyone choosing or comparing formats |
| [Notes for Transcribers](../docs/notes-for-transcribers.md) | Day-to-day local notes for the Scores of Scores profile (generated) | Transcribers and reviewers |
| [Glossary](../docs/glossary.md) | The terms used across the documents (generated) | Everyone |
| [Project overview](../docs/overview.md) | Scope, pipeline and conventions of the wider project | Developers, maintainers, funders |
| [Paper](../paper/paper.md) | The framework, the two worked positions and the evidence for them | Researchers |
<!-- END docmap -->

| Not yet public | Answers | Audience |
|---|---|---|
| Platform Design | Where do files live, and how do people reach, search and improve them? | Developers, maintainers |
| VoR Management Plan | What makes a file a version of record, how does it change, and how do we keep it trustworthy at scale? | Maintainers, stewards, developers |

The schemas in [`schemas/`](../schemas/) cover the core registry, profiles, Notes registry, formats data and glossary. The sidecar schema (with PDF page ranges) and the corrections-layer schema are not yet public.

## Conventions

- **The VoR is the exact transcription,** errors included. A corrected view is derived from the transcription and the corrections layer.
- **Rule IDs:** `domain.slug`, permanent, never reused. Earlier `TP` codes survive as aliases in the registry and the rules table's concordance. Notes have IDs of the form `area.slug`; the previous guide's codes (`T2.2.1`) survive as aliases.
- **Versions:** the Principles, the formats data and the Notes use date versions (YYYY-MM). Each transcription records `principles_version`, `profile`, `notes_version` and the `normalisations` applied. Transcription version numbers mean something checkable: MAJOR for structure, MINOR for notated content, PATCH for everything else. Trust levels T0 to T3 are shown separately.
- **Derived files** live in the object store under content-addressed keys, not in git (VoR plan, section 8).
- **Page information** is recorded as physical PDF page ranges per source file. Bounding boxes are not part of the VoR.
- **Identifiers:** the composer authority ID is a Wikidata Q-ID, shown only as a placeholder in these documents.

## Reading order

- **New transcriber:** Principles framework (sections 1 to 3), the rules table, then the Notes.
- **Reviewer:** the above, then the VoR plan sections 4 to 6.
- **Developer or maintainer:** Platform Design, then the VoR plan, the core registry and schemas.
- **Another project adopting the Principles:** Principles framework, then `core/principles.yaml` and `formats/`; write your own profile.
- **Choosing a format:** the format reader, then Format support.
- **Steward or funder:** this overview, then the VoR plan sections 1, 9 to 16.
