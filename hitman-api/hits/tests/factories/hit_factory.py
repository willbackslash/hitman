import factory
from factory import SubFactory

from hits.models import Hit, HitStatus
from users.tests.factories.user_factory import UserFactory


class HitFactory(factory.django.DjangoModelFactory):
    """
    Factory to create hits
    """

    class Meta:
        model = Hit

    assigned_to = SubFactory(UserFactory)
    target_name = "bla bla bla"
    description = "bla bla bla"
    status = HitStatus.ASSIGNED
    requester = SubFactory(UserFactory)
