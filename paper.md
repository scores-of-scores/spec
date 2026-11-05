# Faithful to the End: Clear but Nuanced Rules of Thumb for "Direct" Transcription of Musical Scores

## Abstract

In projects like the OpenScore lieder and string quartets,
we have aimed first and foremost to make scores that are useful to musicians and others.
Secondarily, we have tried to limit editorial interventions to a minimum: simply "copy sources directly".
Naturally, these two principles of "useful" and "copy" are frequently in conflict,
and the feasibility of a no-editing policy is a long-running, interesting, and recurring question.
In OpenScore we have alighted on a position where we copy a source as directly as possible,
making changes only in the case of clear errors.
This is logical enough, but it calls for more clarity on what counts as an error,
and on what counts as an acceptable divergence simply because of a change of medium,
defined by the functional limits of a format (e.g., MuseScore, MusicXML, KRN).
This paper proposes a formal framework for such decisions.
It expresses two positions in terms of that framework:
the OpenScore position, and a second, at the extreme of proximity to the source,
in which errors are deliberately preserved and flagged rather than corrected.
Together they serve as examples for any project making different decisions around the same options.

## Introduction: On "Neutral" Transcription from Page to Digital Document

A composer sits down and writes out a composition on paper, by hand.
The piece of paper is then filed away and largely forgotten.
Much later it is recovered, and we begin to attempt a transcription into modern notation software.

Among the many markings is what appears to be a slur.
First, note the hesitation: we do not always know enough even to make that categorical assignment.
Is it really a slur, or a different semantic marking (such as a tie),
or even nothing at all (an accidental smudge to be ignored)?
Second, assuming we settle on "slur" as a category, most modern software quite reasonably nudges us to commit to the starting and ending notes to which it is attached.
Again the manuscript leaves this ambiguous, calling for more deduction.
(This comes up as a real issue in many more cases than the categorical question of step 1.)
Finally, with our "slur" category and its starting and ending notes assigned, we might choose to specify the position and curve more exactly,
for example to start a little to the right of the notehead, to capture the source.

These are perhaps especially pertinent questions in the transcription of manuscript sources,
but printed sources do not remove them outright.

What a mark is, what it attaches to, and how much of its appearance matters are all still open questions.

Moreover, printed sources often introduce new questions
such as publishers editorial norms, e.g., over such as how to group rests in 6/8.
These may be visually clear in the source, but not so clearly "important" to the essence of the piece:
does the beaming reflect an editorial house style, or compositional intent?
Should this detail be encoded, even if it opposes the destination format/app's defaults?
Stem direction provides another example, with a distinction often offered between up, down, and auto/unspecified.
If auto/unspecified gives the wrong direction, should that be overridden with a commitment?
Does it matter?
Should there be some additional conditional editing, such that if the piece is transposed, or the clef changed, the stem-direction details are dropped or changed?

These kinds of questions propagate through every symbol in every piece,
and can quickly move from a relatively peripheral position to become the whole story.
In extremely detailed editorial work of the kind seen in Beethovens Werkstatt,
it makes perfect sense to capture as much as possible, one way or another.
In more general use cases such as the OpenScore corpora, we seek a balance.
And although there are countless books on general editorial best practice
(of which Gould seems to be a firm favourite),
these guides tend to focus on abstract best practice, away from editorial house style and
(relatedly) the in-app, format-specific defaults
(which defaults might well be seen as their own kind of house style).

What is needed, then, is a balanced framework.
It should be robust enough to itemise rules, but flexible enough to treat those rules as "rules of thumb"
and to distinguish between kinds of decisions and the criteria for intervening.
In the digital age, it should also serve to define the known gap between a PDF source and a digital encoding:
which differences are neutral (gaps between defaults, or limits of the format),
which are editorial interventions to be debated, and
which are errors, to be corrected or at least flagged/

Each project for a specific use case will take a view of the questions raised above.
That divergence only serves to enhance the motivation for creating a general framework which expresses those
priorities and (by extension) differences.
The framework is the primary technical goal of this repository.
This paper serves to introduce and motivate that effort.
Two worked cases serve to illustrative the range:
OpenScore, which copies a source relatively directly, but does correct "clear" errors;
and Scores of Scores, which sits at the extreme of proximity to the source,
recording what is printed, errors included, and keeping every judgement outside the transcription.

---

# Plan for the remaining sections

Overall, the framework is one set of options with several defensible settings.
The two cases explore this and recur throughout the paper.

## Background and related work

- Editorial and notation practice:
Gould; diplomatic versus critical editions; Beethovens Werkstatt as the maximal pole.
- What encoding formats can and cannot express
(comparison of MuseScore, MusicXML, KRN, MEI).
- Corpus and OMR ground-truth practice (KRN, OMR-NED).
- Wider standards this framework borrows from
(MEI, TEI, BCP 14, provenance and citation standards).

## Concepts

- Define: source, transcription, encoding, format, house style.
- Three separate axes:
the kind of decision (does it need judgement or another source?);
what the format can express;
the strength a project assigns.
- Define "proximity to the source", "direct", "pragmatically faithful".

## The framework

- Layers: core, profile, local notes.
- Anatomy of a rule; permanent IDs; versioning.
- The boundary test and the three tiers.
- Tensions and their explicit resolution by the profile.
- The closed list of presentation normalisations.
- Mark categories and the *unsupported* treatment (a limit of the format, not a judgement).
- Describe the design; cite the repository by version and DOI.
- Box: "State as of 2026-11" (counts, domains, profile values).

## Two positions, one framework

One table of choices, then the reasoning behind each.
Rows come from the profile's dimensions; only what the existing documents state is filled in.

| Choice                              | OpenScore                     | Scores of Scores                                                     |
|-------------------------------------|-------------------------------|----------------------------------------------------------------------|
| Evident source error                | Corrected when clear          | Kept as printed, flagged; fixed only in a separate corrections layer |
| Who decides what counts as an error | Named OpenScore reviewers     | Nobody within the transcription (judgement stays out)                |
| Presentation normalisations         | MuseScore defaults + template | Limited: a closed, registered list, stated once per transcription    |
| Format limits                       | Mostly excluded               | Classed as unsupported; reclassifiable by the profile                |
| "Useful" vs "copy" conflict         | Useful over copy              | Copy over useful (judgement-free record)                             |


## Worked examples

Expand on the introduction's examples and the solutions in the two respective cases.
For each, give the tier or treatment and what is reported.

- The slur: a reading ambiguity.
- 6/8 beaming: composer-led versus house style.
- Stem direction: default versus override.
- A bar that does not add up: where the two positions diverge.
- Fingering: a format limit.

Musical examples (images) would be useful here.

## Implementation

- The registry as data; validation; generated documents and reports; provenance.
- Keep short.
- An illustration e.g., build catching a Note that cites a renamed rule.

## Evaluation

- Apply both profiles to the same excerpts; categorise where they differ
(cf [editorial](https://fourscoreandmore.org/openscore/stringquartets/editorial)).
- Classify historical OpenScore reviewer comments against the rules to test coverage.
- Optionally: inter-transcriber agreement on tiering.
- MG Mozart example

## Discussion

- "Clear error" as a matter of degree.
- What "in doubt, preserve" shifts onto downstream users.
- How format limits move over time.
- Thesis to test: the OpenScore output can be derived from the extreme-proximity record plus a corrections layer, making the two positions layered rather than rivals.
- Where usefulness lives (presentation and meaning over appearance); answer the abstract's first aim explicitly.

## Conclusion, Outlook, and Future work

The editorial layer; uncovered topics; further profiles; other source types.

## Supplementary material

A tagged release with a DOI; the rules table; a profile skeleton.

---
