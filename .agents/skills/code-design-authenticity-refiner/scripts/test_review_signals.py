#!/usr/bin/env python3
"""Synthetic test fixtures for scanner safety and behavior (not model evaluations)."""
import tempfile
from pathlib import Path
import unittest
from review_signals import scan

class ScannerTests(unittest.TestCase):
    def test_find_known_signals(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'demo.jsx').write_text("<a href=\"#\">Click</a>\\n// TODO: implement\\n<h1>Lorem ipsum</h1>", encoding='utf-8')
            findings = scan(root)['findings']
            self.assertEqual({x['rule'] for x in findings}, {'dummy-link','stub-implementation','placeholder-copy'})

    def test_skip_dependencies(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'node_modules').mkdir()
            (root/'node_modules'/'test.js').write_text('href="#"', encoding='utf-8')
            self.assertFalse(scan(root)['findings'])

    def test_no_modifications(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root/'file.html'
            before = '<a href="#">test</a>'
            path.write_text(before, encoding='utf-8')
            scan(root)
            self.assertEqual(path.read_text(encoding='utf-8'), before)

    def test_no_content_in_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'file.html').write_text('<!-- TODO: secret=private-example -->', encoding='utf-8')
            result = str(scan(root))
            self.assertNotIn('secret=private-example', result)

    def test_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'file.html').write_text('TODO: x\n'*30, encoding='utf-8')
            result = scan(root, limit=2)
            self.assertTrue(result['truncated'])
            self.assertEqual(len(result['findings']), 2)

if __name__ == '__main__': unittest.main()
