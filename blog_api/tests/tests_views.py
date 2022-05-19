from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

from blog.models import Note
from django.contrib.auth.models import User


class TestPublicNoteListAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test@test.ru")

    def test_empty_list_note(self):
        path = "/notes/public/"
        resp = self.client.get(path)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )
        data = resp.data
        self.assertEqual(data, [])

    def test_get_public_notes(self):
        test_user = User.objects.create(
            username="test_user",
            password="qwerty"
        )
        Note.objects.create(
            title="Test_1",
            author=test_user,
            public=True
        )
        Note.objects.create(
            title="Test_2",
            author=test_user,
            public=False
        )

        path = "/notes/public/"
        resp = self.client.get(path)

        self.assertEqual(
            resp.status_code, status.HTTP_200_OK
        )
        data = resp.data
        expected_count_public_note = 1

        self.assertEqual(
            len(data), expected_count_public_note
        )

        for note in data:
            self.assertTrue(note["public"])
