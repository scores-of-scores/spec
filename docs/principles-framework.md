# Transcription Principles: framework

*How the Principles are organised and used. Version 2026-11. Part of the Scores of Scores document set (see the README). The rules themselves are in the generated [rules table](principles-rules.md); what each format can express is in [Format support](format-support.md).*

## 1. What this is

The Principles are a small, tool-neutral framework for a **pragmatically faithful transcription** of a notated source into a digital encoding. They say what a transcription must and must not do, what it must declare, and the one kind of correction that a project may allow. They are written so that another project can adopt the core and make different choices.

**The format sets the limit.** A transcription is made in a particular encoding format, and the Principles apply within what that format can express (`stance.faithful-reading`: "as exactly as the encoding allows"). What a format can express is not asserted in the rules. It is recorded as evidence in the formats data and linked to the rules it bears on (section 5). Where a detail cannot be represented, the nearest available form is used (`read.ornaments-as-printed`, `read.ambiguous-marks`); where a whole category of printed mark cannot, its treatment is derived as *unsupported*. This is a limit of the format, not a judgement, so it is not an editorial matter, and it changes when the format or the profile changes.

**Out of scope:** editorial work other than the clear-error correction of section 6 (choosing between readings, completing, interpreting, comparing sources, performance practice) and manuscripts and other special sources, which need further rules.

## 2. Four layers

| Layer | Holds | Changes | Where |
|---|---|---|---|
| **Core** | The rules: what a transcription could be required to do, how rules relate (refines, exception, requires, tension), the tiers, the vocabulary | Rarely | `core/principles.yaml`, `core/glossary.yaml` |
| **Formats** | Evidence of what four formats can express, feature by feature, with sources, linked to the rules it bears on | When a format, a source or a test result changes | `formats/` |
| **Profile** | A project's choices: how strong each rule is, which rule wins in a tension, ranked aims, the format of its version of record, what is out of scope | When the project decides | `profiles/` |
| **Local notes** | Tool settings, placement defaults, workflow, report format, suggestions for downstream work | Often | `notes/registry.yaml` |

**Where does a rule belong?** If a reasonable project could reject it, it is a profile choice, not core. Even "preserve errors" is a stance, because correcting is the classic opposing view: the core defines both `read.preserve-errors` and `correct.in-place`, and each profile decides which to adopt and which wins. Local notes may narrow what the profile allows, never widen it.

## 3. Tiers and the boundary test

Every decision falls into one of three tiers (defined in the registry):

| Tier | Test | Allowed in the transcription? |
|---|---|---|
| **Transcription** | A competent reader could do it from the source and a stated notational convention, with no musical judgement and no second source | Yes |
| **Presentation** | Systematic, reversible, changes nothing notated, stated once in the report | Only the registered normalisations (`normalise.*`) |
| **Editorial** | Needs musical judgement or another source | No, except a correction that passes the clear-error test and that the profile allows |

Three questions, in order:
1. Does it change what is notated (a pitch, rhythm, mark or text)? If yes, it is not presentation.
2. Could it be done from the source and a stated convention alone? If yes, it is transcription; if no, it is editorial.
3. Is it systematic, reversible and reported once, and is it registered under `normalise`? If yes, it is presentation.

If it is unclear, treat it as editorial: keep what the source prints and record an observation (`stance.doubt-means-preserve`, `declare.observations`).

| Situation | Tier | Handling |
|---|---|---|
| The source's convention makes an accidental implicit and the encoding needs it explicit | Transcription | Add it and mark it (`declare.mark-additions`) |
| Cut-time symbol printed | Transcription | Keep it (`read.preserve-distinctions`) |
| A curve may be a slur or a tie, with unclear ends | Transcription | The reading the convention fixes, else the nearest-endpoint slur, with an observation (`read.ambiguous-marks`) |
| One part has a different articulation from the others | Editorial | Keep as printed (`read.consistency-by-equivalence`) |
| A printed note appears to be wrong | Editorial | Keep as printed and record an observation (`read.preserve-errors`); correct only if the error is clear and the profile allows it (`correct.error-test`) |
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
| `kind` | `obligation` (a do or don't) or `permission` (a registered normalisation or a correction) |
| `title`, `statement` | A strength-neutral imperative; the profile supplies the strength |
| `relations` | `refines`, `exception-of`, `requires`, `tension-with`, `see-also` |
| `format_features` | Formats-data features that bear on what the rule can achieve in a given format |
| `rationale`, `examples` | Why, and worked cases |
| `aliases` | Earlier codes, for traceability |
| `status` | `active`, `proposed` or `retired` (retired rules name `replaced_by`) |

### Domains

`stance` (what a transcription is), `read` (what is read), `encode` (how it is encoded), `normalise` (the closed menu of presentation choices), `declare` (what is marked, reported and recorded), `correct` (the clear-error test and where a correction is made and recorded). The domain is the only hierarchy in the ID. Themes are metadata, so a rule can be re-themed without a rename.

### Relations

| Relation | Meaning | Consequence |
|---|---|---|
| `refines` | A more specific form of another rule | Never conflicts |
| `exception-of` | Limits another rule in a stated scope | Wins over it in that scope, in every profile |
| `requires` | Cannot be adopted without the other | Checked by the build for every profile |
| `tension-with` | Can pull against the other | **The profile must resolve every tension** (checked by the build) |
| `see-also` | Related | None |

### Strengths

Set by the profile, using the BCP 14 terms (RFC 2119, RFC 8174), in capitals only where they are normative: **MUST**, **SHOULD**, **MAY**, **OFF** (not adopted; for a normalisation or a correction, not permitted).

## 5. Formats and derived treatments

The formats layer is a dataset of features, each answered for four formats (KRN, MusicXML, MuseScore's native format and MEI). Each cell has a **status** (direct, qualified, extension, workaround, unknown), a mechanism, any condition, a workaround, an **evidence** label (documented, inference, unverified) and cited sources. Status is a capability label and never a score; no format is ranked. A cell counts as *tested* only when a fixture that covers it has a recorded result for that format.

Rules link to features through `format_features`, and the build generates the inverse. A feature linked to a rule shows the rule IDs in the reader; the [format support](format-support.md) table shows, for each profile, whether the feature is expressible in its format.

**Mark categories.** Some printed marks may fall outside a format. The registry lists such categories (`mark_categories`), each linked to a feature. The treatment in a profile is derived from the status of that feature in the profile's format:

| Status in the profile's format | Treatment |
|---|---|
| direct, qualified | Transcribed (a qualification is reported) |
| extension | Transcribed if the profile accepts that extension (`scope.encoding.accept_extensions`); otherwise unsupported |
| workaround, unknown | Unsupported |

A profile may reclassify a category in `scope.marks`, with a reason. Any printed mark outside a listed category is transcribed (`read.transcribe-all-marks`). A project that needs another category proposes it for the registry, as for a rule. When a format gains support, the cell changes and so does the derived treatment, in a new pinned version.

**The dialect is part of the profile.** `scope.encoding` names the format, the exact dialect or version, and the extensions accepted. A profile that accepts no extension for a feature treats a feature whose status is *extension* as unsupported.

## 6. Corrections

A source error is *clear* only if it passes `correct.error-test`: (1) the printed reading is impossible under the source's own notation, and (2) exactly one minimal change makes it possible, found from the source alone. Every other error is kept as printed.

The core defines two placements and a record. A profile chooses between them, which is the main difference between positions:

| Rule | Meaning | Strengths in the shipped profiles |
|---|---|---|
| `correct.in-place` | A clear error may be corrected directly in the transcription | OFF in `sos-2026-11`; MUST in `openscore-2026-11` |
| `correct.layer` | Corrections that are not made in the transcription are recorded in a separate layer pinned to a transcription version | MUST in `sos-2026-11`; OFF in `openscore-2026-11` |
| `correct.record` | Every correction is recorded with location, printed and corrected readings, and the condition of the test that was met | MUST in both |

`correct.in-place` is in tension with `read.preserve-errors`, so each profile resolves it in `precedence`. Everything else that needs judgement stays editorial and outside the transcription. Downstream editions record their own changes in their own project, using an established scheme such as the editorial markup of MEI or TEI, pinned to a transcription version (`work@version`).

## 7. Identity and change

- IDs are **never renumbered and never reused**. If a rule's meaning changes materially it gets a new ID and the old one is retired with `replaced_by` and a date. Editorial rewording keeps the ID.
- Four kinds of ID share one namespace, and the build rejects a clash: rules and notes (`domain.slug`, `area.slug`), format features (`fmt.slug`) and fixtures (`fx.slug`).
- The Principles, the formats data and the Notes use date versions (YYYY-MM), and each release has one tag and one DOI. Schemas carry their own version in their `$id`. Cite a rule as `read.preserve-errors@2026-11`, and a feature as `fmt.fingering@2026-11`.
- A change to a rule, a profile choice or a format cell appears in a new dated version and is listed in `CHANGELOG.md`. A proposed extension is a rule with status `proposed`: it has no strength in any profile until it is made active in a new version. Changes are not retroactive.
- Each transcription records `principles_version`, the `profile` it followed, the `notes_version` and the `normalisations` it applied (the sidecar; see `declare.record-provenance`).
- **Build.** `python3 tools/build.py` validates every file against its schema and the links between layers, and generates the rules table, the format support table, the glossary, the Notes, the formats reader, the paper's tables, JSON files and CSV files. It fails on, among other things: a relation or format link whose target is missing, a tension without precedence, a cycle in precedence, an active rule without a strength, a rule that is adopted while a rule it requires is OFF, an accepted extension that is not an extension in the profile's format, a duplicate ID or alias, and a Note that applies a normalisation or correction that the profile does not permit.

## 8. Adopting the Principles elsewhere

1. Take `core/principles.yaml` and `formats/` unchanged.
2. Write a profile (see the table below): a strength for every active rule, a resolution for every tension, your ranked aims and your scope.
3. Run the build; fix what it reports.
4. Write local notes for your tools and workflow.

| A profile chooses | Profile field |
|---|---|
| The strength of every active rule | `strengths` |
| Where a choice comes from, if it is documented | `basis` |
| Which rule wins in each tension | `precedence` |
| Ranked aims | `aim_order` |
| The format, dialect and accepted extensions of the version of record | `scope.encoding` |
| The treatment of a category of printed mark, where it departs from the derived one | `scope.marks` |
| Source types not covered | `scope.unsupported_sources` |

A profile has status `draft` until every strength is a confirmed choice. In a draft, a rule without a `basis` entry is a core default and is reported as unconfirmed.

A project that wants an extra normalisation, rule or format feature proposes it for the registry. This keeps the list of normalisations closed.

## 9. Related standards

The Principles borrow vocabulary and publish crosswalks. They do not claim compliance.

| Standard | Used for |
|---|---|
| BCP 14 (RFC 2119, RFC 8174) | Strength terms |
| MEI (editorial and transcriptional markup; header and source description) | Vocabulary for corrections and downstream editions; model for the sidecar; an export target; one of the four formats in the formats data |
| TEI | The scholarly-text ancestor of MEI's editorial markup |
| IFLA LRM / LRMoo | Work, source and transcription distinctions |
| W3C PROV-O | Provenance fields |
| W3C Web Annotation | Optional form for corrections layers and their targets |
| IIIF; W3C Media Fragments | Page and region addressing, if a layout index is built |
| SKOS; JSON-LD | Publishing the hierarchy and rule IDs as linkable vocabulary |
| SemVer; date versions | Versioning of schemas and of data and documents |
| SPDX; ISO 8601; CITATION.cff; DataCite | Licence, dates, citation |
| OAIS (ISO 14721); PREMIS; BagIt | Preservation, fixity, packaging |
