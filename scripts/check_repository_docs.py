"""Check local links in the entry README and new guides."""
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'README.md',ROOT/'docs/READING_GUIDE.md',ROOT/'docs/REPRODUCING.md']
errors=[]
for path in files:
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if target.startswith(('https://','http://','#','mailto:')):
            continue
        target=target.split('#',1)[0]
        if target and not (path.parent/target).exists():
            errors.append(f'{path.relative_to(ROOT)}: {target}')
if errors:raise SystemExit('\n'.join(errors))
print('Entry documentation local links and image paths resolve.')
