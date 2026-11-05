# Transcription Principles: framework

*How the Principles are organised and used. Version 2026-11 (draft). Part of the Scores of Scores document set (see the README). The rules themselves are in the generated [rules table](principles-rules.md).*

## 1. What this is

The Principles are a small, tool-neutral framework for a **pragmatically faithful transcription** of a notated source into a digital encoding. They say what a transcription must and must not do, and what it must declare. They are written so that another project can adopt the core and make different choices.

**The encoding sets the limit.** A transcription is made in a particular encoding format, and the Principles apply within what that format can express (`stance.faithful-reading`: "as exactly as the encoding allows"). Where a detail cannot be represented, the nearest available form is used (`read.ornaments-as-printed`, `read.standard-instructions`); where a whole category of printed mark cannot, the profile classes it as *unsupported* (see Mark categories in section 4). This is a limit of the format, not a judgement, so it is not an editorial matter, and it is revisited when the format changes.

**Out of scope:** editorial work (choosing between readings, correcting, completing, interpreting, comparing sources, performance practice) and manuscripts and other special sources, which need further rules.

## 2. Three layers

| Layer | Holds | Changes | Where |
|---|---|---|---|
| **Core** | The rules: what a transcription could be required to do, how rules relate (refines, exception, requires, tension), the tiers, the vocabulary | Rarely | `principles/registry.yaml` |
| **Profile** | A project's choices: how strong each rule is, which rule wins in a tension, ranked aims, what is out of scope | When the project decides | `profiles/sos-2026-11.yaml` |
| **Local notes** | Tool settings, placement defaults, workflow, report format, suggestions for downstream work | Often | `docs/notes-for-transcribers.md` |

**Where does a rule belong?** If a reasonable project could reject it, it is a profile choice, not core. Even "preserve errors" is a stance, because emending is the classic opposing view: the core defines the rule, and each profile decides whether to adopt it. Local notes may narrow what the profile allows, never widen it.

## 3. Tiers and the boundary test

Every decision falls into one of three tiers (defined in the registry):

| Tier | Test | Allowed in the transcription? |
|---|---|---|
| **Transcription** | A competent reader could do it from the source and a stated notational convention, with no musical judgement and no second source | Yes |
| **Presentation** | Systematic, reversible, changes nothing notated, stated once in the report | Only the registered normalisations (`normalise.*`) |
| **Editorial** | Needs musical judgement or another source | No |

Three questions, in order:
1. Does it change what is notated (a pitch, rhythm, mark or text)? If yes, it is not presentation.
2. Could it be done from the source and a stated convention alone? If yes, it is transcription; if no, it is editorial.
3. Is it systematic, reversible and reported once, and is it registered under `normalise`? If yes, it is presentation.

If it is unclear, treat it as editorial (`stance.doubt-means-preserve`).

| Situation | Tier | Handling |
|---|---|---|
| The source's convention makes an accidental implicit and the encoding needs it explicit | Transcription | Add it and mark it (`declare.mark-additions`) |
| Cut-time symbol printed | Transcription | Keep it (`read.preserve-distinctions`) |
| One part has a different articulation from the others | Editorial | Keep as printed (`read.consistency-by-equivalence`) |
| A note is evidently wrong | Editorial | Keep as printed and flag (`read.preserve-errors`) |
| An edition beams every 6/8 bar the same way | Presentation | Normalise (`normalise.beam-grouping`) |
| The composer groups beams unusually in one passage | Transcription | Keep (`read.composer-led-grouping`) |
| An editor might add a suggested accidental (musica ficta) | Editorial | Do not add |
| Cello treble clef that sounds an octave lower than written | Presentation | Notate at sounding pitch (`normalise.clef`) |

## 4. Anatomy of a rule

Each rule in the registry has:

| Field | Meaning |
|---|---|
| `id` | `<domain>.<slug>`, permanent |
| `theme` | A mid-level grouping within its domain (metadata, not part of the ID) |
| `kind` | `obligation` (a do or don't) or `permission` (a registered normalisation) |
| `title`, `statement` | A strength-neutral imperative; the profile supplies the strength |
| `relations` | `refines`, `exception-of`, `requires`, `tension-with`, `see-also` |
| `rationale`, `examples` | Why, and worked cases |
| `aliases` | Earlier codes, for traceability |
| `status` | `active`, `proposed` or `retired` (retired rules name `replaced_by`) |

### Domains

`stance` (what a transcription is), `read` (what is read), `encode` (how it is encoded), `normalise` (the closed menu of presentation choices), `declare` (what is marked, reported and recorded). The domain is the only hierarchy in the ID. Themes are metadata, so a rule can be re-themed without a rename.

### Relations

| Relation | Meaning | Consequence |
|---|---|---|
| `refines` | A more specific form of another rule | Never conflicts |
| `exception-of` | Limits another rule in a stated scope | Wins over it in that scope, in every profile |
| `requires` | Cannot be adopted without the other | Checked by the build |
| `tension-with` | Can pull against the other | **The profile must resolve every tension** (checked by the build) |
| `see-also` | Related | None |

### Mark categories

Some printed marks are not transcribed by default. The registry lists these categories (`mark_categories`), each with a default treatment: *transcribed*, *editorial* (needs judgement or another source) or *unsupported* (outside what the encoding format expresses). At present the only category is fingering, which is unsupported by default because it is outside the remit of some basic encoding formats. A profile can reclassify a category in `scope.marks`, with a reason, for example when the format gains support for it; the rules table shows the treatment in force. Any printed mark outside a listed category is transcribed (`read.transcribe-all-marks`). A project that needs another category proposes it for the registry, as for a rule.

### Strengths

Set by the profile, using the BCP 14 terms (RFC 2119, RFC 8174), in capitals only where they are normative: **MUST**, **SHOULD**, **MAY**, **OFF** (not adopted; for a normalisation, not permitted).

## 5. Identity and change

- IDs are **never renumbered and never reused**. If a rule's meaning changes materially it gets a new ID and the old one is retired with `replaced_by` and a date. Editorial rewording keeps the ID.
- The Principles carry a date version (YYYY-MM) and a changelog. Cite a rule as `read.preserve-errors` or, where precision matters, `read.preserve-errors@2026-11`.
- Each transcription records `principles_version`, the `profile` it followed, and the `normalisations` it applied (the sidecar; see `declare.record-provenance`). Changes are not retroactive.
- **Build.** `python3 tools/build.py` validates the registry, the profile and the local notes, and generates the rules table, the Notes document, JSON files and a CSV. It fails if a relation target is missing, a theme belongs to another domain, a tension has no precedence, precedence has a cycle, an active rule has no strength, or an alias is used twice.

## 6. Adopting the Principles elsewhere

1. Take `principles/registry.yaml` unchanged.
2. Write a profile (see the table below): a strength for every active rule, a resolution for every tension, your ranked aims and your scope.
3. Run the build; fix what it reports.
4. Write local notes for your tools and workflow.

| A profile chooses | Profile field |
|---|---|
| The strength of every active rule | `strengths` |
| Which rule wins in each tension | `precedence` |
| Ranked aims | `aim_order` |
| The treatment of each category of printed mark | `scope.marks` |
| The encoding format of the version of record | `scope.encoding` |
| Source types not yet covered | `scope.unsupported_sources` |

Changing a choice, for example reclassifying a mark category when a destination format gains support for it, means a new profile version. Transcriptions record the profile they followed, so earlier work stays interpretable.

A project that wants an extra normalisation or rule proposes it for the registry (status `proposed`) instead of adding it locally. This is what keeps the list of normalisations closed.

## 7. Where editorial work fits

Editorial interventions are outside the transcription. A light scheme for recording them, aligned with MEI and TEI vocabulary and pinned to a transcription version (`work@version`), is planned as a separate layer; the corrections layer for clear source errors is its first, narrowest case.

## 8. Related standards

The Principles borrow vocabulary and publish crosswalks. They do not claim compliance.

| Standard | Used for |
|---|---|
| BCP 14 (RFC 2119, RFC 8174) | Strength terms |
| MEI (editorial and transcriptional markup; header and source description) | Vocabulary for the editorial layer; model for the sidecar; an export target |
| TEI | The scholarly-text ancestor of MEI's editorial markup |
| IFLA LRM / LRMoo | Work, source and transcription distinctions |
| W3C PROV-O | Provenance fields |
| W3C Web Annotation | Optional form for editorial layers and their targets |
| IIIF; W3C Media Fragments | Page and region addressing, if a layout index is built |
| SKOS; JSON-LD | Publishing the hierarchy and rule IDs as linkable vocabulary |
| SemVer; date versions | Versioning of data and of these documents |
| SPDX; ISO 8601; CITATION.cff; DataCite | Licence, dates, citation |
| OAIS (ISO 14721); PREMIS; BagIt | Preservation, fixity, packaging |

2026-11-03
