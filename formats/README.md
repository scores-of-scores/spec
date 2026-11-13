# Formats data

What each of four encoding formats can express: KRN (core Humdrum `**kern`, with named dialects labelled), MusicXML 4.0, MuseScore 4's native format (MSCZ/MSCX) and MEI 5.1. This is the evidence layer of the Transcription Principles. It is read by the build, linked to the rules, and rendered as [`site/formats.html`](../site/formats.html).

| File | Holds |
|---|---|
| `formats.yaml` | The four formats, the status vocabulary, the categories, the methodology |
| `features/<category>.yaml` | The features of one category: ID (`fmt.<slug>`), question, tags, importance and four cells |
| `sources.yaml` | Primary sources, each with the date it was accessed |
| `cases.yaml` | Worked comparisons of one situation across the four formats |
| `fixtures.yaml` | Test fixtures; those marked `paper` are the worked examples in the paper |

**A cell** has a status (direct, qualified, extension, workaround, unknown), a summary, the mechanism, any condition, a workaround, an evidence label (documented, inference, unverified), sources and a `subset` (the schema subset, customization or extension it refers to). An `extension` cell must name the extension.

**Status is not a score.** The labels are not ordinal, no overall winner is calculated, and a format is chosen by a profile (`scope.encoding`), not by this dataset.

**Evidence.** "Documented" means the cited documentation states the mechanism or limitation; it does not mean a converter was tested. "Inference" is an author's interpretation. "Unverified" is a deliberately open question, not a statement of absence. No format round-trip or playback test has been run. A cell is tested only when a fixture that covers it has a recorded `results` entry for that format; do not set a result merely because a file opens or validates.

**Updating.** Edit the YAML, keep IDs stable where the meaning is unchanged, add primary sources with an accessed date, run `python3 tools/build.py`, and record any change in the changelog. Coverage prioritises divergences; specialist non-Western notations, complete electroacoustic scoring, braille conversion and DAW or MIDI 2.0 workflows are outside the detailed matrix. Version-sensitive statements should be rechecked when a format changes.
