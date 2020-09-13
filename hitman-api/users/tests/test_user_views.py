from cuser.models import CUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestUserViews(APITestCase):
    def setUp(self) -> None:
        self.create_users_url = reverse("users-list")

    def test_it_creates_a_user_correctly(self):
        user = CUser(
            email="myemail@test.com", password="secret"
        )  # TODO: implement factories
        user.save()
        self.client.force_authenticate(user)
        payload = {"email": "test@mail.com", "password": "secret"}
        response = self.client.post(self.create_users_url, payload)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json()["email"], payload["email"])
