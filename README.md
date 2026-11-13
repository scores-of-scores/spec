# Scores of Scores: Transcription Principles, Format Evidence and Notes

Rules for making "exact", citable digital transcriptions of a printed score, the evidence of what each encoding format can express, and the profiles that record different projects' choices, so that editorial projects and other users can build on them.

Version **2026-11**.

**Read it:** [`site/index.html`](site/index.html) is a single stand-alone page (no server, no external files) with the rules and Notes, and [`site/formats.html`](site/formats.html) is the format reader. Or read the Markdown:

<!-- BEGIN docmap -->
| Document | Answers | Audience |
|---|---|---|
| [Start here](docs/start-here.md) | A short orientation to the rules and how they fit together | Everyone |
| [Principles framework](docs/principles-framework.md) | How the layers work, the tiers and boundary test, rule anatomy, relations, derived treatments, versioning, adoption | Anyone, including other projects |
| [Rules table](docs/principles-rules.md) | Every rule, with its strength and relations in each profile, priorities and scope (generated) | Transcribers, reviewers, other projects |
| [Format support](docs/format-support.md) | What each of four formats can express for each rule, and what follows in each profile (generated) | Profile authors, transcribers |
| [Format reader](site/formats.html) | The full formats dataset as a searchable matrix, with worked cases and sources (generated) | Anyone choosing or comparing formats |
| [Notes for Transcribers](docs/notes-for-transcribers.md) | Day-to-day local notes for the Scores of Scores profile (generated) | Transcribers and reviewers |
| [Glossary](docs/glossary.md) | The terms used across the documents (generated) | Everyone |
| [Project overview](docs/overview.md) | Scope, pipeline and conventions of the wider project | Developers, maintainers, funders |
| [Paper](paper/paper.md) | The framework, the two worked positions and the evidence for them | Researchers |
<!-- END docmap -->

Rules and Notes are cited by permanent ID, for example `read.preserve-errors` or `workflow.unclear-cases`; format features as `fmt.fingering`.

## Repository layout

```
core/         principles.yaml (rules, source of truth), glossary.yaml
formats/      formats.yaml, sources.yaml, features/<category>.yaml, cases.yaml, fixtures.yaml
profiles/     sos-2026-11.yaml, openscore-2026-11.yaml (draft)
notes/        registry.yaml (local notes, source of truth), preamble.md
schemas/      JSON Schemas for every YAML file
tools/        build.py (validate and generate), build_site.py, gen_*.py, templates/
tests/        verify_formats.py (the reader's search, filter and export logic), test_checks.py
docs/         hand-written and generated Markdown
paper/        paper.md (tables are generated)
build/        machine-readable outputs: principles.json/csv, notes.json, formats.json/csv
site/         index.html, formats.html (generated, stand-alone)
```

**Generated files:** everything in `build/` and `site/`, `docs/principles-rules.md`, `docs/format-support.md`, `docs/glossary.md`, `docs/notes-for-transcribers.md`, the document maps in this README and `docs/overview.md`, and the tables between markers in `paper/paper.md`. Edit the YAML, not the output.

## Build

```
pip install -r requirements.txt
python3 tools/build.py          # validate every layer and link, then generate everything
python3 tools/build.py check    # validate only
python3 tests/verify_formats.py # needs Node.js; checks the format reader
python3 tests/test_checks.py    # confirms that the build rejects eight kinds of inconsistency
```

`build.py` exits non-zero if anything is inconsistent: an unknown rule, note or feature reference, a tension with no precedence, a cycle in precedence, a rule adopted while one it requires is OFF, a Note that applies a normalisation the profile does not permit, a derived mark treatment that a fixture contradicts, a duplicate ID or alias, and so on. CI runs it on every push.

## Use the data

`build/principles.json` and `build/principles.csv` carry every rule with its strength in each profile; `build/notes.json` carries every Note; `build/formats.json` and `build/formats.csv` carry every format feature, cell and linked rule.

## Adopt the Principles

Take `core/principles.yaml` and `formats/` unchanged, write your own profile and notes, and run the build. See section 8 of the [framework](docs/principles-framework.md).

## Cite

See [`CITATION.cff`](CITATION.cff). Cite a rule as `read.preserve-errors@2026-11` and a format feature as `fmt.fingering@2026-11`.

## Licence

Text, data and schemas are CC BY 4.0; code is MIT. See [`LICENSE.md`](LICENSE.md).
