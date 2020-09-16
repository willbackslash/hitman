from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from hits.models import Hit
from hits.tests.factories.hit_factory import HitFactory
from users.tests.factories.user_factory import UserFactory
from users.tests.factories.user_manager_factory import ManagerUserFactory


class TestHitViewset(APITestCase):
    def setUp(self) -> None:
        self.boss = UserFactory(is_staff=True, is_superuser=True, email="boss@mail.com")
        self.manager = UserFactory(email="manager@mail.com")
        self.manager2 = UserFactory(email="manager2@mail.com")
        self.hitman = UserFactory(email="hitman@mail.com")
        self.hitman2 = UserFactory(email="hitman2@mail.com")
        self.manager_user = ManagerUserFactory(manager=self.manager, user=self.hitman)
        self.create_hits_url = reverse("hits-list")
        self.create_hit_base_payload = {
            "assigned_to": self.hitman.email,
            "target_name": "test name",
            "description": "fast and clean",
        }
        self.manager_hit = HitFactory(assigned_to=self.manager, requester=self.boss)
        self.manager2_hit = HitFactory(assigned_to=self.manager2, requester=self.boss)
        self.hitman_from_manager_hit = HitFactory(
            assigned_to=self.hitman, requester=self.manager
        )
        self.hitman_from_boss_hit = HitFactory(
            assigned_to=self.hitman, requester=self.boss
        )
        self.hitman2_from_boss_hit = HitFactory(
            assigned_to=self.hitman2, requester=self.boss
        )

    def test_given_a_hitman_user_then_cant_create_hits(self):
        self.client.force_authenticate(self.hitman)
        response = self.client.post(self.create_hits_url, self.create_hit_base_payload)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_given_a_hitman_user_then_can_view_only_hits_assigned_to_him(self):
        self.client.force_authenticate(self.hitman)
        response = self.client.get(self.create_hits_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), 2)
        self.assertEquals(response.json()[0]["assigned_to"]["email"], self.hitman.email)
        self.assertEquals(response.json()[0]["requester"]["email"], self.boss.email)
        self.assertEquals(response.json()[1]["assigned_to"]["email"], self.hitman.email)
        self.assertEquals(response.json()[1]["requester"]["email"], self.manager.email)

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
        self.client.force_authenticate(self.manager)
        response = self.client.get(self.create_hits_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), 3)
        self.assertEquals(
            response.json()[0]["assigned_to"]["email"], self.manager.email
        )
        self.assertEquals(response.json()[0]["requester"]["email"], self.boss.email)
        self.assertEquals(response.json()[1]["assigned_to"]["email"], self.hitman.email)
        self.assertEquals(response.json()[1]["requester"]["email"], self.manager.email)
        self.assertEquals(response.json()[2]["assigned_to"]["email"], self.hitman.email)
        self.assertEquals(response.json()[2]["requester"]["email"], self.boss.email)

    def test_given_a_manager_user_he_can_create_a_hit_for_any_of_his_lackeys(self):
        self.client.force_authenticate(self.manager)
        response = self.client.post(self.create_hits_url, self.create_hit_base_payload)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_given_a_manager_user_he_can_assign_a_hit_for_any_of_his_lackeys(self):
        self.assertEquals(True, False)

    def test_given_a_manager_then_cannot_assign_hits_to_himself(self):
        self.assertEquals(True, False)

    def test_given_a_boss_it_can_create_a_hit_for_any_hitman(self):
        self.client.force_authenticate(self.boss)
        response = self.client.post(self.create_hits_url, self.create_hit_base_payload)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_given_a_boss_it_can_create_a_hit_for_any_manager(self):
        self.client.force_authenticate(self.boss)
        self.create_hit_base_payload["assigned_to"] = self.manager.email
        response = self.client.post(self.create_hits_url, self.create_hit_base_payload)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_given_a_boss_it_can_view_all_the_hits(self):
        self.client.force_authenticate(self.boss)
        response = self.client.get(self.create_hits_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), len(Hit.objects.all()))

    def test_given_a_boss_then_cannot_assign_hits_to_inactive_users(self):
        self.assertEquals(True, False)

    def test_given_a_manager_then_cannot_assign_hits_to_inactive_users(self):
        self.assertEquals(True, False)

    def test_given_a_boss_then_cannot_assign_hits_to_himself(self):
        self.assertEquals(True, False)
