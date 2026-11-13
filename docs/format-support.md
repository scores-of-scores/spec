# Format support for the rules

*Generated from `core/principles.yaml`, `formats/` and the profiles. Formats data version 2026-11, research date 2026-11-06. Do not edit by hand.*

Each rule that depends on what a format can express is linked to the features in the formats data that bear on it. The table shows the status of each feature in four formats, then whether the feature is expressible in each profile's format. Status is a capability label, not a quality score, and every cell is documentation-based, inferred or unverified; none has been tested by conversion (see [the formats reader](../site/formats.html) for mechanisms, conditions and sources).

Expressible natively means the status is direct or qualified, or an extension that the profile accepts. "No" does not mean the rule fails: the point is then met in the report or through a workaround rather than in the encoding, and for a category of printed mark the derived treatment follows `read.transcribe-all-marks`.

| Rule | Feature | KRN | MusicXML | MuseScore 4 (MSCX) | MEI | `openscore-2026-11` | `sos-2026-11` |
|---|---|---|---|---|---|---|---|
| `stance.faithful-reading` | `fmt.version-profile`: Version and dialect are part of the answer | Qualified | Direct | Qualified | Qualified | yes | yes |
| `stance.faithful-reading` | `fmt.exact-appearance`: Exact visual reproduction | Qualified (inferred) | Qualified | Qualified (inferred) | Qualified | yes | yes |
| `read.preserve-distinctions` | `fmt.phrase-slur-tie`: Ties, slurs and analytical phrases | Direct | Qualified | Qualified (inferred) | Direct | yes | yes |
| `read.preserve-distinctions` | `fmt.time-signature-symbol`: Common and cut time symbols versus numeric signatures | Qualified | Direct | Direct (inferred) | Direct | yes | yes |
| `read.preserve-distinctions` | `fmt.grace-timing`: Grace-note timing versus written value | Qualified | Direct | Qualified | Direct | yes | yes |
| `read.preserve-errors` | `fmt.irregular-measures`: Pickups and incomplete / overfull bars | Qualified | Direct | Direct | Direct | yes | yes |
| `read.preserve-errors` | `fmt.annotations`: Machine-readable annotations and ranges | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |
| `read.record-source-marks` | `fmt.editorial-accidentals`: Editorial accidentals / musica ficta | Extension | Direct | Qualified (inferred) | Direct | yes | yes (extension accepted) |
| `read.transcribe-all-marks` | `fmt.fingering`: Printed fingering | Extension (inferred) | Direct | Direct | Direct | yes | no (extension not accepted) |
| `read.ornaments-as-printed` | `fmt.grace-timing`: Grace-note timing versus written value | Qualified | Direct | Qualified | Direct | yes | yes |
| `read.ornaments-as-printed` | `fmt.ornament-realization`: Ornament sign versus realised notes | Qualified | Qualified (inferred) | Qualified | Qualified (inferred) | yes | yes |
| `read.ambiguous-marks` | `fmt.phrase-slur-tie`: Ties, slurs and analytical phrases | Direct | Qualified | Qualified (inferred) | Direct | yes | yes |
| `read.ambiguous-marks` | `fmt.spanner-geometry`: Spanner endpoints, curvature and open ties | Qualified | Direct | Qualified (inferred) | Direct | yes | yes |
| `encode.real-objects` | `fmt.phrase-slur-tie`: Ties, slurs and analytical phrases | Direct | Qualified | Qualified (inferred) | Direct | yes | yes |
| `encode.real-objects` | `fmt.spanner-geometry`: Spanner endpoints, curvature and open ties | Qualified | Direct | Qualified (inferred) | Direct | yes | yes |
| `encode.defaults-not-overrides` | `fmt.stem-direction`: Stem direction: explicit or automatic | Direct | Direct | Direct | Direct | yes | yes |
| `encode.defaults-not-overrides` | `fmt.visual-accidental`: Printed accidental versus effective pitch | Qualified | Direct | Qualified (inferred) | Direct | yes | yes |
| `encode.layout-as-data` | `fmt.page-breaks`: Page/system breaks and spacing | Extension (inferred) | Qualified | Direct | Qualified | yes | yes (extension accepted) |
| `normalise.beam-grouping` | `fmt.beam-geometry`: Beam grouping, feathering and cross-bar beams | Qualified | Direct | Direct | Direct | yes | yes |
| `normalise.tuplet-brackets` | `fmt.nested-tuplets`: Nested and complex tuplets | Qualified | Direct | Direct | Direct | yes | yes |
| `normalise.stem-placement` | `fmt.stem-direction`: Stem direction: explicit or automatic | Direct | Direct | Direct | Direct | yes | yes |
| `normalise.accidental-conventions` | `fmt.visual-accidental`: Printed accidental versus effective pitch | Qualified | Direct | Qualified (inferred) | Direct | yes | yes |
| `normalise.clef` | `fmt.written-sounding`: Written versus sounding pitch | Direct | Direct | Direct | Direct | yes | yes |
| `normalise.page-geometry` | `fmt.page-breaks`: Page/system breaks and spacing | Extension (inferred) | Qualified | Direct | Qualified | yes | yes (extension accepted) |
| `declare.mark-additions` | `fmt.editorial-accidentals`: Editorial accidentals / musica ficta | Extension | Direct | Qualified (inferred) | Direct | yes | yes (extension accepted) |
| `declare.observations` | `fmt.annotations`: Machine-readable annotations and ranges | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |
| `declare.record-provenance` | `fmt.metadata`: Bibliographic and source metadata | Direct | Qualified | Qualified | Direct | yes | yes |
| `declare.record-provenance` | `fmt.source-description`: Physical source, hands and provenance | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |
| `correct.layer` | `fmt.editorial-status`: Sic, interpretation and intervention | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |
| `correct.layer` | `fmt.annotations`: Machine-readable annotations and ranges | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |
| `correct.layer` | `fmt.persistent-addresses`: Stable addresses for notes and annotations | Extension (inferred) | Qualified | Unverified (unverified) | Direct | no | no (extension not accepted) |
| `correct.record` | `fmt.editorial-status`: Sic, interpretation and intervention | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |
| `correct.record` | `fmt.annotations`: Machine-readable annotations and ranges | Qualified | Qualified | Workaround (inferred) | Direct | no | yes |

21 of 78 features are linked to at least one rule. The other 57 are context for choosing or comparing formats and carry no rule.

## Mark categories

| Category | Feature | `openscore-2026-11` | `sos-2026-11` |
|---|---|---|---|
| `fingering` | `fmt.fingering` | transcribe | unsupported |
