from cuser.models import CUser, Group
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

    def test_it_gets_a_user_profile_correctly(self):
        url = reverse("users-profile")
        user = CUser(
            email="myemail@test.com", password="secret"
        )  # TODO: implement factories
        user.save()
        role = Group.objects.get(name="hitman")
        role.user_set.add(user)
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_gets_an_exception_trying_to_get_a_user_profile_without_a_role_assigned(
        self,
    ):
        url = reverse("users-profile")
        user = CUser(
            email="myemail@test.com", password="secret"
        )  # TODO: implement factories
        user.save()
        self.client.force_authenticate(user)
        with self.assertRaises(Exception):
            try:
                response = self.client.get(url)
                self.assertEquals(
                    response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                self.assertEquals(e.value, "INVALID_USER_PROFILE")
