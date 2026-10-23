import json
from pathlib import Path
import tempfile
import unittest

from compare import select_workloads


class InputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.harness = self.root / 'tools/gungraun'
        (self.harness / 'fixtures').mkdir(parents=True)
        (self.harness / 'fixtures/a.tsv').write_text('https://example.com/\thttps://example.com/\n')

    def test_default_and_filter(self):
        self.assertEqual(list(select_workloads(self.harness, '', 'a')), ['a'])
        with self.assertRaises(ValueError):
            select_workloads(self.harness, '', 'missing')

    def test_paths_and_duplicates(self):
        for paths in [[], ['../outside.tsv'], ['/tmp/a.tsv'],
                      ['tools/gungraun/fixtures/a.tsv'] * 2, ['missing.tsv']]:
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                select_workloads(self.harness, json.dumps(paths), '')

    def test_fixture_contract(self):
        for fixture in (Path(__file__).parent / 'fixtures').glob('*.tsv'):
            lines = fixture.read_text(encoding='utf-8').splitlines()
            self.assertTrue(lines)
            for line in lines:
                columns = line.split('\t')
                self.assertEqual(len(columns), 2)
                self.assertTrue(all(columns))
