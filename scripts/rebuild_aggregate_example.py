"""Rebuild a small comparison figure from committed aggregate CSVs only.

Requires matplotlib; does not import the NLP pipeline or read any post text.
The output is an example view of existing results, not a new fitted analysis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import textwrap

from validate_public_aggregates import ROOT, ANALYSIS, table, validate


def build(output_dir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator, PercentFormatter

    checked = validate()
    source = ROOT / ANALYSIS / 'candidate_theme_window_prevalence.csv'
    rows = table(source)
    first, last = checked['windows'][0], checked['windows'][-1]
    themes = [r['candidate_theme'] for r in rows if r['rolling_window'] == first]
    by_key = {(r['rolling_window'], r['candidate_theme']): r for r in rows}
    themes.sort(key=lambda t: float(by_key[(last, t)]['share_all_posts']), reverse=True)
    a = [float(by_key[(first, t)]['share_all_posts']) for t in themes]
    b = [float(by_key[(last, t)]['share_all_posts']) for t in themes]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'aggregate-example',
                         'axes.titlelocation': 'left'})
    fig, ax = plt.subplots(figsize=(12, 7.6))
    fig.subplots_adjust(left=.35, right=.96, top=.81, bottom=.17)
    y = list(range(len(themes)))
    ax.barh([v-.18 for v in y], a, height=.31, color='#30566D', label='Y1 · Mar 2021–Feb 2022')
    ax.barh([v+.18 for v in y], b, height=.31, color='#9FC6AE', edgecolor='#527763', linewidth=.5,
            label='Y4 · Mar 2024–Feb 2025')
    ax.set_yticks(y, [textwrap.fill(t, 34) for t in themes])
    ax.invert_yaxis()
    ax.set_xlim(0, .06)
    ax.xaxis.set_major_locator(MultipleLocator(.01))
    ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_xlabel('Share of all filtered posts in the same yearly window', labelpad=10)
    ax.set_axisbelow(True)
    ax.grid(axis='x', color='#e0e5e2', linewidth=.7)
    for spine in ['top','right','left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#9daaa1')
    ax.tick_params(axis='y', length=0, pad=10)
    for i, (va, vb) in enumerate(zip(a, b)):
        ax.text(va+.0007, i-.18, f'{va:.2%}', va='center', fontsize=9)
        ax.text(vb+.0007, i+.18, f'{vb:.2%}', va='center', fontsize=9)
    fig.text(.04,.955,'Candidate themes in management-related Reddit discussion', fontsize=16, weight='bold')
    fig.text(.04,.915,'First and last yearly windows · descriptive comparison from the saved exploratory analysis',fontsize=10,color='#4a5950')
    ax.legend(loc='lower left',bbox_to_anchor=(0,1.02),frameon=False,ncol=2,fontsize=9)
    fig.text(.04,.065,'The nine-theme map covers 19.0% of the full corpus. Bars count only posts assigned to included clusters;\n'
             'they do not estimate the complete prevalence of each concern. No causal or human-validation claim.',fontsize=9,color='#4a5950')
    output_dir.mkdir(parents=True, exist_ok=True)
    for ext in ['png','svg']:
        path=output_dir/f'aggregate_theme_comparison.{ext}'
        fig.savefig(path,dpi=170,facecolor='white',metadata={'Date':None} if ext=='svg' else None)
        if ext=='svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)
    report={'scope':'Rebuilt view of existing aggregate results; no raw text or model execution.',
            'source':source.relative_to(ROOT).as_posix(),
            'source_sha256':hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
            'source_hash_normalization':'UTF-8 text with LF newlines',
            'windows':[first,last], 'validated_summaries':checked,
            'displayed_values':[{'candidate_theme':t,'first_share':va,'last_share':vb} for t,va,vb in zip(themes,a,b)]}
    (output_dir/'aggregate_example_summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Rebuilt PNG, SVG and summary from the committed aggregate CSV.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,default=ROOT/'examples/output')
    build(p.parse_args().output_dir)
