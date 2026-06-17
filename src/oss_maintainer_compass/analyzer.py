"""Analysis engine for GitHub issues and pull requests."""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

from .models import GitHubItem, ItemType, ItemState, Label, User


class IssueAnalyzer:
    """Analyzes GitHub issues and PR backlogs."""

    def __init__(self, stale_days: int = 30, new_days: int = 7):
        """Initialize analyzer.

        Args:
            stale_days: Number of days without update to consider stale
            new_days: Number of days since creation to consider new
        """
        self.stale_days = stale_days
        self.new_days = new_days
        self.items: List[GitHubItem] = []

    def load_from_json(self, json_path: Path) -> None:
        """Load issues/PRs from GitHub export JSON.

        Args:
            json_path: Path to JSON file

        Raises:
            FileNotFoundError: If file not found
            json.JSONDecodeError: If file is not valid JSON
        """
        json_path = Path(json_path)
        if not json_path.exists():
            raise FileNotFoundError(f"File not found: {json_path}")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSON root must be a list of items")

        self.items = []
        for item_data in data:
            item = self._parse_item(item_data)
            if item:
                self.items.append(item)

    def _parse_item(self, data: Dict) -> Optional[GitHubItem]:
        """Parse a single item from GitHub export.

        Args:
            data: Dictionary containing item data

        Returns:
            GitHubItem or None if parsing failed
        """
        try:
            # Determine item type
            item_type = ItemType.PULL_REQUEST if 'pull_request' in data else ItemType.ISSUE

            # Parse user
            author = None
            if data.get('user'):
                user_data = data['user']
                author = User(
                    login=user_data.get('login', ''),
                    html_url=user_data.get('html_url'),
                    avatar_url=user_data.get('avatar_url')
                )

            # Parse labels
            labels = []
            if data.get('labels'):
                for label_data in data['labels']:
                    if isinstance(label_data, dict):
                        labels.append(Label(
                            name=label_data.get('name', ''),
                            description=label_data.get('description'),
                            color=label_data.get('color')
                        ))
                    elif isinstance(label_data, str):
                        labels.append(Label(name=label_data))

            # Parse state
            state_str = data.get('state', 'open').lower()
            state = ItemState.OPEN if state_str == 'open' else ItemState.CLOSED

            # Parse dates
            created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            closed_at = None
            if data.get('closed_at'):
                closed_at = datetime.fromisoformat(data['closed_at'].replace('Z', '+00:00'))

            item = GitHubItem(
                number=data.get('number', 0),
                title=data.get('title', ''),
                state=state,
                item_type=item_type,
                created_at=created_at,
                updated_at=updated_at,
                closed_at=closed_at,
                html_url=data.get('html_url', ''),
                body=data.get('body', ''),
                author=author,
                labels=labels,
                comments=data.get('comments', 0),
                reactions=data.get('reactions', {}).get('total_count', 0)
                    if isinstance(data.get('reactions'), dict) else 0
            )
            return item
        except (KeyError, ValueError, TypeError) as e:
            print(f"Warning: Failed to parse item: {e}")
            return None

    def get_issues(self) -> List[GitHubItem]:
        """Get all issues (not PRs)."""
        return [item for item in self.items if item.item_type == ItemType.ISSUE]

    def get_pull_requests(self) -> List[GitHubItem]:
        """Get all pull requests."""
        return [item for item in self.items if item.item_type == ItemType.PULL_REQUEST]

    def get_open_items(self) -> List[GitHubItem]:
        """Get all open items."""
        return [item for item in self.items if item.state == ItemState.OPEN]

    def get_stale_items(self, days: Optional[int] = None) -> List[GitHubItem]:
        """Get items not updated for specified days.

        Args:
            days: Threshold in days (uses self.stale_days if not specified)
        """
        threshold = days if days is not None else self.stale_days
        return [item for item in self.get_open_items() if item.is_stale(threshold)]

    def get_new_items(self, days: Optional[int] = None) -> List[GitHubItem]:
        """Get recently created items.

        Args:
            days: Threshold in days (uses self.new_days if not specified)
        """
        threshold = days if days is not None else self.new_days
        return [item for item in self.get_open_items() if item.is_new(threshold)]

    def get_prs_needing_review(self) -> List[GitHubItem]:
        """Get PRs that are open and likely need review.

        Returns PRs without recent comments, sorted by age.
        """
        prs = self.get_pull_requests()
        open_prs = [pr for pr in prs if pr.state == ItemState.OPEN]
        # Sort by update time (oldest first - they've been waiting)
        return sorted(open_prs, key=lambda x: x.updated_at)

    def get_label_distribution(self, items: Optional[List[GitHubItem]] = None) -> Dict[str, int]:
        """Get count of items per label.

        Args:
            items: Specific items to analyze (uses all open if not specified)
        """
        target_items = items if items is not None else self.get_open_items()
        label_counts = Counter()
        for item in target_items:
            for label in item.labels:
                label_counts[label.name] += 1
        return dict(label_counts)

    def get_top_labels(self, n: int = 10, items: Optional[List[GitHubItem]] = None) -> List[Tuple[str, int]]:
        """Get top N most common labels.

        Args:
            n: Number of top labels to return
            items: Specific items to analyze (uses all open if not specified)
        """
        distribution = self.get_label_distribution(items)
        return sorted(distribution.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_items_by_label(self, label: str) -> List[GitHubItem]:
        """Get all open items with a specific label."""
        return [item for item in self.get_open_items() if label in item.label_names]

    def get_items_by_author(self, author_login: str) -> List[GitHubItem]:
        """Get all open items by a specific author."""
        return [item for item in self.get_open_items()
                if item.author and item.author.login == author_login]

    def get_author_stats(self) -> Dict[str, Dict]:
        """Get statistics by author.

        Returns dict with author login -> {count, issues, prs}
        """
        stats = defaultdict(lambda: {'count': 0, 'issues': 0, 'prs': 0})
        for item in self.get_open_items():
            if item.author:
                author_name = item.author.login
                stats[author_name]['count'] += 1
                if item.item_type == ItemType.ISSUE:
                    stats[author_name]['issues'] += 1
                else:
                    stats[author_name]['prs'] += 1
        return dict(stats)

    def get_summary(self) -> Dict:
        """Get overall backlog summary.

        Returns dict with key metrics.
        """
        issues = self.get_issues()
        prs = self.get_pull_requests()
        open_issues = [i for i in issues if i.state == ItemState.OPEN]
        open_prs = [p for p in prs if p.state == ItemState.OPEN]

        return {
            'total_items': len(self.items),
            'total_issues': len(issues),
            'total_prs': len(prs),
            'open_issues': len(open_issues),
            'open_prs': len(open_prs),
            'stale_items': len(self.get_stale_items()),
            'new_items': len(self.get_new_items()),
            'top_labels': dict(self.get_top_labels(5)),
        }
