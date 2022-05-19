from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Note
from blog_api import filters


class TestNoteFilter(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User(
            username="test_user1",
            password="qwerty1"
        )
        test_user_2 = User(
            username="test_user2",
            password="qwerty2"
        )

        test_user_1, test_user_2 = User.objects.bulk_create([test_user_1, test_user_2])

        Note.objects.create(title="Test_1", author=test_user_1)
        Note.objects.create(title="Test_2", author=test_user_2)

    def test_filter_by_author_id(self):
        filter_author = 1
        queryset = Note.objects.all()
        expected_queryset = \
            Note.objects.filter(author_id=filter_author)

        actual_queryset = filters.filter_by_author_id(
            queryset,
            filter_author
        )

        self.assertQuerysetEqual(actual_queryset, expected_queryset)

        # queryset.filter(author__username='test_user2') - фильтр по имени автора


