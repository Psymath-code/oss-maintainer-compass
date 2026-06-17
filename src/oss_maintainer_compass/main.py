#!/usr/bin/env python3
"""Command-line interface for oss-maintainer-compass."""

import argparse
import sys
from pathlib import Path

from .analyzer import IssueAnalyzer
from .reporter import Reporter
from . import __version__


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="oss-maintainer-compass",
        description="Lightweight CLI tool for open source maintainer workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze-export issues.json
  %(prog)s generate-report issues.json --output report.md
  %(prog)s find-stale issues.json --days 30
  %(prog)s agent-handoff issues.json --output handoff.md
  %(prog)s full-report issues.json --output maintainer_report.md
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # analyze-export
    analyze_parser = subparsers.add_parser(
        "analyze-export",
        help="Analyze GitHub issues/PRs JSON export"
    )
    analyze_parser.add_argument("json_file", help="Path to GitHub export JSON")
    analyze_parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Days without update to consider stale (default: 30)"
    )

    # find-stale
    stale_parser = subparsers.add_parser(
        "find-stale",
        help="Find stale issues and PRs"
    )
    stale_parser.add_argument("json_file", help="Path to GitHub export JSON")
    stale_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Days without update to consider stale (default: 30)"
    )

    # generate-report
    report_parser = subparsers.add_parser(
        "generate-report",
        help="Generate maintainer summary report"
    )
    report_parser.add_argument("json_file", help="Path to GitHub export JSON")
    report_parser.add_argument(
        "--output",
        "-o",
        help="Output file path (prints to stdout if not specified)"
    )
    report_parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Days without update to consider stale (default: 30)"
    )

    # agent-handoff
    handoff_parser = subparsers.add_parser(
        "agent-handoff",
        help="Generate AI agent handoff section"
    )
    handoff_parser.add_argument("json_file", help="Path to GitHub export JSON")
    handoff_parser.add_argument(
        "--output",
        "-o",
        help="Output file path (prints to stdout if not specified)"
    )
    handoff_parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Days without update to consider stale (default: 30)"
    )

    # full-report
    full_parser = subparsers.add_parser(
        "full-report",
        help="Generate complete report with all sections"
    )
    full_parser.add_argument("json_file", help="Path to GitHub export JSON")
    full_parser.add_argument(
        "--output",
        "-o",
        help="Output file path (prints to stdout if not specified)"
    )
    full_parser.add_argument(
        "--stale-days",
        type=int,
        default=30,
        help="Days without update to consider stale (default: 30)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        json_file = Path(args.json_file)
        analyzer = IssueAnalyzer(
            stale_days=getattr(args, 'stale_days', getattr(args, 'days', 30))
        )
        analyzer.load_from_json(json_file)

        if args.command == "analyze-export":
            return _cmd_analyze_export(analyzer)
        elif args.command == "find-stale":
            return _cmd_find_stale(analyzer)
        elif args.command == "generate-report":
            return _cmd_generate_report(analyzer, args.output)
        elif args.command == "agent-handoff":
            return _cmd_agent_handoff(analyzer, args.output)
        elif args.command == "full-report":
            return _cmd_full_report(analyzer, args.output)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

    return 0


def _cmd_analyze_export(analyzer: IssueAnalyzer) -> int:
    """Handle analyze-export command."""
    summary = analyzer.get_summary()
    print("\n📊 Backlog Summary")
    print(f"  Total items: {summary['total_items']}")
    print(f"  Issues: {summary['total_issues']} ({summary['open_issues']} open)")
    print(f"  PRs: {summary['total_prs']} ({summary['open_prs']} open)")
    print(f"  Stale (>{analyzer.stale_days}d): {summary['stale_items']}")
    print(f"  New (<{analyzer.new_days}d): {summary['new_items']}")
    print("\n🏷️ Top Labels")
    for label, count in summary['top_labels'].items():
        print(f"  {label}: {count}")
    return 0


def _cmd_find_stale(analyzer: IssueAnalyzer) -> int:
    """Handle find-stale command."""
    stale = analyzer.get_stale_items()
    if not stale:
        print(f"✅ No stale items found (threshold: >{analyzer.stale_days}d)")
        return 0

    print(f"\n⏰ Found {len(stale)} stale item(s):")
    for item in stale:
        item_type = "PR" if item.item_type.value == "pull_request" else "Issue"
        print(f"  [{item_type}] #{item.number}: {item.title}")
        print(f"    Last updated: {item.days_since_update} days ago")
    return 0


def _cmd_generate_report(analyzer: IssueAnalyzer, output_path: str = None) -> int:
    """Handle generate-report command."""
    reporter = Reporter(analyzer)
    report = reporter.generate_summary_report()
    if output_path:
        reporter.save_report(report, output_path)
    else:
        print(report)
    return 0


def _cmd_agent_handoff(analyzer: IssueAnalyzer, output_path: str = None) -> int:
    """Handle agent-handoff command."""
    reporter = Reporter(analyzer)
    handoff = reporter.generate_agent_handoff()
    if output_path:
        reporter.save_report(handoff, output_path)
    else:
        print(handoff)
    return 0


def _cmd_full_report(analyzer: IssueAnalyzer, output_path: str = None) -> int:
    """Handle full-report command."""
    reporter = Reporter(analyzer)
    report = reporter.generate_full_report()
    if output_path:
        reporter.save_report(report, output_path)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
