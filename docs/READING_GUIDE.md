# Reading guide

This guide explains the analysis stages and supporting evidence. It adds navigation; it does not select a final manuscript, revise a result or replace the original notes.

## Begin with the shared evidence

| Material | What it establishes | Limit |
| --- | --- | --- |
| [README](../README.md) | Question, saved scope and selected results | Follow the linked evidence for detail |
| [Analysis metrics](../outputs/v2_clean_min25/analysis/analysis_metrics.json) | Corpus size, assignments and cluster counts | Saved summary, not a fresh model fit |
| [Theme summary](../outputs/v2_clean_min25/analysis/candidate_theme_summary.csv) | Mapped counts and coverage | Nine-theme map covers 19.0% of the corpus |
| [Yearly-window shares](../outputs/v2_clean_min25/analysis/candidate_theme_window_prevalence.csv) | Theme counts with all-post and mapped-post denominators | Different denominator columns answer different questions |
| [Monthly coverage](../outputs/v2_clean_min25/analysis/monthly_assignment_coverage.csv) | Fraction assigned to a cluster by month | Outliers are a coverage limitation, not a theme |
| [Codebook](../planning/CANDIDATE_THEME_CODEBOOK.csv) | Included/excluded clusters and candidate themes | Review notes are not independent validation ratings |
| [Robustness](../planning/ROBUSTNESS.md) | Recorded audits and sensitivity results | Retain the limits of each check |

The [aggregate example](REPRODUCING.md) runs from these shared tables without underlying post text.

## Keep analysis streams distinct

**Exploratory topic analysis.** The [writing handoff](../planning/WRITING_HANDOFF.md), [findings](../planning/FINDINGS.md) and [collaborator brief](../planning/COLLABORATOR_BRIEF.md) describe the full-corpus model and smaller mapped subset. Preserve full-corpus, non-outlier and mapped-theme denominators. Statements about excluding sentiment describe the topic-paper scope in those notes.

**Separate whole-post sentiment check.** [SENTIMENT.md](../planning/SENTIMENT.md) documents the pinned model, text handling and limits. It estimates whole-post polarity, not sentiment specifically about management. It supplies neither human labels nor a new topic-model scope. The [sentiment outputs](../outputs/sentiment/twitter_roberta_base_sentiment_latest/) belong to this separate stream.

**Dated research documents.** The [deliverables](../deliverables/) retain their own dates and scope. This cleanup does not promote a draft to a final manuscript, add publication approval or establish completion of proposed validation.

## Read historical planning in context

- [DATA.md](../planning/DATA.md) inventories the original 6,132-row title-only input, not the later 97,254-post title-and-body corpus.
- [PROJECT.md](../planning/PROJECT.md) records plans, decisions and deferred alternatives. Plans are not proof of execution; use saved outputs and robustness notes for what actually ran.
- [WINDOWS.md](../planning/WINDOWS.md), [PREPROCESSING.md](../planning/PREPROCESSING.md) and [SCRAPING.md](../planning/SCRAPING.md) describe source preparation and time-window choices.
- [NEXT_STEPS.md](../planning/NEXT_STEPS.md) and the [email draft](../planning/COLLABORATOR_EMAIL_DRAFT.md) are planning/communication artifacts, not evidence that actions occurred or a message was sent.

The original notes are preserved. Earlier topic-only draft scope and a later separate sentiment check should be read by stage, not reconciled by deleting the earlier record.

## Local-only and historical references

Some notes name raw corpus files, embeddings, document-level assignments, sampled review posts or intermediate figures. Raw/per-post data are intentionally excluded, so the public repository cannot run every historical validation command by itself.

Use the [aggregate reproduction path](REPRODUCING.md) for a portable example and the [shared figures directory](../outputs/v2_clean_min25/figures/) for available images. A historical reference such as `monthly_anchor_topic_prevalence.png` is not a current shared deliverable. The [candidate-theme monthly figure](../outputs/v2_clean_min25/figures/candidate_theme_monthly_prevalence.png) and [coverage figure](../outputs/v2_clean_min25/figures/monthly_assignment_coverage.png) are available directly.
