"""Report generation for maintainer analysis."""

from datetime import datetime
from typing import List, Dict, Optional

from .models import GitHubItem, ItemType
from .analyzer import IssueAnalyzer


class Reporter:
    """Generates Markdown reports from analysis."""

    def __init__(self, analyzer: IssueAnalyzer):
        """Initialize reporter with analyzer.

        Args:
            analyzer: IssueAnalyzer instance with loaded data
        """
        self.analyzer = analyzer

    def generate_summary_report(self) -> str:
        """Generate executive summary report."""
        summary = self.analyzer.get_summary()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')

        report = f"""# Maintainer Backlog Report

**Generated:** {timestamp}

## 📊 Overview

| Metric | Count |
|--------|-------|
| Total Issues | {summary['total_issues']} |
| Total PRs | {summary['total_prs']} |
| Open Issues | {summary['open_issues']} |
| Open PRs | {summary['open_prs']} |
| Stale Items (>{self.analyzer.stale_days}d) | {summary['stale_items']} |
| New Items (<{self.analyzer.new_days}d) | {summary['new_items']} |

## 🏷️ Top Labels

"""
        for label, count in summary['top_labels'].items():
            report += f"- **{label}** ({count} items)\n"

        return report

    def generate_pr_review_queue(self) -> str:
        """Generate PRs needing review report."""
        prs = self.analyzer.get_prs_needing_review()

        if not prs:
            return "## 📋 PRs Needing Review\n\nNo open PRs found.\n"

        report = "## 📋 PRs Needing Review\n\n"
        report += f"Found {len(prs)} open PR(s):\n\n"

        for pr in prs[:20]:  # Show top 20
            days_since = pr.days_since_update
            report += f"- [#{pr.number}]({pr.html_url}) {pr.title}\n"
            report += f"  - Last updated: {days_since} days ago\n"
            if pr.author:
                report += f"  - Author: {pr.author.login}\n"
            if pr.comments:
                report += f"  - Comments: {pr.comments}\n"
            report += "\n"

        if len(prs) > 20:
            report += f"... and {len(prs) - 20} more.\n"

        return report

    def generate_stale_items_report(self) -> str:
        """Generate stale items report."""
        stale = self.analyzer.get_stale_items()

        if not stale:
            return f"## ⏰ Stale Items (>{self.analyzer.stale_days}d)\n\nNo stale items found.\n"

        report = f"## ⏰ Stale Items (>{self.analyzer.stale_days} days)\n\n"
        report += f"Found {len(stale)} stale item(s):\n\n"

        # Separate by type
        stale_issues = [i for i in stale if i.item_type == ItemType.ISSUE]
        stale_prs = [i for i in stale if i.item_type == ItemType.PULL_REQUEST]

        if stale_issues:
            report += "### Stale Issues\n\n"
            for issue in stale_issues[:10]:
                report += f"- [#{issue.number}]({issue.html_url}) {issue.title}\n"
                report += f"  - Last updated: {issue.days_since_update} days ago\n"
                report += "\n"
            if len(stale_issues) > 10:
                report += f"... and {len(stale_issues) - 10} more issues.\n\n"

        if stale_prs:
            report += "### Stale PRs\n\n"
            for pr in stale_prs[:10]:
                report += f"- [#{pr.number}]({pr.html_url}) {pr.title}\n"
                report += f"  - Last updated: {pr.days_since_update} days ago\n"
                report += "\n"
            if len(stale_prs) > 10:
                report += f"... and {len(stale_prs) - 10} more PRs.\n\n"

        return report

    def generate_agent_handoff(self) -> str:
        """Generate structured handoff for AI agents (Codex, ChatGPT)."""
        summary = self.analyzer.get_summary()
        prs_needing_review = self.analyzer.get_prs_needing_review()
        stale = self.analyzer.get_stale_items()
        top_labels = dict(self.analyzer.get_top_labels(5))

        handoff = """## 🤖 AI Agent Handoff

Context for Codex / ChatGPT assisted maintenance workflows.

### Current State

```json
{
"""
        handoff += f'  "total_open_issues": {summary["open_issues"]},\n'
        handoff += f'  "total_open_prs": {summary["open_prs"]},\n'
        handoff += f'  "stale_items_count": {summary["stale_items"]},\n'
        handoff += f'  "new_items_count": {summary["new_items"]},\n'
        handoff += f'  "stale_days_threshold": {self.analyzer.stale_days}\n'
        handoff += "}\n```\n\n"

        handoff += "### Priority Actions\n\n"

        if prs_needing_review:
            handoff += f"1. **Review {len(prs_needing_review)} open PR(s)**\n"
            handoff += "   - Suggest focus on PRs waiting longest for review\n"

        if stale:
            handoff += f"2. **Address {len(stale)} stale item(s)**\n"
            handoff += "   - Consider if stale items should be:"
            handoff += " closed as wontfix, reopened for discussion, or reassigned\n"

        handoff += "\n### Suggested Next Steps\n\n"
        handoff += "1. Review and comment on oldest open PRs\n"
        handoff += "2. Triage stale issues for closure or reclassification\n"
        handoff += "3. Update documentation for commonly reported issues\n"
        handoff += "4. Reach out to maintainers/contributors about stuck items\n"

        handoff += "\n### Label Distribution\n\n"
        for label, count in sorted(top_labels.items(), key=lambda x: x[1], reverse=True):
            handoff += f"- `{label}`: {count} items\n"

        return handoff

    def generate_full_report(self) -> str:
        """Generate complete report with all sections."""
        report = self.generate_summary_report()
        report += "\n" + self.generate_pr_review_queue()
        report += "\n" + self.generate_stale_items_report()
        report += "\n" + self.generate_agent_handoff()
        return report

    def save_report(self, content: str, output_path: str) -> None:
        """Save report to file.

        Args:
            content: Markdown report content
            output_path: Path to save report
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Report saved to {output_path}")
