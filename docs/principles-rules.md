# Transcription Principles: rules

*Generated from `core/principles.yaml` (version 2026-11), the profiles in `profiles/` and the formats data in `formats/`. Do not edit by hand; edit the sources and run `python3 tools/build.py`.*

Profiles shown: **OpenScore profile (draft)** (`openscore-2026-11`, draft), **Scores of Scores profile** (`sos-2026-11`, adopted). How the framework works is described in [Principles framework](principles-framework.md); what each format can express is in [Format support](format-support.md).

## Tiers

| Tier | Test |
|---|---|
| **Transcription** | A competent reader could do it from the source and a stated notational convention, with no musical judgement and no second source. |
| **Presentation** | It is systematic, reversible, changes nothing that is notated, and is stated once in the report. Only the registered normalisations qualify. |
| **Editorial** | It needs musical judgement or another source. It is not done in the transcription. |

## Rules

Strength is set by each profile: **MUST** always; **SHOULD** unless there is a recorded reason; **MAY** at discretion; **OFF** not adopted. For normalisations and corrections, MUST means always applied and OFF means not permitted.

### Stance (`stance`)

What a transcription is, and is not.

| Theme | Rule | Statement | openscore-2026-11 | sos-2026-11 | Relations |
|---|---|---|---|---|---|
| Aims | <a id="stance.faithful-reading"></a>`stance.faithful-reading` | **Faithful reading.** Reproduce what the source prints, as exactly as the encoding allows. A transcription reads; it does not edit. | SHOULD | MUST | tension with `stance.meaning-over-appearance`; formats `fmt.version-profile`, `fmt.exact-appearance` |
| Aims | <a id="stance.meaning-over-appearance"></a>`stance.meaning-over-appearance` | **Meaning over appearance.** Encode musical meaning in a form that converts, plays back and survives tool changes. Where an exact visual copy conflicts with a standard encoding, use the standard encoding, only through the registered normalisations, and report them. | MUST | MUST | requires `normalise.closed-list`, `declare.report-deviations` |
| Aims | <a id="stance.judgement-stays-out"></a>`stance.judgement-stays-out` | **Judgement stays out.** Do not choose between readings, correct, complete or interpret. A transcription records; judgement belongs elsewhere. | MUST | MUST | - |
| Boundary | <a id="stance.doubt-means-preserve"></a>`stance.doubt-means-preserve` | **In doubt, preserve.** When it is unclear which tier a decision falls in, treat it as editorial. Keep what the source prints and record the point as an observation. | MUST | MUST | refines `stance.judgement-stays-out`; requires `declare.observations` |

### Reading the source (`read`)

What is read from the source and transcribed.

| Theme | Rule | Statement | openscore-2026-11 | sos-2026-11 | Relations |
|---|---|---|---|---|---|
| Fidelity | <a id="read.preserve-distinctions"></a>`read.preserve-distinctions` | **Preserve the distinctions the source makes.** Where the source uses different notations for what might seem the same, keep the difference (for example common time, cut time and 4/4; ties and slurs; acciaccatura and appoggiatura; key signatures as given). | MUST | MUST | formats `fmt.phrase-slur-tie`, `fmt.time-signature-symbol`, `fmt.grace-timing` |
| Fidelity | <a id="read.consistency-by-equivalence"></a>`read.consistency-by-equivalence` | **Consistency means equivalence only.** Encode notations that mean the same thing the same way. Preserve any divergence that might be musical (a different articulation in one part, a different pitch in a repeated passage); do not harmonise it. | MUST | MUST | refines `stance.judgement-stays-out` |
| Fidelity | <a id="read.preserve-errors"></a>`read.preserve-errors` | **Source errors are preserved.** Transcribe a source error as printed and record it as an observation. Never fix it silently in the transcription. | SHOULD | MUST | refines `stance.judgement-stays-out`; requires `declare.observations`; see also `declare.report-deviations`, `correct.error-test`; formats `fmt.irregular-measures`, `fmt.annotations` |
| Fidelity | <a id="read.record-source-marks"></a>`read.record-source-marks` | **Record the source's own editorial marks.** Brackets and similar marks printed in the source signal an intervention by that edition. Keep the printed mark in the encoding where the format expresses it, and record each such mark in the report. Where the format cannot express the mark, record it in the report only. | MUST | MUST | see also `declare.report-deviations`; formats `fmt.editorial-accidentals` |
| Scope of marks | <a id="read.transcribe-all-marks"></a>`read.transcribe-all-marks` | **Transcribe every printed mark.** Transcribe pitches, rhythms and every printed mark, within what the encoding can express. A category of mark that is classed as editorial or unsupported (see mark_categories; a profile may reclassify a category) is left out systematically and stated once in each report. | MUST | MUST | requires `declare.report-deviations`; formats `fmt.fingering` |
| Terms and text | <a id="read.source-language"></a>`read.source-language` | **Keep the source language.** Keep musical terms and other text in the source language. Translations are additions. | MUST | MUST | tension with `read.standard-instructions`; see also `declare.mark-additions`, `normalise.terms` |
| Terms and text | <a id="read.standard-instructions"></a>`read.standard-instructions` | **Standard encodings for instructions.** Transcribe printed techniques, strings, mutes and harmonics using the standard encoding where one exists, even where that changes the printed wording. | MUST | MUST | - |
| Notation | <a id="read.composer-led-grouping"></a>`read.composer-led-grouping` | **Preserve composer-led grouping.** Preserve beaming, rest and similar grouping that carries musical meaning (the composer's own choice for a passage). Grouping that is only the source edition's habit is a presentation matter. If the two cannot be told apart, keep the grouping as printed and record an observation. | SHOULD | SHOULD | exception of `normalise.beam-grouping`, `normalise.rest-grouping` |
| Notation | <a id="read.ornaments-as-printed"></a>`read.ornaments-as-printed` | **Ornaments as printed.** Copy ornaments as printed, including the difference between acciaccatura and appoggiatura and the position before or after the main note. Where the tool cannot represent a detail, use the nearest available form in this order - type of ornament, then number of beams or strokes, then other indications. | MUST | MUST | formats `fmt.grace-timing`, `fmt.ornament-realization` |
| Notation | <a id="read.ambiguous-marks"></a>`read.ambiguous-marks` | **Ambiguous marks.** Where a printed mark could be read in more than one way (what it is, or which notes it attaches to), encode the reading that the source's own convention fixes - a curve joining adjacent notes of the same pitch is a tie, any other curve is a slur - attached to the notes at the horizontal positions nearest the printed endpoints. Where the convention does not fix a reading, encode that nearest-endpoint reading and record an observation that names the alternatives. A mark that cannot be read as any notated object is recorded as an observation and not encoded. | MUST | MUST | refines `stance.doubt-means-preserve`; see also `read.preserve-distinctions`, `declare.observations`; formats `fmt.phrase-slur-tie`, `fmt.spanner-geometry` |

### Encoding (`encode`)

How what is read is encoded.

| Theme | Rule | Statement | openscore-2026-11 | sos-2026-11 | Relations |
|---|---|---|---|---|---|
| Musical objects | <a id="encode.real-objects"></a>`encode.real-objects` | **Real objects, not drawings or text.** Encode ties, slurs, hairpins, spanning lines, tuplets, tremolo and grace notes as the musical objects they are, so that playback and export work. Do not draw them or type them as text. | MUST | MUST | formats `fmt.phrase-slur-tie`, `fmt.spanner-geometry` |
| Defaults | <a id="encode.defaults-not-overrides"></a>`encode.defaults-not-overrides` | **Defaults, not manual overrides.** Use the tool's defaults for placement, stem direction, accidentals and similar. Avoid manual position offsets and flips. | MUST | SHOULD | refines `stance.meaning-over-appearance`; formats `fmt.stem-direction`, `fmt.visual-accidental` |
| Source layout | <a id="encode.layout-as-data"></a>`encode.layout-as-data` | **Source layout is removable data.** Record the source's system and page breaks where possible, never split a bar across them, and keep them separable from the musical content so that they can be removed in one step. Where a source has no usable layout, omit them and say so. | SHOULD | SHOULD | see also `normalise.page-geometry`; formats `fmt.page-breaks` |

### Normalisation (`normalise`)

The closed menu of permitted presentation choices (the presentation tier).

| Theme | Rule | Statement | openscore-2026-11 | sos-2026-11 | Relations |
|---|---|---|---|---|---|
| The closed list | <a id="normalise.closed-list"></a>`normalise.closed-list` | **Normalisations are a closed list.** Presentation normalisations are limited to those registered in this domain. A profile chooses which are permitted or required; local notes may not add to them. Each applied normalisation is stated once per transcription in the report. | MUST | MUST | refines `stance.meaning-over-appearance`; requires `declare.report-deviations` |
| Grouping and rhythm | <a id="normalise.beam-grouping"></a>`normalise.beam-grouping` | **Beam grouping.** Beam grouping follows the time-signature default, except where grouping is composer-led. | MUST | MUST | formats `fmt.beam-geometry` |
| Grouping and rhythm | <a id="normalise.rest-grouping"></a>`normalise.rest-grouping` | **Rest grouping.** Rest grouping follows the time-signature default, except where grouping is composer-led. | MUST | MUST | - |
| Grouping and rhythm | <a id="normalise.tuplet-brackets"></a>`normalise.tuplet-brackets` | **Tuplet brackets.** Tuplet brackets use a single standard form. Repeated tuplet numbers in a long group may be hidden but are kept in the data. | MUST | MUST | formats `fmt.nested-tuplets` |
| Grouping and rhythm | <a id="normalise.tremolo"></a>`normalise.tremolo` | **Tremolo.** A measured tremolo may use any semantically equivalent notation. | MAY | MAY | - |
| Signs and placement | <a id="normalise.stem-placement"></a>`normalise.stem-placement` | **Stem and placement.** Stem direction and similar placement is automatic. | MUST | MUST | formats `fmt.stem-direction` |
| Signs and placement | <a id="normalise.accidental-conventions"></a>`normalise.accidental-conventions` | **Accidental conventions.** Courtesy accidentals and cancelling naturals follow the default. | MUST | MUST | formats `fmt.visual-accidental` |
| Signs and placement | <a id="normalise.clef"></a>`normalise.clef` | **Clefs.** An unusual or obsolete clef may be replaced by its nearest modern equivalent; an octave-ambiguous clef is notated at sounding pitch; a brief clef change may be adapted for readability. Written pitch is unaffected. | SHOULD | SHOULD | formats `fmt.written-sounding` |
| Words and terms | <a id="normalise.terms"></a>`normalise.terms` | **Standard terms and abbreviations.** Standard abbreviations and equivalent terms are normalised (for example one standard form for decrescendo and diminuendo); anything ambiguous is spelled out. | SHOULD | SHOULD | - |
| Words and terms | <a id="normalise.spread-words"></a>`normalise.spread-words` | **Words spread over several bars.** A word spread over several bars or systems (for example cre - - scen - - do) is one spanning object with a start text and a continuation text. | MUST | MUST | - |
| Page | <a id="normalise.page-geometry"></a>`normalise.page-geometry` | **Page geometry and typography.** Page geometry and typography follow defaults. The source's system and page breaks are kept as data. | MUST | MUST | see also `encode.layout-as-data`; formats `fmt.page-breaks` |

### Declaration (`declare`)

What must be marked, reported and recorded.

| Theme | Rule | Statement | openscore-2026-11 | sos-2026-11 | Relations |
|---|---|---|---|---|---|
| Additions | <a id="declare.mark-additions"></a>`declare.mark-additions` | **Additions are rare and marked.** Add only what is needed to express the source's own notational conventions in the encoding (for example accidentals that the source's convention leaves implicit). Mark every addition visibly. Translations of non-standard terms are additions. Anything that needs judgement is editorial, not an addition. | MUST | MUST | refines `stance.judgement-stays-out`; formats `fmt.editorial-accidentals` |
| Reporting | <a id="declare.report-deviations"></a>`declare.report-deviations` | **Report every unmarked deviation.** Report every deviation that is not visibly marked. Differences caused by registered normalisations are stated once per transcription; specific interventions are listed one by one. The report, with the transcription, is enough to recover what the source prints. | MUST | MUST | - |
| Observations | <a id="declare.observations"></a>`declare.observations` | **Observations.** Record in the report, as an observation, every point that may be a source error, a divergence between parts or repeated passages, a mark with more than one reading, or a decision whose tier was unclear. An observation gives the location, what the source prints, and why it was recorded. It does not change the transcription. | MUST | MUST | see also `declare.report-deviations`; formats `fmt.annotations` |
| Provenance | <a id="declare.record-provenance"></a>`declare.record-provenance` | **Record provenance.** Record the source edition and file, the pages where the transcription appears, who transcribed and reviewed it, when, which tools were used, and the versions of the Principles, profile and notes applied. | MUST | MUST | formats `fmt.metadata`, `fmt.source-description` |

### Correction (`correct`)

The one kind of editorial intervention that a profile may allow, the test it must pass, and how it is recorded.

| Theme | Rule | Statement | openscore-2026-11 | sos-2026-11 | Relations |
|---|---|---|---|---|---|
| The clear-error test | <a id="correct.error-test"></a>`correct.error-test` | **The clear-error test.** A source error is clear only if both conditions hold. (1) The printed reading is impossible under the source's own notation, for example a bar whose durations do not add up to the time signature and that is not marked as incomplete, a tie joining different pitches, or a slur that begins and never ends. (2) Exactly one minimal change makes the reading possible, and that change is found from the source alone, its own parallel passages included. An error that fails either condition is not clear and is kept as printed. | MUST | MUST | refines `stance.judgement-stays-out` |
| Placement and record | <a id="correct.in-place"></a>`correct.in-place` | **Correct in the transcription.** A clear error (`correct.error-test`) may be corrected directly in the transcription. | MUST | OFF | requires `correct.error-test`, `correct.record`; tension with `read.preserve-errors` |
| Placement and record | <a id="correct.layer"></a>`correct.layer` | **Corrections in a separate layer.** A correction that is not made in the transcription is recorded in a layer separate from it, pinned to a transcription version, so that the printed reading and the corrected reading can each be recovered. | OFF | MUST | requires `correct.error-test`, `correct.record`; formats `fmt.editorial-status`, `fmt.annotations`, `fmt.persistent-addresses` |
| Placement and record | <a id="correct.record"></a>`correct.record` | **Record every correction.** Record each correction with its location, the printed reading, the corrected reading, and the part of `correct.error-test` that was met, whether the correction is made in the transcription or in a layer. | MUST | MUST | see also `declare.report-deviations`; formats `fmt.editorial-status`, `fmt.annotations` |

## Profile `openscore-2026-11`

OpenScore profile (draft). Status: **draft**.

Draft: 7 of 36 strengths have a documented basis. The other 29 take the Scores of Scores strength as a core default and are not yet confirmed choices of the project.

**Ranked aims** (highest first):

1. `stance.meaning-over-appearance` (Useful to musicians first.)
2. `stance.faithful-reading` (Then copy the source directly.)
3. `stance.judgement-stays-out`

**Resolution of tensions:**

| Wins | Over | Scope | Reason |
|---|---|---|---|
| `stance.meaning-over-appearance` | `stance.faithful-reading` | Appearance, and source errors that pass correct.error-test. | A useful score comes first; the source is otherwise copied directly. |
| `read.standard-instructions` | `read.source-language` | Instructions that have a standard encoding in the tool. | Standard entries drive playback, part extraction and export. |
| `correct.in-place` | `read.preserve-errors` | Source errors that pass correct.error-test. | A clear error is corrected; every other error stays as printed, and read.preserve-errors still applies to it. |

**Format of the version of record:** `musescore`. MuseScore 4 native project (MSCZ/MSCX), documented 4.x workflows.

Extensions accepted: none.

**Categories of printed mark.** The treatment is derived from the formats data (direct or qualified: transcribed; extension: transcribed only if accepted; otherwise unsupported). A category classed as unsupported is left out systematically and stated once in each report. Every other printed mark is transcribed (`read.transcribe-all-marks`).

| Category | Treatment | Derived from |
|---|---|---|
| Fingering (`fingering`) | **Transcribed** | fmt.fingering in musescore: direct. Fingering text objects. |

## Profile `sos-2026-11`

Scores of Scores profile. Status: **adopted**.

**Ranked aims** (highest first):

1. `stance.judgement-stays-out`
2. `stance.meaning-over-appearance` (Applies to appearance only (grouping, placement, typography), never to notated content.)
3. `stance.faithful-reading`
4. `read.consistency-by-equivalence`

**Resolution of tensions:**

| Wins | Over | Scope | Reason |
|---|---|---|---|
| `stance.meaning-over-appearance` | `stance.faithful-reading` | Appearance only (grouping, placement, typography), through the registered normalisations. | Standard encodings convert, play back and survive tool changes; an exact visual copy does not. |
| `read.standard-instructions` | `read.source-language` | Instructions that have a standard encoding in the tool (for example arco, pizz., con sord., senza sord.). | Standard entries drive playback, part extraction and export. Almost no other terms have this status. |
| `read.preserve-errors` | `correct.in-place` | Every source error, including clear ones. | The transcription records what the source prints. A clear error is corrected only in the separate layer (correct.layer). |

**Format of the version of record:** `krn`. Core **kern as defined in the Humdrum guide, plus the VHV editorial-accidental signifier declared in !!!RDF**kern and the VHV system and page break conventions. No other extension.

Extensions accepted: `fmt.editorial-accidentals`, `fmt.page-breaks`.

**Categories of printed mark.** The treatment is derived from the formats data (direct or qualified: transcribed; extension: transcribed only if accepted; otherwise unsupported). A category classed as unsupported is left out systematically and stated once in each report. Every other printed mark is transcribed (`read.transcribe-all-marks`).

| Category | Treatment | Derived from |
|---|---|---|
| Fingering (`fingering`) | **Unsupported** | fmt.fingering in krn: extension (extension not accepted). Separate **fing spine. |

**Source types not covered:** manuscript.

**Structural precedence (all profiles):** a rule that is an `exception-of` another wins over it within its scope. `refines` and `see-also` never conflict.

## Concordance with earlier codes

| Earlier code | Rule |
|---|---|
| TP1 | `stance.faithful-reading` |
| TP2 | `stance.meaning-over-appearance` |
| TP3 | `read.preserve-distinctions` |
| TP4 | `stance.judgement-stays-out` |
| TP5 | `read.consistency-by-equivalence` |
| TP6 | `read.transcribe-all-marks` |
| TP7 | `read.preserve-errors` |
| TP8 | `read.composer-led-grouping` |
| TP9 | `read.source-language` |
| TP10 | `read.standard-instructions` |
| TP11 | `read.record-source-marks` |
| TP12 | `read.ornaments-as-printed` |
| TP13 | `encode.real-objects` |
| TP14 | `encode.defaults-not-overrides` |
| TP15 | `normalise.closed-list` |
| TP15.1 | `normalise.beam-grouping` |
| TP15.2 | `normalise.rest-grouping` |
| TP15.3 | `normalise.tuplet-brackets` |
| TP15.4 | `normalise.stem-placement` |
| TP15.5 | `normalise.accidental-conventions` |
| TP15.6 | `normalise.clef` |
| TP15.7 | `normalise.terms` |
| TP15.8 | `normalise.spread-words` |
| TP15.9 | `normalise.page-geometry` |
| TP15.10 | `normalise.tremolo` |
| TP16 | `encode.layout-as-data` |
| TP17 | `declare.mark-additions` |
| TP18 | `declare.report-deviations` |
| TP19 | `declare.record-provenance` |
