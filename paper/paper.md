# Faithful to the End: Clear but Nuanced Rules of Thumb for "Direct" Transcription of Musical Scores

## Abstract

In projects like the OpenScore lieder and string quartets,
we have aimed first and foremost to make scores that are useful to musicians and others.
Secondarily, we have tried to limit editorial interventions:
to simply "copy sources directly".
Naturally, these two principles of "useful" and "copy" are frequently in conflict,
and the feasibility of a no-editing policy is a long-running, interesting, and recurring question.
OpenScore aims to copy a source as directly as possible,
making changes only in the case of clear errors.
This is logical enough, but it calls for more clarity on what counts as an error,
and on what counts as an acceptable divergence simply because of a change of medium,
defined by the functional limits of a format (e.g., MuseScore, MusicXML, KRN).
This paper proposes a formal framework for such decisions
and uses it to characterise two profiles in terms of that framework.
One is the OpenScore approach, broadly of light pragmatic editing for use;
the second, complementary profile sets out what extreme proximity to the source might look like.
This latter case can be useful for example in reporting the contents of source exactly,
for instance, in OMR benchmarking;
here even clear errors are deliberately preserved and recorded as observations, rather than corrected.
Together, this pair serves as examples for any project making different decisions,
while still characterising them according to the same framework.

## Introduction: On "Neutral" Transcription from Page to Digital Document

A composer sits down and writes out a composition on paper, by hand.
The piece of paper is then filed away and largely forgotten.
Much later it is recovered, and we begin to attempt a transcription into modern notation software.

Among the many markings is what appears to be a slur.
First, note the hesitation: we do not always know enough even to make such a categorical assignment.
Is it really a slur, or a different semantic marking (such as a tie),
or even nothing at all (an accidental smudge to be ignored)?
Second, assuming we settle on "slur" as a category,
most modern software quite reasonably nudges us to identify the starting and ending notes to which it is attached.
Again the manuscript leaves this ambiguous, calling for more deduction.
(And this is a real issue in many more cases than the categorical question with which we began.)
Finally, with our "slur" category and its starting and ending notes assigned,
we may or may not choose to specify the position and curve more exactly,
for example to start a little to the right of the notehead, to capture the source more exactly.

These are perhaps especially pertinent questions in the transcription of manuscript sources,
but even professionally printed and edited sources do not remove them outright.
What a mark is, what it attaches to, and how much (of) its appearance matters are all open questions.
Moreover, printed sources often introduce new questions
such as publishers' editorial norms, e.g., how to group rests in 6/8.
These may be visually clear in the source, but not so clearly "important" to the essence of the piece:
does the choice reflect an editorial house style, or compositional intent?
Should this detail be encoded, even if it opposes the destination format/app's defaults?
Stem direction provides another example, with a distinction often offered between up, down, and auto/unspecified.
If auto/unspecified gives the wrong direction, should that be overridden with a commitment?
Does it matter?
Should there be some additional conditional editing,
such that if the piece is transposed, or the clef changed,
then the stem-direction details are correspondingly dropped or changed?

These kinds of questions propagate through every symbol in every piece,
and can quickly move from a relatively peripheral position to become the whole story.
In extremely detailed editorial work of the kind seen in Beethovens Werkstatt,
it makes perfect sense to capture as much as possible, one way or another.
In more general use cases such as the OpenScore corpora, we seek a balance.
And although there are countless books on general editorial best practice
(of which Gould's _Behind Bars_ seems to be a firm favourite),
these guides tend to focus on abstract best practice, away from editorial house style and
(relatedly) the in-app, format-specific defaults
(which defaults might well be seen as their own kind of house style).

What is needed, then, is a balanced framework.
It should be robust enough to itemise rules, but flexible enough to treat them as rules "of thumb",
and to distinguish between kinds of decisions and the criteria for intervening.
In the digital age, it should also serve to define the known gap between a PDF source and a digital encoding:
which differences are presentation choices (gaps between defaults),
which are limits of the format,
which are editorial interventions to be debated, and
which are errors, to be corrected where clear, or otherwise recorded as observations?

Each project for a specific use case will take a view of the questions raised above.
That divergence only serves to enhance the motivation for creating a general framework which expresses those
priorities and (by extension) differences.
The framework, together with an inventory of what each format can express, is the primary technical goal of this repository.
This paper serves to introduce and motivate that effort.
Two positions serve to illustrate the range:
OpenScore, which copies a source relatively directly, but does correct clear errors;
and Scores of Scores, which sits at the extreme of proximity to the source,
recording what is printed, errors included, and keeping every judgement outside the transcription.

---

# Plan for the remaining sections

Overall, the framework is one set of options with several defensible settings.
The two positions explore this and recur throughout the paper.
The tables below are generated from the profiles, the rules and the formats data in the repository as it stands for reference.

## Background and related work

- Editorial and notation practice:
Gould; diplomatic versus critical editions; Beethovens Werkstatt as a _ne plus ultra_.
- What encoding formats can and cannot express
(MSCX, MusicXML, KRN, MEI):
the formats data, with evidence labels.
- Corpus and OMR ground-truth practice (KRN, OMR-NED).
- Wider standards this framework borrows from
(MEI, TEI, BCP 14, provenance and citation standards).

## Concepts

- Define: source, transcription, encoding, format, application, house style, position (a profile).
The glossary is the reference.
- Three separate axes, one per layer:
the kind of decision (does it need judgement or another source? the core and its tiers);
what the format can express (the formats data);
the strength a project assigns (the profile).
- Define "proximity to the source", "direct", "pragmatically faithful".
- At this stage, map the introduction's informal language onto the framework ... and perhaps revisit that intro ;) ...

| Introduction                 | Framework                                                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------------------------|
| Neutral gap between defaults | Presentation tier: a registered normalisation (`normalise.*`)                                             |
| Neutral limit of the format  | The *unsupported* treatment, derived from the formats data                                                |
| Editorial intervention       | Editorial tier: kept out of "transcription"                                                               |
| Error                        | Kept (`read.preserve-errors`) or corrected only when clear (`correct.error-test`) and the profile permits |

## The framework

- Layers: core, formats, profile, local notes.
- Anatomy of a rule; permanent IDs in one namespace; versioning.
- The boundary test and the three tiers.
- Tensions and their explicit resolution by the profile.
- The closed list of presentation normalisations.
- The clear-error test, and its two placements (in the transcription, or in a separate layer).
- Mark categories and the *unsupported* treatment:
derived from the status of a format feature in the profile's format and the extensions the profile accepts
(a limit of the format, not a judgement).
- Describe the design; cite the repository by version and DOI.
- Box: "State as of 2026-11", generated:

<!-- BEGIN state-box -->
- Principles version 2026-11: 36 rules (4 stance, 10 read, 3 encode, 11 normalise, 4 declare, 4 correct).
- Profiles: `openscore-2026-11`, `sos-2026-11`.
- Notes for the Scores of Scores profile: 52.
- Formats data 2026-11: 78 features in four formats (312 assessments), 21 linked to a rule, 133 primary sources.
- Fixtures: 17, of which 5 are worked examples in this paper. Assessments with a recorded test: 0.
<!-- END state-box -->

## What the formats can express

The features that the worked examples use, in the four formats.
Status is a capability label, not a score, and every cell is documented, inferred or unverified.

<!-- BEGIN paper-formats -->
| Feature                                                            | KRN                  | MusicXML  | MuseScore 4 (MSCX)    | MEI    |
|--------------------------------------------------------------------|----------------------|-----------|-----------------------|--------|
| `fmt.phrase-slur-tie`: Ties, slurs and analytical phrases          | Direct               | Qualified | Qualified (inferred)  | Direct |
| `fmt.spanner-geometry`: Spanner endpoints, curvature and open ties | Qualified            | Direct    | Qualified (inferred)  | Direct |
| `fmt.beam-geometry`: Beam grouping, feathering and cross-bar beams | Qualified            | Direct    | Direct                | Direct |
| `fmt.stem-direction`: Stem direction: explicit or automatic        | Direct               | Direct    | Direct                | Direct |
| `fmt.irregular-measures`: Pickups and incomplete / overfull bars   | Qualified            | Direct    | Direct                | Direct |
| `fmt.editorial-status`: Sic, interpretation and intervention       | Qualified            | Qualified | Workaround (inferred) | Direct |
| `fmt.annotations`: Machine-readable annotations and ranges         | Qualified            | Qualified | Workaround (inferred) | Direct |
| `fmt.fingering`: Printed fingering                                 | Extension (inferred) | Direct    | Direct                | Direct |
<!-- END paper-formats -->

## Two positions, one framework

One table of choices, then the reasoning behind each.
Rows come from the profile's dimensions.
The OpenScore column is a draft: it is a step towards fully formalising
[OpenScore's public-facing notes for transcribers](https://fourscoreandmore.org/scores-of-scores/notes-for-transcribers/).
Otherwise, it takes the core defaults, and the count of unconfirmed strengths is part of the table.

<!-- BEGIN two-positions -->
| Choice                                                | OpenScore profile                                                                        | Scores of Scores profile                                                                                               |
|-------------------------------------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Clear source error (`correct.error-test`)             | Corrected in the transcription (MUST), and recorded                                      | Kept as printed; the correction is recorded in a separate layer (MUST)                                                 |
| Source error that is not clear                        | Kept as printed; observation recorded                                                    | Kept as printed; observation recorded                                                                                  |
| Test for "clear"                                      | The same core test (`correct.error-test`, MUST)                                          | The same core test (`correct.error-test`, MUST)                                                                        |
| Presentation normalisations                           | 10 of 10 registered normalisations permitted, 7 always applied                           | 10 of 10 registered normalisations permitted, 7 always applied                                                         |
| Format of the version of record                       | MuseScore 4 (MSCX) (4.x, 4.6 family as reference)                                        | KRN (core **kern, Humdrum guide)                                                                                       |
| Marks left out because the format cannot express them | None                                                                                     | fingering                                                                                                              |
| Highest-ranked aim                                    | Meaning over appearance (useful to musicians first)                                      | Judgement stays out                                                                                                    |
| Where meaning and faithful reading conflict           | Meaning over appearance wins: Appearance, and source errors that pass correct.error-test | Meaning over appearance wins: Appearance only (grouping, placement, typography), through the registered normalisations |
| Status of the profile                                 | Draft: 7 of 36 strengths documented, 29 core defaults unconfirmed                        | Adopted                                                                                                                |
<!-- END two-positions -->

## Worked examples

Expand on the introduction's examples and the solutions in the two respective positions.
For each, give the tier or treatment and what is reported.
The table is generated from the fixtures; each example is also a test fixture for the formats.

<!-- BEGIN worked-examples -->
| Example                                                             | Rules                                                                                                                       | OpenScore profile                                                                                                                                  | Scores of Scores profile                                                                                                                                                                                                                                                              |
|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A curve that may be a slur, a tie or a smudge (`fx.slur-ambiguity`) | `read.ambiguous-marks`, `read.preserve-distinctions`, `declare.observations`, `encode.defaults-not-overrides`               | The same reading rule applies. The curve follows the MuseScore default (`encode.defaults-not-overrides`).                                          | A tie if the curve joins adjacent notes of the same pitch, otherwise a slur on the notes nearest its printed endpoints (`read.ambiguous-marks`). An observation names the alternative readings (`declare.observations`). The default curve is used (`encode.defaults-not-overrides`). |
| Beaming in 6/8: composer-led or house style (`fx.beaming-6-8`)      | `normalise.beam-grouping`, `read.composer-led-grouping`, `stance.doubt-means-preserve`                                      | The same three outcomes. The default is the MuseScore time-signature default.                                                                      | Edition-wide habit: normalised to the time-signature default and stated once (`normalise.beam-grouping`). Composer-led grouping: kept (`read.composer-led-grouping`). Cannot tell: kept as printed, with an observation (`stance.doubt-means-preserve`).                              |
| Stem direction: default or override (`fx.stem-direction`)           | `normalise.stem-placement`, `encode.defaults-not-overrides`                                                                 | Automatic: the MuseScore stem direction stays on Auto (`normalise.stem-placement`).                                                                | Automatic (`normalise.stem-placement`): no / or \ signifier is entered in the KRN.                                                                                                                                                                                                    |
| A bar that does not add up (`fx.bar-does-not-add-up`)               | `read.preserve-errors`, `correct.error-test`, `correct.in-place`, `correct.layer`, `correct.record`, `declare.observations` | Test fails: kept as printed, with an observation. Test passes: corrected in the transcription and recorded (`correct.in-place`, `correct.record`). | Test fails: kept as printed, with an observation. Test passes: kept as printed in the transcription (`correct.in-place` is OFF) and the correction is recorded in the separate layer (`correct.layer`, `correct.record`).                                                             |
| Printed fingering (`fx.fingering`)                                  | `read.transcribe-all-marks`                                                                                                 | Transcribed: MuseScore expresses fingering directly (`read.transcribe-all-marks`).                                                                 | Unsupported: KRN has no fingering in its core vocabulary and this profile accepts no extension for it. The category is left out and stated once in each report (`read.transcribe-all-marks`).                                                                                         |
<!-- END worked-examples -->

- The slur: a reading ambiguity (category, attachment and geometry are three separate levels).
- 6/8 beaming: composer-led versus house style.
- Stem direction: default versus override.
- A bar that does not add up: where the two positions diverge, and why "clear" is a matter of degree.
- Fingering: a format limit, derived rather than asserted.

Musical examples (images) would be useful here.

## Implementation

- The layers as data; validation, including the links between layers; generated documents and reports; provenance.
- Keep short.
- An illustration e.g., build catching a Note that cites a renamed rule, or a fixture whose expected treatment disagrees with the derivation.

## Evaluation

- Apply both profiles to the same excerpts; categorise where they differ
(cf [editorial notes PoC](https://fourscoreandmore.org/openscore/stringquartets/editorial)).
- Classify historical OpenScore reviewer comments against the rules to test coverage and consistency.
- Run the fixtures in the formats data, so that cells move from documented to tested.
- Optionally: inter-transcriber agreement on tiering and on the clear-error test.
- MG Mozart example and wider robust contextual evidence.

## Discussion

- "Clear error" as a matter of degree: the two conditions of the test, and what each excludes.
- What "in doubt, preserve" shifts onto downstream users.
- How format limits move over time: a changed cell changes a derived treatment in a new pinned version.
- Thesis to test: the OpenScore output can be derived from the extreme-proximity record plus a corrections layer, making the two positions layered rather than rivals.
The formats data bounds the thesis: the derivation holds only for what the target format can express, and the editorial-status and annotation rows show where it would lose information.
- Where usefulness lives (presentation and meaning over appearance); answer the abstract's first aim explicitly.

## Conclusion, Outlook, and Future work

- The corrections layer and the downstream editorial layer;
- uncovered topics;
- further profiles;
- other source types.

## Supplementary material

- A tagged release with a DOI;
- the rules table;
- a profile skeleton;
- the formats data and fixtures.
