"""Tests for models module."""

import unittest
from datetime import datetime, timedelta
from src.oss_maintainer_compass.models import GitHubItem, ItemType, ItemState, Label, User


class TestLabel(unittest.TestCase):
    """Test Label model."""

    def test_label_equality(self):
        label1 = Label(name="bug")
        label2 = Label(name="bug", description="Something isn't working")
        self.assertEqual(label1, label2)  # Equality based on name only

    def test_label_hash(self):
        label1 = Label(name="bug")
        label2 = Label(name="bug")
        # Should be hashable and equal labels have same hash
        self.assertEqual(hash(label1), hash(label2))

    def test_label_set_deduplication(self):
        labels = [Label(name="bug"), Label(name="bug", description="test")]
        unique = set(labels)
        self.assertEqual(len(unique), 1)


class TestUser(unittest.TestCase):
    """Test User model."""

    def test_user_equality(self):
        user1 = User(login="alice")
        user2 = User(login="alice", html_url="https://github.com/alice")
        self.assertEqual(user1, user2)  # Equality based on login only

    def test_user_hash(self):
        user1 = User(login="alice")
        user2 = User(login="alice")
        self.assertEqual(hash(user1), hash(user2))


class TestGitHubItem(unittest.TestCase):
    """Test GitHubItem model."""

    def setUp(self):
        """Set up test fixtures."""
        self.now = datetime.now()
        self.item = GitHubItem(
            number=42,
            title="Test issue",
            state=ItemState.OPEN,
            item_type=ItemType.ISSUE,
            created_at=self.now - timedelta(days=10),
            updated_at=self.now - timedelta(days=5),
            html_url="https://github.com/test/repo/issues/42",
            body="Test body",
        )

    def test_days_since_update(self):
        """Test days_since_update calculation."""
        # Should be approximately 5 days
        self.assertGreaterEqual(self.item.days_since_update, 4)
        self.assertLessEqual(self.item.days_since_update, 6)

    def test_days_since_creation(self):
        """Test days_since_creation calculation."""
        # Should be approximately 10 days
        self.assertGreaterEqual(self.item.days_since_creation, 9)
        self.assertLessEqual(self.item.days_since_creation, 11)

    def test_is_stale_true(self):
        """Test is_stale returns True for stale items."""
        self.assertTrue(self.item.is_stale(days_threshold=3))

    def test_is_stale_false(self):
        """Test is_stale returns False for fresh items."""
        self.assertFalse(self.item.is_stale(days_threshold=10))

    def test_is_new_true(self):
        """Test is_new returns True for new items."""
        new_item = GitHubItem(
            number=43,
            title="New issue",
            state=ItemState.OPEN,
            item_type=ItemType.ISSUE,
            created_at=self.now - timedelta(days=3),
            updated_at=self.now - timedelta(days=1),
        )
        self.assertTrue(new_item.is_new(days_threshold=5))

    def test_is_new_false(self):
        """Test is_new returns False for old items."""
        self.assertFalse(self.item.is_new(days_threshold=5))

    def test_label_names(self):
        """Test label_names property."""
        item = GitHubItem(
            number=44,
            title="Test",
            state=ItemState.OPEN,
            item_type=ItemType.ISSUE,
            created_at=self.now,
            updated_at=self.now,
            labels=[Label(name="bug"), Label(name="urgent")],
        )
        self.assertEqual(item.label_names, ["bug", "urgent"])


if __name__ == "__main__":
    unittest.main()
