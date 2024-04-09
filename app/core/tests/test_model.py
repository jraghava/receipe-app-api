"""
Tests for Models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_success(self):
        """Test creating a user with an email is successful """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@example.COM', 'TEST3@example.com'],
            ['test4@EXAMPLE.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test new user without email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_new_user_as_none_email_raises_error(self):
        """Test new user as none email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'sample123')

    def test_create_superuser(self):
        """Test creating a Super user."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test create new recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.'
        )

        self.assertEqual(str(recipe), recipe.title)
