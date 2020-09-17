import factory
from factory import SubFactory

from users.models import ManagerUser
from users.tests.factories.user_factory import UserFactory


class ManagerUserFactory(factory.django.DjangoModelFactory):
    """
    Factory to create manager users
    """

    class Meta:
        model = ManagerUser

    manager = SubFactory(UserFactory)
    user = SubFactory(UserFactory)
