from datetime import datetime
from unittest.mock import patch, PropertyMock

from cuser.models import CUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import ManagerUser
from users.tests.factories.user_factory import UserFactory
from users.tests.factories.user_manager_factory import ManagerUserFactory
from users.utils import is_manager, is_hitman


class TestUserViews(APITestCase):
    def setUp(self) -> None:
        self.create_users_url = reverse("users-list")
        self.get_users_url = reverse("users-list")
        self.update_users_url = reverse("users-list")
        self.boss = UserFactory(is_staff=True, is_superuser=True, email="boss@mail.com")
        self.manager = UserFactory(email="manager@mail.com")
        self.manager2 = UserFactory(email="manager2@mail.com")
        self.hitman = UserFactory(email="hitman@mail.com")
        self.hitman2 = UserFactory(email="hitman2@mail.com")
        self.manager_user = ManagerUserFactory(manager=self.manager, user=self.hitman)
        self.manager2_user2 = ManagerUserFactory(
            manager=self.manager2, user=self.hitman2
        )
        self.base_create_payload = {
            "first_name": "John",
            "last_name": "Lemon",
            "email": "test@mail.com",
            "password": "secret1992",
        }

    def test_it_creates_a_user_correctly(self):
        response = self.client.post(self.create_users_url, self.base_create_payload)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json()["email"], self.base_create_payload["email"])

    def test_it_gets_a_bad_request_response_creating_user_with_invalid_password(self):
        self.base_create_payload["password"] = "secret"
        response = self.client.post(self.create_users_url, self.base_create_payload)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_it_gets_a_bad_request_responsecreating_user_with_not_invalid_email(self):
        self.base_create_payload["email"] = "not-an-email.com"
        response = self.client.post(self.create_users_url, self.base_create_payload)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_it_gets_a_user_profile_correctly(self):
        url = reverse("users-profile")
        self.client.force_authenticate(self.hitman)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_it_gets_an_exception_trying_to_get_a_user_profile_without_a_role_assigned(
        self,
    ):
        url = reverse("users-profile")
        user = UserFactory(email="no-role-user@mail.com")
        self.client.force_authenticate(user)
        with self.assertRaises(Exception):
            try:
                response = self.client.get(url)
                self.assertEquals(
                    response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                self.assertEquals(e.value, "INVALID_USER_PROFILE")

    def test_given_a_hitman_user_then_can_not_view_hitmen_list(self):
        self.client.force_authenticate(self.hitman)
        response = self.client.get(self.get_users_url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("cuser.models.CUser.date_joined", new_callable=PropertyMock)
    def test_given_a_manager_then_can_only_view_his_managed_users(
        self, mocked_date_joined
    ):
        fixed_datetime = datetime.now()
        mocked_date_joined.return_value = fixed_datetime
        self.client.force_authenticate(self.manager)
        response = self.client.get(self.get_users_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), 1)
        self.assertListEqual(
            response.json(),
            [
                {
                    "id": self.hitman.id,
                    "first_name": "",
                    "last_name": "",
                    "groups": [1],
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "email": "hitman@mail.com",
                    "date_joined": fixed_datetime.isoformat() + "Z",
                    "last_login": None,
                    "managed_users": [],
                    "roles": [{"name": "hitman"}],
                }
            ],
        )

    def test_given_a_manager_then_cant_view_other_manager_users(self):
        self.client.force_authenticate(self.manager)
        response = self.client.get(self.get_users_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            len(response.json()),
            len(ManagerUser.objects.filter(manager=self.manager).all()),
        )

    def test_given_a_boss_user_then_can_view_all_the_users(self):
        self.client.force_authenticate(self.boss)
        response = self.client.get(self.get_users_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), 5)
        self.assertEquals(len(response.json()), len(CUser.objects.all()))

    def test_given_a_boss_then_can_promote_a_hitman_to_manager_adding_managed_users_to_end_hitman(
        self,
    ):
        update_url = reverse("users-detail", args=[str(self.hitman.id)])
        self.client.force_authenticate(self.boss)
        payload = {
            "is_active": True,
            "managed_users": [{"id": self.hitman2.id}],
        }
        response = self.client.put(update_url, payload)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.hitman2.refresh_from_db()
        self.assertTrue(is_manager(self.hitman))
        self.assertTrue(not is_hitman(self.hitman))

    def test_given_a_boss_can_convert_a_manager_to_end_hitman_removing_all_his_managed_hitmen(
        self,
    ):
        update_url = reverse("users-detail", args=[str(self.manager.id)])
        self.client.force_authenticate(self.boss)
        payload = {"is_active": True, "managed_users": []}
        response = self.client.put(update_url, payload)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.hitman2.refresh_from_db()
        self.assertTrue(not is_manager(self.manager))
        self.assertTrue(is_hitman(self.manager))

    def test_it_can_update_managed_users_list_if_one_of_the_users_in_the_list_is_manager_or_boss(
        self,
    ):
        pass  # TODO: implement this logic and complete this test case
