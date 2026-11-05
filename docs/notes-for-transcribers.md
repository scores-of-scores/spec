# Notes for Transcribers

*Local notes for transcribers and reviewers. Version 2026-11 (draft). Generated from `notes/registry.yaml`. Applies the profile `sos-2026-11` of the Transcription Principles, version 2026-11. Part of the Scores of Scores document set (see the README).*

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

## Contents

| Area | Section |
|---|---|
| `metadata` | Metadata |
| `layout` | Layout |
| `rhythm` | Rhythm and grouping |
| `ornaments` | Ornaments |
| `key` | Key and accidentals |
| `clef` | Clefs and stems |
| `dynamics` | Dynamics and lines |
| `ties` | Ties and slurs |
| `brackets` | Brackets |
| `playing` | Playing instructions |
| `text` | Text |
| `workflow` | Workflow |
| `report` | The editorial report |
| `editorial` | Editorial matters |

## Metadata (`metadata`)

Whether and where metadata appears in the rendered score is project specific and handled at the templating stage. For stored metadata, more is more.

<a id="metadata.title-composer-lyricist"></a>

### `metadata.title-composer-lyricist`: Title, composer and lyricist

*house*

Title and composer are present in the score properties and displayed. Title is at the top of the page, centred; composer is at the right-hand side, just below the title. For songs, the lyricist is at the left-hand side, just below the title, roughly in line with the composer.

Earlier codes: M1.

<a id="metadata.dedication"></a>

### `metadata.dedication`: Dedication

*house*

Use a separate vertical frame above the main title frame, centred and italicised, at the templating stage.

Earlier codes: M2.

<a id="metadata.dates-not-shown"></a>

### `metadata.dates-not-shown`: Dates are not shown

*house*

Birth and death dates are not shown for anyone (composer, lyricist or dedicatee). Some of that data is stored separately in the project data.

Earlier codes: M3.

<a id="metadata.composition-date"></a>

### `metadata.composition-date`: Date of composition

*house*

The date of composition is not shown in the title frame. A date and place of composition may be shown at the end of the score if it appears in the source.

Earlier codes: M4.

<a id="metadata.provenance-stored"></a>

### `metadata.provenance-stored`: Provenance is stored, not rendered

*house*; applies [`declare.record-provenance`](principles-rules.md#declare.record-provenance)

Provenance (source edition and file, pages, transcriber, reviewer, licence, tools, and the Principles, profile and Notes versions) is stored in the project data and not rendered by default. The editorial report repeats the source details.

Earlier codes: M5.

## Layout (`layout`)

Source breaks and placement above and below the stave.

<a id="layout.source-breaks"></a>

### `layout.source-breaks`: Entering source breaks

*tool*; applies [`encode.layout-as-data`](principles-rules.md#encode.layout-as-data)

Follow the source's system breaks first and page breaks second. Enter them with the app's standard break elements (not spacers or manual position offsets) so that removal is a single operation. Never split a bar across a break.

- Omit all breaks in extreme cases (very small pages, or music transcribed from parts) and say so in the report.

Earlier codes: L1, L1.1, L1.2.

<a id="layout.above-below"></a>

### `layout.above-below`: Above and below the stave

*house*

Use the template defaults. Above the stave go tempo marks and playing instructions such as pizz. and arco. Below go all dynamics, hairpins and expression text.

- *Exception:* Quartets: where one voice is arco and another pizz., place each above or below as suits its voice.

- *Exception:* All: with several expressive markings at once, it can help to flip some to the other side.

- *Exception:* Lieder: dynamics in the vocal parts go above.

Earlier codes: L2, L2.1, L2.2.

## Rhythm and grouping (`rhythm`)

Beaming, rests, tuplets, tremolo and tempo.

<a id="rhythm.beaming-default"></a>

### `rhythm.beaming-default`: Default beaming

*presentation*; applies [`normalise.beam-grouping`](principles-rules.md#normalise.beam-grouping)

Enter notes with the default beaming for the time signature. Editorial conventions for 6/8, for example, vary between editions, so they are normalised.

Earlier codes: T2, T2.2.

<a id="rhythm.beam-placement"></a>

### `rhythm.beam-placement`: Beam placement

*house*

Beams go all above or all below the noteheads, not a combination of both.

- *Exception:* String parts never use beams with noteheads on both sides. Lieder piano parts sometimes need it, for example when crossing between treble and bass of the grand stave. Discuss with your reviewer.

Earlier codes: T2.1.

<a id="rhythm.composer-led-signals"></a>

### `rhythm.composer-led-signals`: Telling composer-led grouping from house style

*house*; applies [`read.composer-led-grouping`](principles-rules.md#read.composer-led-grouping)

Copy a non-standard grouping when it appears to be the composer's own choice for a passage (Bartok is a classic case). If you cannot tell, ask your reviewer and report the decision.

- Signals of composer-led grouping: it departs from the norm only in that passage; it recurs identically when the material recurs; it plainly serves the music (regrouping the metre, showing a phrase); or other sources agree.

- Signals of house style: the same habit applies across the whole edition regardless of the music.

Earlier codes: T2.2.1.

<a id="rhythm.beam-across-break"></a>

### `rhythm.beam-across-break`: Beams across a system break

*tool*; applies [`encode.layout-as-data`](principles-rules.md#encode.layout-as-data)

Do not copy a beam that would continue across a barline at a system break if the app has no provision for it. Separate the beam groups at that barline.

Earlier codes: T2.2.2.

<a id="rhythm.rest-grouping"></a>

### `rhythm.rest-grouping`: Rest grouping

*presentation*; applies [`normalise.rest-grouping`](principles-rules.md#normalise.rest-grouping)

Use the time-signature defaults. This can diverge visibly from the source; that is fine if consistent. State it once in the report.

Earlier codes: T3.

<a id="rhythm.tuplet-settings"></a>

### `rhythm.tuplet-settings`: Tuplet settings

*tool*; applies [`normalise.tuplet-brackets`](principles-rules.md#normalise.tuplet-brackets)

Use the default bracket whatever the source uses. In the Inspector set Direction = Auto, Number type = Number and Bracket type = Auto.

- In a long passage that is consistently in one tuplet, show the first marking and make the rest invisible. They stay in the file, so playback and export are unaffected.

Earlier codes: T4, T4.1, T4.2.

<a id="rhythm.tremolo-default"></a>

### `rhythm.tremolo-default`: Tremolo

*presentation*; applies [`normalise.tremolo`](principles-rules.md#normalise.tremolo)

Prefer the app's default form of a measured tremolo.

Earlier codes: T5.

<a id="rhythm.tempo-marks"></a>

### `rhythm.tempo-marks`: Tempo marks

*house*; applies [`read.source-language`](principles-rules.md#read.source-language)

Include tempo marks as in the source, with metronome marks, above the stave. Keep tempo terms in the source language, with a bracketed translation for non-standard ones (`text.translation-format`). Gradual changes (rit., accel.) are lines and follow `dynamics.terms` and `dynamics.ritardando-line`.

Earlier codes: T6.

## Ornaments (`ornaments`)

Grace notes and other ornaments.

<a id="ornaments.placement-default"></a>

### `ornaments.placement-default`: Ornament placement

*tool*; applies [`read.ornaments-as-printed`](principles-rules.md#read.ornaments-as-printed)

Use the defaults for exact placement (for example before or after the barline).

Earlier codes: O2.

<a id="ornaments.nearest-form"></a>

### `ornaments.nearest-form`: Nearest available form

*house*; applies [`read.ornaments-as-printed`](principles-rules.md#read.ornaments-as-printed)

When a grace note group cannot be entered exactly, use the nearest form in the order the rule gives, and add staff text for a tuplet indication only if it is useful.

Earlier codes: O3.

## Key and accidentals (`key`)

Key signatures and added accidentals.

<a id="key.no-cancelling-naturals"></a>

### `key.no-cancelling-naturals`: No cancelling naturals

*tool*; applies [`normalise.accidental-conventions`](principles-rules.md#normalise.accidental-conventions)

Never show cancelling naturals on a change of key signature. Never use the "Natural-flat" or "Natural-sharp" symbols for individual cancellation in adjacent measures.

Earlier codes: K1.1.

<a id="key.added-accidentals"></a>

### `key.added-accidentals`: Added accidentals

*house*; applies [`declare.mark-additions`](principles-rules.md#declare.mark-additions)

Enclose any accidental you introduce (one not in the source) in square brackets [] and list each in the report.

Earlier codes: K2.

## Clefs and stems (`clef`)

Which clefs to keep, adapt or replace.

<a id="clef.decision-order"></a>

### `clef.decision-order`: Decision order for viola and cello

*house*; applies [`normalise.clef`](principles-rules.md#normalise.clef)

(a) Keep the source clef where `clef.preserved-clefs` lists it. (b) Apply the leger-line test in `clef.leger-line-test` to brief changes. (c) Use `clef.other-clefs-modern` for any clef not listed.

<a id="clef.two-clefs-default"></a>

### `clef.two-clefs-default`: Two clefs by default

*house*

Most work is set in two clefs, treble and bass.

Earlier codes: C1.

<a id="clef.preserved-clefs"></a>

### `clef.preserved-clefs`: Clefs to preserve

*house*; applies [`normalise.clef`](principles-rules.md#normalise.clef)

Preserve these clefs, subject to `clef.leger-line-test`. Lieder: treble clef with 8 beneath it (down an octave), typical for the tenor voice in modern editions (solo and choral). Viola: mostly alto clef, with occasional treble passages. 'Cello: bass, tenor and treble.

- *Exception:* Cello treble clef is notated at the sounding octave, per modern convention. Some sources (for example Dvorak and Beethoven) use a de facto treble clef an octave lower; we avoid that practice.

Earlier codes: C2, C2.1, C2.2, C2.3.

<a id="clef.leger-line-test"></a>

### `clef.leger-line-test`: Leger-line test for brief clef changes

*presentation*; applies [`normalise.clef`](principles-rules.md#normalise.clef)

Omit or adapt brief clef changes where a source seems to prioritise page space over readability. For viola and cello, change clef only if you would need more than 2 leger lines and the passage stays high long enough to help the player. Use the clef a modern player would expect, and report it.

- Some transcribers use the original clefs while transcribing (see `workflow.original-clefs`). An algorithmic approach to modern clef choice exists in the [Species corpus](https://github.com/MarkGotham/species) and may be formalised later.

Earlier codes: C3.

<a id="clef.other-clefs-modern"></a>

### `clef.other-clefs-modern`: Other clefs to modern equivalents

*presentation*; applies [`normalise.clef`](principles-rules.md#normalise.clef)

Adapt any clef not listed in `clef.preserved-clefs` (soprano, mezzo-soprano, baritone, French violin clef) to its nearest modern equivalent. The cello clefs in `clef.preserved-clefs` are preserved.

Earlier codes: C4.

<a id="clef.no-stem-flips"></a>

### `clef.no-stem-flips`: No manual stem flips

*tool*; applies [`encode.defaults-not-overrides`](principles-rules.md#encode.defaults-not-overrides)

Almost never flip a note's stem manually. This also matters for transposition and clef changes.

Earlier codes: C5.

## Dynamics and lines (`dynamics`)

Terms, abbreviations and spanning lines.

<a id="dynamics.terms"></a>

### `dynamics.terms`: Terms

*presentation*; applies [`normalise.terms`](principles-rules.md#normalise.terms)

Copy the source, except where an alternative is clearly equivalent and more standard today (for example diminuendo or dim. for decrescendo).

Earlier codes: D2, D2.1.

<a id="dynamics.abbreviations"></a>

### `dynamics.abbreviations`: Abbreviations

*presentation*; applies [`normalise.terms`](principles-rules.md#normalise.terms)

Use the recognised standards cresc., dim., rit., rall. and accel. Spell out anything even slightly ambiguous, or adapt it to one of these.

Earlier codes: D3.

<a id="dynamics.spread-words-line"></a>

### `dynamics.spread-words-line`: Words spread over several bars

*tool*; applies [`normalise.spread-words`](principles-rules.md#normalise.spread-words)

For cre - - - scen - - - do across bars or systems, use a wide-dashed line (Line Thickness = 0.12sp, Dash Line Length = 5, Dash Gap Width = 20) with standard Begin text and a Continue text in parentheses at the start of each system, for example (dim.).

Earlier codes: D4.

<a id="dynamics.ritardando-line"></a>

### `dynamics.ritardando-line`: Ritardando line

*tool*; applies [`encode.real-objects`](principles-rules.md#encode.real-objects)

Use the app's built-in ritardando line where it exists. Earlier scores used a System text entry instead; these may be updated. Record the app and version in the report header.

Earlier codes: D5.

## Ties and slurs (`ties`)

Accidentals across ties.

<a id="ties.accidental-across-tie"></a>

### `ties.accidental-across-tie`: Accidentals across ties

*tool*; applies [`normalise.accidental-conventions`](principles-rules.md#normalise.accidental-conventions)

An accidental is not repeated at the start of the second (or later) bar of a tie, even at a system or page break. If the same pitch recurs later in that bar, the accidental is shown (a default, and worth keeping).

Earlier codes: S2.

## Brackets (`brackets`)

Our brackets, the source's brackets, and telling them apart.

<a id="brackets.ours"></a>

### `brackets.ours`: Square brackets mark what we add

*house*; applies [`declare.mark-additions`](principles-rules.md#declare.mark-additions)

Square brackets in our files mark only what we add (accidentals, translations). Every other intervention is reported, not marked.

Earlier codes: B2.

<a id="brackets.source-marks"></a>

### `brackets.source-marks`: Keep the source's brackets

*house*; applies [`read.record-source-marks`](principles-rules.md#read.record-source-marks)

In a direct transcription, keep the brackets (square or curved) that the source prints around a note, accidental or similar, as printed. They signal an intervention by the source's edition. Downstream editions may drop them (see `editorial.downstream-editions`).

Earlier codes: B1, B3.

<a id="brackets.tell-apart"></a>

### `brackets.tell-apart`: Telling the source's brackets from ours

*house*; applies [`read.record-source-marks`](principles-rules.md#read.record-source-marks), [`declare.mark-additions`](principles-rules.md#declare.mark-additions)

Keep the source's brackets distinguishable from ours. Carry the distinction in the data where the format allows, and always in the report. Where the source also uses square brackets, the report lists which are ours.

Earlier codes: B4.

## Playing instructions (`playing`)

Techniques, strings, mutes, harmonics and fingerings.

<a id="playing.standard-entries"></a>

### `playing.standard-entries`: Standard palette entries

*tool*; applies [`read.standard-instructions`](principles-rules.md#read.standard-instructions)

Where the app has a standard entry for a technique or similar instruction, use it with its standard (Italian) wording, whatever the source says. These are pizz. and arco (from the text palette; placement as in `layout.above-below`) and con sord. and senza sord. for mutes. The entries drive playback, part extraction and export. Almost no other terms have this status, so for everything else the source language stands.

Earlier codes: G5.1, P1, P5.

<a id="playing.harmonics"></a>

### `playing.harmonics`: Harmonics

*tool*; applies [`read.transcribe-all-marks`](principles-rules.md#read.transcribe-all-marks)

Include harmonics, from the articulations palette (the symbol looks like o).

Earlier codes: P2.

<a id="playing.string-indications"></a>

### `playing.string-indications`: String indications

*house*; applies [`read.transcribe-all-marks`](principles-rules.md#read.transcribe-all-marks)

Include any instruction giving the string, for example sul A or IV.

Earlier codes: P3.

<a id="playing.fingerings-excluded"></a>

### `playing.fingerings-excluded`: Fingerings are not transcribed

*house*; applies [`read.transcribe-all-marks`](principles-rules.md#read.transcribe-all-marks)

Fingering is classed as unsupported in our profile (mark category `fingering`), because it is outside what basic encoding formats express, so printed fingerings are not transcribed. State this once in each report.

- *Exception:* Where a fingering works as an implicit string instruction, include it.

Earlier codes: P4, P4.1.

## Text (`text`)

Translations and other text conventions.

<a id="text.translation-format"></a>

### `text.translation-format`: Translations

*house*; applies [`declare.mark-additions`](principles-rules.md#declare.mark-additions), [`read.source-language`](principles-rules.md#read.source-language)

Give a translation of a non-standard term in square brackets after the term in the same text item, for example Sehr langsam [Very slowly]. If it would clutter the score, put it in the report instead.

Earlier codes: G5.2.

## Workflow (`workflow`)

How work proceeds from transcriber to reviewer.

<a id="workflow.red-text"></a>

### `workflow.red-text`: Red text while working

*house*

Use staff text coloured red to explain intentional deviations from the source and to flag anything suspicious, including 'obvious' corrections you did not make. Reviewers decide each point and delete all red text before upload.

Earlier codes: W1.

<a id="workflow.report-transfer"></a>

### `workflow.report-transfer`: From red text to the report

*house*; applies [`declare.report-deviations`](principles-rules.md#declare.report-deviations)

Before deleting red text, reviewers move whatever still applies into the editorial report. Red text is the working draft of that report.

Earlier codes: W2.

<a id="workflow.source-errors"></a>

### `workflow.source-errors`: Handling a suspected source error

*house*; applies [`read.preserve-errors`](principles-rules.md#read.preserve-errors)

Transcribe it as printed, add red text, and note it as an observation in the report (`editorial.observations`) so that a correction can be proposed later.

Earlier codes: W3.

<a id="workflow.consistency-edits"></a>

### `workflow.consistency-edits`: Consistency edits

*house*; applies [`read.consistency-by-equivalence`](principles-rules.md#read.consistency-by-equivalence)

Make equivalent notations match, but do not edit a divergence that might be musical (an articulation that differs in one part, a different pitch in a recurring motive). Preserve it and flag it. Harmonising is editorial.

Earlier codes: G4.

<a id="workflow.ask-reviewer"></a>

### `workflow.ask-reviewer`: If in doubt, ask

*house*; applies [`stance.doubt-means-preserve`](principles-rules.md#stance.doubt-means-preserve)

Ask your reviewer and/or the team via Signal.

Earlier codes: G7.

<a id="workflow.manuscripts"></a>

### `workflow.manuscripts`: Manuscripts

*house*

Manuscript and other special sources are not covered by the Principles yet. They bring more exceptions and need more reporting. Always agree the approach with your reviewer first.

Earlier codes: G6.

<a id="workflow.original-clefs"></a>

### `workflow.original-clefs`: Original clefs while transcribing

*house*

Some transcribers use the original clefs while transcribing, to make proofreading easier (comparing a notehead on the same line or space). Reviewers change them to the standard clefs before release.

## The editorial report (`report`)

What the report contains and how it is laid out.

<a id="report.contents"></a>

### `report.contents`: What is reported

*house*; applies [`declare.report-deviations`](principles-rules.md#declare.report-deviations)

Report any deviation from the source that is not visibly marked in the score. The report covers at least the following.

- Consistency edits within `read.consistency-by-equivalence`.

- Normalised terms and abbreviations.

- Added accidentals (also bracketed in the score).

- Clef changes and modernisation.

- Composer-led or house-style grouping decisions that were not obvious.

- System and page breaks omitted.

- Ornaments or details entered in the nearest available form.

- Excluded categories of mark.

- Which brackets are ours, where the source also uses square brackets (`brackets.tell-apart`).

Earlier codes: R1.

<a id="report.systematic-vs-specific"></a>

### `report.systematic-vs-specific`: Systematic and specific entries

*house*; applies [`declare.report-deviations`](principles-rules.md#declare.report-deviations)

State systematic differences once, in a general note that lists the normalisations applied. Give each specific intervention one row, with bar, part or staff, source reading, our reading, reason and rule ID.

- *Example:* A clef is changed in a cello part. b. 34, Vc.: clef changed to tenor; passage stays above the stave for 9 bars (`clef.leger-line-test`).

Earlier codes: R2.

<a id="report.header"></a>

### `report.header`: Report header

*house*; applies [`declare.record-provenance`](principles-rules.md#declare.record-provenance)

Source edition and file, pages, transcriber, reviewer, date, the app and version, the Principles version, the profile, the Notes version, and the normalisations applied (also recorded in the transcription's machine-readable metadata, the sidecar).

Earlier codes: R3.

<a id="report.purpose"></a>

### `report.purpose`: Purpose of the report

*house*; applies [`declare.report-deviations`](principles-rules.md#declare.report-deviations)

The report is for readers who need to know how the score differs from its source. It should be possible to read the score without the report, and to recover what the source prints from the two together.

Earlier codes: R5.

## Editorial matters (`editorial`)

Out of scope for the transcription and the version of record. Suggestions for handing observations on and for downstream work.

<a id="editorial.observations"></a>

### `editorial.observations`: Observations

*editorial*; applies [`stance.judgement-stays-out`](principles-rules.md#stance.judgement-stays-out)

If you notice something that looks like a source error, a divergence between parts or repeated passages, or a question an editor would want to ask, record it as an observation in a separate section of the report, not in the score. Say where it is, what the source prints, and why it caught your eye. Observations are not decisions. A clear source error may later be proposed for the corrections layer.

Earlier codes: E1, R4.

<a id="editorial.do-not-resolve"></a>

### `editorial.do-not-resolve`: Do not resolve

*editorial*; applies [`stance.judgement-stays-out`](principles-rules.md#stance.judgement-stays-out)

Do not choose between readings, supply missing material or "improve" the score, however obvious it seems.

Earlier codes: E2.

<a id="editorial.downstream-editions"></a>

### `editorial.downstream-editions`: Downstream editions

*editorial*; applies [`stance.judgement-stays-out`](principles-rules.md#stance.judgement-stays-out)

Anyone preparing an edition (harmonising recurring motives or articulation across parts, adding suggested accidentals, choosing between sources, dropping the source's own brackets) should start from a pinned VoR version, work in their own project, and report every change there. Use an established scheme to record the interventions, such as the editorial markup in MEI or TEI. The previous guide's consistency edits, 'obvious' corrections and editorial accidentals belong at this layer.

Earlier codes: E3.

<a id="editorial.comparing-sources"></a>

### `editorial.comparing-sources`: Comparing sources

*editorial*

An optional, judgement-free comparison between transcriptions of the same work is planned. Editions may use it as a starting point.

Earlier codes: E4.

## Not yet covered

To be added as core rules if general, or as Notes if house style. Until then, ask your reviewer (`workflow.ask-reviewer`) and record the decision in the report.

- Lyrics: underlay, hyphenation, melismas, translations.
- Piano pedalling.
- Articulations, fermatas, repeats and voltas.
- Rehearsal marks, bar numbering, multi-bar rests.
- Hairpins (beyond their placement in `layout.above-below`).
- Ornaments other than grace notes (trills, turns, mordents).
- Courtesy accidentals already in the source.

## Concordance with the previous guide

Codes not listed here moved to the core rules; see the concordance in the [rules table](principles-rules.md).

| Earlier code | Note |
|---|---|
| B1 | `brackets.source-marks` |
| B2 | `brackets.ours` |
| B3 | `brackets.source-marks` |
| B4 | `brackets.tell-apart` |
| C1 | `clef.two-clefs-default` |
| C2 | `clef.preserved-clefs` |
| C2.1 | `clef.preserved-clefs` |
| C2.2 | `clef.preserved-clefs` |
| C2.3 | `clef.preserved-clefs` |
| C3 | `clef.leger-line-test` |
| C4 | `clef.other-clefs-modern` |
| C5 | `clef.no-stem-flips` |
| D2 | `dynamics.terms` |
| D2.1 | `dynamics.terms` |
| D3 | `dynamics.abbreviations` |
| D4 | `dynamics.spread-words-line` |
| D5 | `dynamics.ritardando-line` |
| E1 | `editorial.observations` |
| E2 | `editorial.do-not-resolve` |
| E3 | `editorial.downstream-editions` |
| E4 | `editorial.comparing-sources` |
| G4 | `workflow.consistency-edits` |
| G5.1 | `playing.standard-entries` |
| G5.2 | `text.translation-format` |
| G6 | `workflow.manuscripts` |
| G7 | `workflow.ask-reviewer` |
| K1.1 | `key.no-cancelling-naturals` |
| K2 | `key.added-accidentals` |
| L1 | `layout.source-breaks` |
| L1.1 | `layout.source-breaks` |
| L1.2 | `layout.source-breaks` |
| L2 | `layout.above-below` |
| L2.1 | `layout.above-below` |
| L2.2 | `layout.above-below` |
| M1 | `metadata.title-composer-lyricist` |
| M2 | `metadata.dedication` |
| M3 | `metadata.dates-not-shown` |
| M4 | `metadata.composition-date` |
| M5 | `metadata.provenance-stored` |
| O2 | `ornaments.placement-default` |
| O3 | `ornaments.nearest-form` |
| P1 | `playing.standard-entries` |
| P2 | `playing.harmonics` |
| P3 | `playing.string-indications` |
| P4 | `playing.fingerings-excluded` |
| P4.1 | `playing.fingerings-excluded` |
| P5 | `playing.standard-entries` |
| R1 | `report.contents` |
| R2 | `report.systematic-vs-specific` |
| R3 | `report.header` |
| R4 | `editorial.observations` |
| R5 | `report.purpose` |
| S2 | `ties.accidental-across-tie` |
| T2 | `rhythm.beaming-default` |
| T2.1 | `rhythm.beam-placement` |
| T2.2 | `rhythm.beaming-default` |
| T2.2.1 | `rhythm.composer-led-signals` |
| T2.2.2 | `rhythm.beam-across-break` |
| T3 | `rhythm.rest-grouping` |
| T4 | `rhythm.tuplet-settings` |
| T4.1 | `rhythm.tuplet-settings` |
| T4.2 | `rhythm.tuplet-settings` |
| T5 | `rhythm.tremolo-default` |
| T6 | `rhythm.tempo-marks` |
| W1 | `workflow.red-text` |
| W2 | `workflow.report-transfer` |
| W3 | `workflow.source-errors` |
