"""Data models for representing GitHub issues and pull requests."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class ItemType(Enum):
    """GitHub item type."""
    ISSUE = "issue"
    PULL_REQUEST = "pull_request"


class ItemState(Enum):
    """GitHub item state."""
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class Label:
    """Represents a GitHub label."""
    name: str
    description: Optional[str] = None
    color: Optional[str] = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Label):
            return self.name == other.name
        return False


@dataclass
class User:
    """Represents a GitHub user."""
    login: str
    html_url: Optional[str] = None
    avatar_url: Optional[str] = None

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.login == other.login
        return False


@dataclass
class GitHubItem:
    """Represents a GitHub issue or pull request."""
    number: int
    title: str
    state: ItemState
    item_type: ItemType
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    html_url: str = ""
    body: str = ""
    author: Optional[User] = None
    labels: List[Label] = field(default_factory=list)
    comments: int = 0
    reactions: int = 0

    @property
    def days_since_update(self) -> int:
        """Calculate days since last update."""
        delta = datetime.now().replace(tzinfo=None) - self.updated_at.replace(tzinfo=None)
        return delta.days

    @property
    def days_since_creation(self) -> int:
        """Calculate days since creation."""
        delta = datetime.now().replace(tzinfo=None) - self.created_at.replace(tzinfo=None)
        return delta.days

    @property
    def label_names(self) -> List[str]:
        """Get list of label names."""
        return [label.name for label in self.labels]

    def is_stale(self, days_threshold: int = 30) -> bool:
        """Check if item hasn't been updated for the specified days."""
        return self.days_since_update >= days_threshold

    def is_new(self, days_threshold: int = 7) -> bool:
        """Check if item was created recently."""
        return self.days_since_creation <= days_threshold
