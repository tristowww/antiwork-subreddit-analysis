"""Check consistency of the shared summaries without raw text or model files.

This validates the published aggregate evidence, not the underlying model or
the substantive validity of candidate themes. It never rewrites source files.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path('outputs/v2_clean_min25/analysis')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def table(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def number(row, key):
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('Missing or invalid numeric field: ' + key) from exc
    require(math.isfinite(value), 'Non-finite value: ' + key)
    return value


def count(row, key):
    value = number(row, key)
    require(value >= 0 and value.is_integer(), 'Expected nonnegative integer: ' + key)
    return int(value)


def close(actual, expected, message):
    require(math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-8), message)


def validate(root=ROOT):
    base = root / ANALYSIS
    metrics = json.loads((base / 'analysis_metrics.json').read_text(encoding='utf-8'))
    summary = table(base / 'candidate_theme_summary.csv')
    windows = table(base / 'candidate_theme_window_prevalence.csv')
    months = table(base / 'monthly_assignment_coverage.csv')
    corpus = count(metrics, 'corpus_posts')
    assigned = count(metrics, 'assigned_posts')
    require(corpus > 0, 'Corpus denominator must be positive.')
    require(assigned + count(metrics, 'outlier_posts') == corpus, 'Assigned/outlier counts do not sum to corpus.')
    close(number(metrics, 'assigned_rate'), round(assigned / corpus, 6), 'Saved assigned rate disagrees with counts.')
    themes = [r['candidate_theme'] for r in summary]
    require(len(themes) == len(set(themes)) and len(themes) > 0, 'Duplicate or missing theme summaries.')
    mapped = sum(count(r, 'mapped_posts') for r in summary)
    require(0 < mapped <= assigned, 'Mapped count must be positive and no greater than assigned count.')
    for r in summary:
        close(number(r, 'share_all_posts'), count(r, 'mapped_posts') / corpus, 'Theme all-post share disagrees with count.')
        close(number(r, 'share_mapped_posts'), count(r, 'mapped_posts') / mapped, 'Theme mapped share disagrees with count.')
    grouped = {}
    keys = set()
    for r in windows:
        k = r['rolling_window'], r['candidate_theme']
        require(k not in keys, 'Duplicate window/theme row.')
        keys.add(k)
        require(r['candidate_theme'] in themes, 'Unknown candidate theme in window table.')
        total, n_mapped, n = count(r, 'total_posts'), count(r, 'mapped_posts'), count(r, 'post_count')
        require(total > 0 and n_mapped > 0 and n <= n_mapped <= total, 'Invalid window counts or denominator.')
        close(number(r, 'share_all_posts'), n / total, 'Window all-post share disagrees with count.')
        close(number(r, 'share_mapped_posts'), n / n_mapped, 'Window mapped share disagrees with count.')
        grouped.setdefault(r['rolling_window'], []).append(r)
    for key, rows in grouped.items():
        require({r['candidate_theme'] for r in rows} == set(themes), 'Window has missing themes: ' + key)
        require(len({r['total_posts'] for r in rows}) == 1, 'Inconsistent total denominator within window.')
        require(len({r['mapped_posts'] for r in rows}) == 1, 'Inconsistent mapped denominator within window.')
        require(sum(count(r, 'post_count') for r in rows) == count(rows[0], 'mapped_posts'), 'Window theme counts do not sum to mapped count.')
    require(sum(count(rows[0], 'total_posts') for rows in grouped.values()) == corpus, 'Window totals do not sum to corpus.')
    require(sum(count(rows[0], 'mapped_posts') for rows in grouped.values()) == mapped, 'Window mapped totals disagree with summary.')
    for theme in themes:
        require(sum(count(r, 'post_count') for r in windows if r['candidate_theme'] == theme) ==
                next(count(r, 'mapped_posts') for r in summary if r['candidate_theme'] == theme),
                'Window counts disagree with theme summary.')
    require(len(months) == len({r['month'] for r in months}) == count(metrics, 'months'), 'Missing or duplicate months.')
    for r in months:
        n, a, o = count(r, 'total_posts'), count(r, 'assigned_posts'), count(r, 'outlier_posts')
        require(n > 0 and a + o == n, 'Invalid monthly count/denominator.')
        close(number(r, 'assigned_rate'), a / n, 'Monthly assignment rate disagrees with count.')
        close(number(r, 'outlier_rate'), o / n, 'Monthly outlier rate disagrees with count.')
    require(sum(count(r, 'total_posts') for r in months) == corpus, 'Monthly totals disagree with corpus.')
    require(sum(count(r, 'assigned_posts') for r in months) == assigned, 'Monthly assigned counts disagree.')
    codebook = table(root / 'planning/CANDIDATE_THEME_CODEBOOK.csv')
    included = [r for r in codebook if r['decision'] == 'include']
    require(len(included) == sum(count(r, 'candidate_clusters') for r in summary), 'Codebook included-cluster count disagrees.')
    require({r['candidate_theme'] for r in included} == set(themes), 'Codebook themes disagree with summary.')
    return {'corpus_posts': corpus, 'assigned_posts': assigned, 'mapped_posts': mapped,
            'candidate_themes': len(themes), 'included_clusters': len(included),
            'windows': sorted(grouped), 'months': len(months),
            'mapped_share_all_posts': mapped / corpus,
            'mapped_share_assigned_posts': mapped / assigned}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    print(json.dumps(validate(parser.parse_args().root), indent=2))
