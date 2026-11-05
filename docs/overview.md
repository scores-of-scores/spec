# Scores of Scores: project overview

*Overview and document map. Consolidated draft, 2026-11-03. This is the wider project picture; documents marked "not yet public" are in preparation. For the published rules, start with [Start here](start-here.md).*

Scores of Scores aims to provide an open, clear, digital encoding of the out-of-copyright works (and most editions) on IMSLP, stored so that people and programs can rely on, cite and improve them. This folder holds the project's governing documents as Markdown (and YAML and JSON), the single source from which other formats can be built.

## Scope

| | |
|---|---|
| **Input** (assumed, not owned) | The source PDF. We reference it by ID and hash and record the pages where each transcription sits. We don't host or control the scans. |
| **What we produce** | Exact, pragmatically faithful transcriptions of one source each, as a version of record (VoR) in KRN, with metadata and an editorial report. A separate corrections layer for clear source errors. Derived files (MusicXML, SVG and so on). |
| **What we provide to others** | A reliable, citable foundation for downstream work: pinned versions (`work@version`), hashes, and an optional judgement-free comparison between transcriptions of the same work. |
| **What we run** | A platform of ~28K composer repos, an index, a public site and API, a review and corrections workflow, and long-term preservation (trust levels, signed releases, fixity, archiving). |
| **Out of scope** | Editorial work of any kind (critical or performing editions, choosing between readings, apparatus, performance practice) and hosting the source scans. |

## How the rules are organised

Three layers, so that the core can be adopted by other projects with different priorities:

| Layer | Holds | File |
|---|---|---|
| **Core registry** | The rules, their domains and themes, how they relate (refines, exception-of, requires, tension-with), the three tiers | `principles/registry.yaml` |
| **Profile** | Our choices: strength of each rule (MUST, SHOULD, MAY, OFF), ranked aims, which rule wins in each tension, scope | `profiles/sos-2026-11.yaml` |
| **Local notes** | Tool settings, placement, workflow, report format, editorial suggestions | `docs/notes-for-transcribers.md` |

Rules are cited by permanent ID, `domain.slug` (for example `read.preserve-errors`, `normalise.clef`). The domains are `stance`, `read`, `encode`, `normalise` and `declare`. `python3 tools/build.py` validates the registry, profile and notes and generates the rules table, the Notes document, JSON files and a CSV.

## The documents

| Document | Answers | Audience | Status |
|---|---|---|---|
| [Principles framework](principles-framework.md) | How the Principles work: layers, tiers and boundary test, rule anatomy, relations, identity, related standards | Anyone, including other projects | Version 2026-11, draft |
| [Rules table](principles-rules.md) (generated) | Every rule, by domain and theme, with strength, relations, priorities and a concordance with earlier codes | Transcribers, reviewers, other projects | Generated |
| [Notes for Transcribers](notes-for-transcribers.md) | How our project works day to day. Each Note has a permanent ID and a kind: presentation, tool, house or editorial | Transcribers and reviewers | Version 2026-11, draft |
| Platform Design (not yet public) | Where do files live, and how do people reach, search and improve them? | Developers, maintainers | Draft 2 |
| VoR Management Plan (not yet public) | What makes a file a version of record, how does it change, and how do we keep it trustworthy at scale? | Maintainers, stewards, developers | Draft 3 |
| [Schemas](../schemas/) | Principles registry, profile and notes registry published; sidecar (with PDF page ranges), errata and comparison schemas not yet public | Developers, CI | Version 1, draft |

```
Source PDF ──► Principles (core + profile) ──► Transcription (KRN, exact) ──► VoR (versioned, signed)
                      ▲                                │                            │
              Local notes (tools,                      ├─► Errata layer ────────────┤
              workflow, report format)                 │                            ▼
                                                       └─► Derived files ──► Platform (index, site, API)
                                                                                    │
                                              Downstream editions ◄─────────────────┘  (pin work@version; out of scope)
```

## Settled in this draft

- **The VoR is the exact transcription,** errors included. Corrections are a separate layer; the corrected view is derived (VoR plan, section 6).
- **Core, profile and local notes are separate.** The core defines the rules and how they relate. The profile sets strengths and resolves every tension (the build fails if one is left unresolved). Notes may narrow but never override.
- **A closed list of presentation normalisations** (`normalise.*`) is the formal line between presentation and editorial. Each transcription records which it applied.
- **Rules have permanent slugs,** with only the domain in the ID. Priority is stated as data in the profile, not implied by numbering.
- **Fingering is unsupported by default** (a mark category in the core registry, outside what some basic encoding formats express; a profile can reclassify it), and the five domains and the rule slugs are fixed for version 2026-11.
- **Editorial matters are out of scope,** apart from an optional, judgement-free comparison view.
- **Version numbers mean something checkable** (MAJOR for structure, MINOR for notated content, PATCH for everything else), with trust levels T0 to T3 shown separately.
- **Derived files live in the object store** under content-addressed keys, not in git (VoR plan, section 8).
- **Page information** is recorded as physical PDF page ranges per source file; bounding boxes are not part of the VoR.

## Open decisions

| Where | Question |
|---|---|
| VoR plan D6 | Minimum trust level for a first release (`1.0.0`) |
| VoR plan D7 | DOIs for snapshots only? |
| VoR plan D8 | Withdrawal and takedown policy (needs legal review) |
| VoR plan D9 | Licence for transcriptions and contributions |
| VoR plan D10 | Who sits on the steward group, and how it is chosen |
| VoR plan D11 | Default view on the work page (as printed, or with corrections) |
| Registry | Whether the source's own brackets should be kept in the encoding or only recorded (`read.record-source-marks`) |
| Notes G6, N | Manuscripts, and the topics listed as not yet covered |
| Design 6 | Granularity of "work"; performance of large scores in CI |

## Reading order

- **New transcriber:** Principles framework (sections 1 to 3), the rules table, then the Notes.
- **Reviewer:** the above, then the VoR plan sections 4 to 6.
- **Developer or maintainer:** Platform Design, then the VoR plan, registry and schemas.
- **Another project adopting the Principles:** Principles framework, then `principles/registry.yaml`; write your own profile.
- **Steward or funder:** this README, then the VoR plan sections 1, 9 to 16.

## Conventions across the documents

- **Rule IDs:** `domain.slug`, permanent, never reused. Earlier `TP` codes survive as aliases in the registry and the rules table's concordance.
- **Notes** have permanent IDs of the form `area.slug` (for example `workflow.ask-reviewer`); the previous guide's codes (`T2.2.1`) survive as aliases. The VoR plan and Platform Design are cited by section number. Decisions in the plan are `D1` to `D12`.
- **Versions:** the Principles and Notes use date versions (YYYY-MM). Each transcription records `principles_version`, `profile`, `notes_version` and the `normalisations` applied.
- **Identifiers:** the composer authority ID is a Wikidata Q-ID, shown only as a placeholder in these documents.

## Not yet written

- A light scheme for editorial interventions (aligned with MEI and TEI vocabulary and pinned to `work@version`); the corrections layer is its first case.
- A changelog schema for the release bot.
- A documentation build (Pandoc to PDF, HTML and Word) with a check that cross-references resolve.
- Any separate proposal for a funder or venue.
