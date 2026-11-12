"""Consistency checks on shared evidence; no raw corpus or NLP dependencies."""
import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_public_aggregates import ANALYSIS, validate


class AggregateChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        for relative in [ANALYSIS/'analysis_metrics.json',ANALYSIS/'candidate_theme_summary.csv',
                         ANALYSIS/'candidate_theme_window_prevalence.csv',ANALYSIS/'monthly_assignment_coverage.csv',
                         Path('planning/CANDIDATE_THEME_CODEBOOK.csv')]:
            p=self.root/relative;p.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/relative,p)
        self.path=self.root/ANALYSIS/'candidate_theme_window_prevalence.csv'

    def tearDown(self):
        self.temp.cleanup()

    def rewrite(self,change):
        with self.path.open(newline='',encoding='utf-8') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        change(rows)
        with self.path.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

    def test_shared_evidence_reconciles(self):
        result=validate(self.root)
        self.assertEqual(result['mapped_posts'],18506)
        self.assertEqual(result['candidate_themes'],9)
        self.assertEqual(len(result['windows']),4)

    def test_zero_denominator_rejected(self):
        self.rewrite(lambda rows:rows[0].update(total_posts='0'))
        with self.assertRaisesRegex(ValueError,'denominator'):validate(self.root)

    def test_duplicate_window_theme_rejected(self):
        self.rewrite(lambda rows:rows.append(dict(rows[0])))
        with self.assertRaisesRegex(ValueError,'Duplicate'):validate(self.root)

    def test_missing_theme_rejected(self):
        self.rewrite(lambda rows:rows.pop())
        with self.assertRaisesRegex(ValueError,'missing themes'):validate(self.root)

    def test_wrong_share_rejected(self):
        self.rewrite(lambda rows:rows[0].update(share_all_posts='0.9'))
        with self.assertRaisesRegex(ValueError,'share disagrees'):validate(self.root)

    def test_non_finite_share_rejected(self):
        self.rewrite(lambda rows:rows[0].update(share_all_posts='nan'))
        with self.assertRaisesRegex(ValueError,'Non-finite'):validate(self.root)


if __name__=='__main__':unittest.main()
