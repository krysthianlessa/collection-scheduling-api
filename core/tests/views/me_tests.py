from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from core.views import MeView
from core.serializers import MeSerializer


class MeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.factory = APIRequestFactory()

    def test_me_view(self):
        view = MeView.as_view()
        request = self.factory.get("/me/")
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "username": self.user.username,
            "sector": "",
            "neighborhood": "",
            "full_name": self.user.get_full_name(),
        }
        self.assertEqual(response.data, expected_data)


class MeSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_get_sector_with_shared_calendar(self):
        serializer = MeSerializer(instance=self.user)
        shared_calendar = self.user.shared_calendar.create(
            identify="123456", is_active=True, sector="Sector A", neighborhood="Neighborhood X"
        )
        self.assertEqual(serializer.data["sector"], shared_calendar.sector)

    def test_get_sector_without_shared_calendar(self):
        serializer = MeSerializer(instance=self.user)
        self.assertEqual(serializer.data["sector"], "")

    def test_get_neighborhood_with_shared_calendar(self):
        serializer = MeSerializer(instance=self.user)
        shared_calendar = self.user.shared_calendar.create(
            identify="123456", is_active=True, sector="Sector A", neighborhood="Neighborhood X"
        )
        self.assertEqual(serializer.data["neighborhood"], shared_calendar.neighborhood)

    def test_get_neighborhood_without_shared_calendar(self):
        serializer = MeSerializer(instance=self.user)
        self.assertEqual(serializer.data["neighborhood"], "")

    def test_get_full_name(self):
        serializer = MeSerializer(instance=self.user)
        self.assertEqual(serializer.data["full_name"], self.user.get_full_name())
