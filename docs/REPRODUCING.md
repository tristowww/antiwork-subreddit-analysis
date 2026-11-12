# Reproduction paths

Run commands from the repository root. Choose the path matching your available inputs.

## Public aggregate checks

Python 3.10+; no third-party dependencies or network calls:

```bash
python scripts/validate_public_aggregates.py
python -m unittest discover -s tests_public -v
```

The check reconciles monthly/yearly totals, assignment and outlier counts, candidate-theme counts, denominators, shares and included-cluster counts. It rejects duplicate or missing theme/window cells, non-finite values and inconsistent shares. Tests use temporary copies; originals are unchanged.

A pass establishes consistency of the shared summaries, not source-corpus accuracy, model validity or human agreement.

## Rebuild the example figure

```bash
python -m pip install "matplotlib>=3.8,<4"
python scripts/rebuild_aggregate_example.py
```

Default output, ignored by Git:

- `examples/output/aggregate_theme_comparison.png`
- `examples/output/aggregate_theme_comparison.svg`
- `examples/output/aggregate_example_summary.json`

The source is `candidate_theme_window_prevalence.csv`. Bars compare the first and last yearly windows using `share_all_posts`, with every filtered post in the corresponding window as denominator. The JSON records the source SHA-256 after normalizing text to UTF-8 with LF newlines, windows and exact plotted shares. Rendering may vary by environment; numerical checks do not.

The [committed preview](../examples/aggregate_theme_comparison.png) and [summary](../examples/aggregate_example_summary.json) can be inspected without installing anything. Original research figures are not overwritten.

## Full topic workflow

This path requires the authorized local corpus and intermediate files, which are not distributed here. Commands are retained from the existing workflow; the cleanup does not execute them.

```bash
python -m pip install -e ".[nlp,viz]"
python -m src.collaborator_analysis --out-dir outputs/v2_clean_min25
python -m src.theme_trends --out-dir outputs/v2_clean_min25 --codebook planning/CANDIDATE_THEME_CODEBOOK.csv
python -m src.theme_hierarchy
python -m src.topic_alignment --out-dir outputs/v2_clean_min25 --top-n 15 --threshold 0.2
```

The original `scripts/validate_handoff.py` checks the corpus, post-level assignments and handoff using local inputs. It is separate from the portable aggregate check. Consult [ROBUSTNESS.md](../planning/ROBUSTNESS.md) and the script before running it.

## Separate sentiment workflow

Read [SENTIMENT.md](../planning/SENTIMENT.md) first. With the required local inputs and dependencies:

```bash
python -m src.sentiment --overwrite
python -m src.theme_sentiment
```

This is model-based whole-post polarity, not human labels or management-targeted sentiment.

## Existing document builders

```bash
python -m pip install -e ".[docs]"
python scripts/build_collaborator_brief.py
python scripts/build_revised_manuscript.py
```

Choose the original builder and source edition deliberately. This cleanup does not rebuild or edit Word/PDF deliverables.
