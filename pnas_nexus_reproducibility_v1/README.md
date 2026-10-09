# Reproducibility materials

This directory accompanies the PNAS Nexus manuscript *Language models compress
human preference geometry while political structure remains prompt-sensitive*.

It contains:

- the submitted Main and Supporting Information sources;
- aggregate, confirmed-adult source tables used for the reported results;
- scientific prompt specifications and response-decoding rules;
- five analysis notebooks;
- pinned Python environments; and
- utilities that verify the release and reproduce headline summaries.

It contains no direct identifiers, private participant-level joins, model
weights, or inference infrastructure. The DYNAMAP implementation is not part of
this release; reported aggregate fit outputs and initialization-sensitivity
summaries are included.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r environment/requirements-analysis.txt
make verify PYTHON=.venv/bin/python
make reproduce-analysis PYTHON=.venv/bin/python
make test-notebooks PYTHON=.venv/bin/python
```

`make verify` checks release integrity, manuscript assets, cohort declarations,
and the absence of participant identifiers. `make reproduce-analysis` rebuilds
the compact headline verification table from the distributed aggregate source
tables. `make test-notebooks` executes all distributed notebooks in a temporary
directory.

## Directory guide

- `config/`: confirmed-adult cohort definitions.
- `environment/`: pinned analysis requirements.
- `manuscript/`: submitted LaTeX sources, figures, and source tables.
- `notebooks/`: concise exploratory and verification notebooks.
- `prompts/`: scientific prompt specification and decoding rules.
- `results/source_data/`: machine-readable aggregate results.
- `scripts/` and `src/`: verification and reproduction utilities.

## Citation

Citation metadata are provided in `CITATION.cff`.

