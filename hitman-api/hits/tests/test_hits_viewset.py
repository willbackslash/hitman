from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.tests.factories.user_factory import UserFactory


class TestHitViewset(APITestCase):
    def setUp(self) -> None:
        self.boss = UserFactory(
            is_staff=True, is_superuser=True, email="boss@hitman.com"
        )
        self.manager = UserFactory(email="manager@hitman.com")
        self.hitman = UserFactory(email="hitman@hitman.com")
        self.create_hits_url = reverse("hits-list")
        self.create_hit_base_payload = {
            "assigned_to": self.hitman.email,
            "target_name": "test name",
            "description": "fast and clean",
        }

    def test_given_a_hitman_user_then_cant_create_hits(self):
        self.client.force_authenticate(self.hitman)
        response = self.client.post(self.create_hits_url, self.create_hit_base_payload)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_given_a_hitman_user_then_can_view_only_hits_assigned_to_him(self):
        self.assertEquals(True, False)

    def test_given_a_hitman_user_then_can_mark_as_completed_his_own_hits(self):
        self.assertEquals(True, False)

    def test_given_a_hitman_user_then_can_mark_as_failed_his_own_hits(self):
        self.assertEquals(True, False)

    def test_given_a_hitman_user_then_can_not_change_the_status_of_another_hitman_hits(
        self,
    ):
        self.assertEquals(True, False)

    def test_given_a_hitman_user_then_cant_assign_hits(self):
        self.assertEquals(True, False)

    def test_given_a_manager_user_he_can_view_hits_from_him_and_from_his_lackeys(self):
        self.assertEquals(True, False)

    def test_given_a_manager_user_he_can_create_a_hit_for_any_of_his_lackeys(self):
        self.assertEquals(True, False)

    def test_given_a_manager_user_he_can_assign_a_hit_for_any_of_his_lackeys(self):
        self.assertEquals(True, False)

    def test_given_a_manager_then_cannot_assign_hits_to_himself(self):
        self.assertEquals(True, False)

    def test_given_a_boss_it_can_create_a_hit_for_any_hitman(self):
        self.client.force_authenticate(self.boss)
        response = self.client.post(self.create_hits_url, self.create_hit_base_payload)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_given_a_boss_it_can_create_a_hit_for_any_manager(self):
        self.assertEquals(True, False)

    def test_given_a_boss_it_can_view_all_the_hits(self):
        self.assertEquals(True, False)

    def test_given_a_boss_then_cannot_assign_hits_to_inactive_users(self):
        self.assertEquals(True, False)

    def test_given_a_manager_then_cannot_assign_hits_to_inactive_users(self):
        self.assertEquals(True, False)

    def test_given_a_boss_then_cannot_assign_hits_to_himself(self):
        self.assertEquals(True, False)
