import factory

from cuser.models import CUser as User, Group


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.Faker("password", length=12)

    class Params:
        admin = factory.Trait(is_staff=True)
        super_user = factory.Trait(is_superuser=True)

    @factory.post_generation
    def add_user_role(obj, create, extracted, **kwargs):
        if create:
            if "hitman" in obj.email:
                role = Group.objects.get(name="hitman")
                role.user_set.add(obj)
            elif "manager" in obj.email:
                role = Group.objects.get(name="manager")
                role.user_set.add(obj)

        return obj
