"""Tests for test_models module."""

import unittest
from datetime import datetime, timedelta
from src.oss_maintainer_compass.models import GitHubItem, ItemType, ItemState, Label, User


class TestModels(unittest.TestCase):
    """Test data models."""

    def test_label_creation(self):
        """Test Label creation."""
        label = Label(name="bug", description="Something isn't working")
        self.assertEqual(label.name, "bug")
        self.assertIsNotNone(label.description)

    def test_user_creation(self):
        """Test User creation."""
        user = User(login="alice")
        self.assertEqual(user.login, "alice")

    def test_github_item_creation(self):
        """Test GitHubItem creation."""
        now = datetime.now()
        item = GitHubItem(
            number=42,
            title="Test issue",
            state=ItemState.OPEN,
            item_type=ItemType.ISSUE,
            created_at=now,
            updated_at=now,
        )
        self.assertEqual(item.number, 42)
        self.assertEqual(item.state, ItemState.OPEN)
        self.assertEqual(item.item_type, ItemType.ISSUE)


if __name__ == "__main__":
    unittest.main()
