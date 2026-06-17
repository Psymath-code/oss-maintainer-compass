"""Tests for reporter module."""

import unittest
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import json
from pathlib import Path

from src.oss_maintainer_compass.analyzer import IssueAnalyzer
from src.oss_maintainer_compass.reporter import Reporter
from src.oss_maintainer_compass.models import ItemType


class TestReporter(unittest.TestCase):
    """Test Reporter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = IssueAnalyzer(stale_days=30, new_days=7)
        self.reporter = Reporter(self.analyzer)
        self.now = datetime.now()

    def _create_test_json(self, items_data):
        """Helper to create temporary JSON file with test data."""
        with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(items_data, f)
            return f.name

    def _sample_issue(self, number=1, title="Test", state="open", days_ago=5):
        """Helper to create sample issue data."""
        now = datetime.now()
        created = (now - timedelta(days=days_ago + 10)).isoformat() + "Z"
        updated = (now - timedelta(days=days_ago)).isoformat() + "Z"
        return {
            "number": number,
            "title": title,
            "state": state,
            "created_at": created,
            "updated_at": updated,
            "closed_at": None,
            "html_url": f"https://github.com/test/repo/issues/{number}",
            "body": "Test body",
            "user": {"login": "testuser"},
            "labels": [{"name": "bug"}],
            "comments": 0,
            "reactions": {},
        }

    def test_generate_summary_report(self):
        """Test summary report generation."""
        json_path = self._create_test_json([self._sample_issue(1)])
        try:
            self.analyzer.load_from_json(json_path)
            report = self.reporter.generate_summary_report()
            self.assertIn("Maintainer Backlog Report", report)
            self.assertIn("Overview", report)
            self.assertIn("Top Labels", report)
        finally:
            Path(json_path).unlink()

    def test_generate_pr_review_queue(self):
        """Test PR review queue generation."""
        json_path = self._create_test_json([])
        try:
            self.analyzer.load_from_json(json_path)
            report = self.reporter.generate_pr_review_queue()
            self.assertIn("PRs Needing Review", report)
        finally:
            Path(json_path).unlink()

    def test_generate_stale_items_report(self):
        """Test stale items report generation."""
        json_path = self._create_test_json([])
        try:
            self.analyzer.load_from_json(json_path)
            report = self.reporter.generate_stale_items_report()
            self.assertIn("Stale Items", report)
        finally:
            Path(json_path).unlink()

    def test_generate_agent_handoff(self):
        """Test agent handoff generation."""
        json_path = self._create_test_json([self._sample_issue(1)])
        try:
            self.analyzer.load_from_json(json_path)
            handoff = self.reporter.generate_agent_handoff()
            self.assertIn("AI Agent Handoff", handoff)
            self.assertIn("Current State", handoff)
            self.assertIn("Priority Actions", handoff)
        finally:
            Path(json_path).unlink()

    def test_generate_full_report(self):
        """Test full report generation."""
        json_path = self._create_test_json([self._sample_issue(1)])
        try:
            self.analyzer.load_from_json(json_path)
            report = self.reporter.generate_full_report()
            self.assertIn("Maintainer Backlog Report", report)
            self.assertIn("PRs Needing Review", report)
            self.assertIn("Stale Items", report)
            self.assertIn("AI Agent Handoff", report)
        finally:
            Path(json_path).unlink()

    def test_save_report(self):
        """Test saving report to file."""
        json_path = self._create_test_json([self._sample_issue(1)])
        output_path = None
        try:
            self.analyzer.load_from_json(json_path)
            report = self.reporter.generate_summary_report()
            with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                output_path = f.name
            self.reporter.save_report(report, output_path)
            self.assertTrue(Path(output_path).exists())
            with open(output_path, 'r') as f:
                content = f.read()
                self.assertIn("Maintainer Backlog Report", content)
        finally:
            if Path(json_path).exists():
                Path(json_path).unlink()
            if output_path and Path(output_path).exists():
                Path(output_path).unlink()


if __name__ == "__main__":
    unittest.main()
