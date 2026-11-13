# Glossary

*Generated from `core/glossary.yaml`. The same terms are used in the rules, the Notes and the paper.*

| Term | Meaning |
|---|---|
| **Source** | The notated document being transcribed, one edition or one manuscript, identified by file and pages. |
| **Transcription** | The digital encoding of one source, made under a profile. Also the name of the tier of decisions that need no judgement and no second source. |
| **Encoding** | A file or set of files that records a transcription in one format. |
| **Format** | A specification that defines how music is encoded (KRN, MusicXML, MEI, MuseScore's native MSCX). A format sets what can be expressed. It is not the same as an application that reads or writes it. |
| **Application** | A program such as MuseScore, whose defaults act as a house style that the format does not set. |
| **Version of record (VoR)** | The exact transcription of one source, errors included, identified by a pinned version. |
| **Tier** | One of three kinds of decision. Transcription needs no musical judgement and no second source. Presentation is systematic, reversible and changes nothing notated. Editorial needs judgement or another source. |
| **Normalisation** | A registered presentation choice such as beam grouping or clefs. The list is closed. |
| **Profile** | A project's choices over the core rules, the format of its version of record, and the treatment of marks. In the paper a profile is also called a position. |
| **Strength** | MUST, SHOULD, MAY or OFF (BCP 14). MUST is always applied, SHOULD unless there is a recorded reason, MAY at discretion, OFF not adopted. For a normalisation or a correction, OFF means not permitted. |
| **Format feature** | One entry in the formats data (fmt.*) that states, for each of four formats, whether and how it can express something, and on what evidence. |
| **Status** | The capability label of a format feature cell. Direct, qualified, extension, workaround or unknown. It is not a quality score. |
| **Unsupported** | The treatment of a category of printed mark that the profile's format cannot express. Derived from the formats data. It is a limit of the format, not a judgement, and changes when the format or the profile does. |
| **Observation** | A point recorded in the report (a possible source error, a divergence, a mark with more than one reading, an unclear tier). It does not change the transcription. |
| **Clear error** | A source error that passes the two-part test in correct.error-test. Every other error is kept as printed. |
| **Correction** | A change to the printed reading of a clear error, made either in the transcription (correct.in-place) or in a separate layer (correct.layer), and always recorded (correct.record). |
| **Corrections layer** | A layer separate from the transcription, pinned to a transcription version, that records corrections. The corrected view is derived from the transcription and the layer. |
| **Note kinds** | Presentation (a choice among permitted normalisations), tool (settings that may change between applications), house (a house convention) and editorial (a suggestion for downstream work, never applied in the version of record). |
| **Sidecar** | The machine-readable metadata stored with each transcription: source, pages, tools, versions and the normalisations applied. |
| **Collation** | A derived record of where transcriptions of the same work differ, without choosing between them. |
| **Fixture** | A defined test situation that exercises format features and, for the worked examples, rules. A feature cell counts as tested only when a fixture covering it has a recorded result for that format. |
