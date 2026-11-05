# Scores of Scores: Transcription Principles and Notes

Rules for making "exact", citable digital transcription of a printed score,
so that editorial projects and other users can build on it.

Version **2026-11 (draft, formal semantic versioning to follow)**.

**Read it:** [`site/index.html`](site/index.html) is a single stand-alone page
(no server, no external files) built from the documents below.
Or read them as Markdown:

| Document                                                 | Purpose                                                                   |
|----------------------------------------------------------|---------------------------------------------------------------------------|
| [Start here](docs/start-here.md)                         | A short orientation, with a glossary                                      |
| [Principles framework](docs/principles-framework.md)     | How the rules are organised: layers, tiers, relations, versioning         |
| [Rules table](docs/principles-rules.md)                  | Every rule, with its strength and relations in our profile (generated)    |
| [Notes for Transcribers](docs/notes-for-transcribers.md) | Day-to-day local notes: tools, house style, workflow, reports (generated) |
| [Project overview](docs/overview.md)                     | The wider project and its document map                                    |

Rules and Notes are cited by permanent ID, for example `read.preserve-errors` or `workflow.ask-reviewer`.

## Repository layout

```
principles/registry.yaml   core rules (source of truth)
profiles/sos-2026-11.yaml  our choices: strengths, precedence, scope
notes/registry.yaml        local notes (source of truth)
notes/preamble.md          introduction to the generated Notes
schemas/                   JSON Schemas for the three YAML files
tools/build.py             validate everything and generate docs/ and build/
tools/build_site.py        build the stand-alone page, site/index.html
docs/                      hand-written and generated Markdown
build/                     machine-readable outputs: principles.json, principles.csv, notes.json
```

**Generated files**:
Everything in `build/` as well as `docs/principles-rules.md` and `docs/notes-for-transcribers.md`. 
Edit the YAML, not the output.

## Build

```
pip install -r requirements.txt
python3 tools/build.py        # validate, then write docs/ and build/
python3 tools/build_site.py   # write site/index.html (one self-contained file)
```

`build.py` exits non-zero if anything is inconsistent:
an unknown rule or note reference, a tension with no precedence, a cycle in precedence, a Note that applies a normalisation the profile does not permit, a duplicate ID or alias, and so on.
CI runs it on every push.

## Use the data

`build/principles.json`, `build/principles.csv` and `build/notes.json` carry every rule (with its strength in our profile) and every Note, flattened for use in other tools.

## Adopt the Principles

These principles are designed to be adopted and adaptable.

Take `principles/registry.yaml` unchanged, write your own profile and notes, and run the build.
See section 6 of the [framework](docs/principles-framework.md).

## Cite

See [`CITATION.cff`](CITATION.cff)
(placeholder, details to follow).
Cite a rule as `read.preserve-errors@2026-11`.

## Licence

See [`LICENSE`](LICENSE).
Possible split of code from schema to follow.
