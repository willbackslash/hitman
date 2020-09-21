from django.contrib.auth.hashers import make_password
from django.db import migrations


def up(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("cuser", "CUser")
    ManagerUser = apps.get_model("users", "ManagerUser")

    User.objects.using(db_alias).bulk_create(
        [
            User(
                first_name="Big",
                last_name="Boss",
                email="theboss@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=True,
            ),
            User(
                first_name="Manager",
                last_name="One",
                email="manager1@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Manager",
                last_name="Two",
                email="manager2@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Manager",
                last_name="Three",
                email="manager3@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="One",
                email="hitman1@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Two",
                email="hitman2@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Three",
                email="hitman3@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Four",
                email="hitman4@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Five",
                email="hitman5@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Six",
                email="hitman6@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Seven",
                email="hitman7@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Eight",
                email="hitman8@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
            User(
                first_name="Hitman",
                last_name="Nine",
                email="hitman9@hitman.com",
                password=make_password("hitman2020"),
                is_superuser=False,
            ),
        ]
    )
    manager_group = Group.objects.get(name="manager")
    manager_group.user_set.add(*User.objects.filter(first_name="Manager").all())
    hitman_group = Group.objects.get(name="hitman")
    hitman_group.user_set.add(*User.objects.filter(first_name="Hitman").all())

    ManagerUser.objects.using(db_alias).bulk_create(
        [
            ManagerUser(
                manager=User.objects.get(email="manager1@hitman.com"),
                user=User.objects.get(email="hitman1@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager1@hitman.com"),
                user=User.objects.get(email="hitman2@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager1@hitman.com"),
                user=User.objects.get(email="hitman3@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager2@hitman.com"),
                user=User.objects.get(email="hitman4@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager2@hitman.com"),
                user=User.objects.get(email="hitman5@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager2@hitman.com"),
                user=User.objects.get(email="hitman6@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager3@hitman.com"),
                user=User.objects.get(email="hitman7@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager3@hitman.com"),
                user=User.objects.get(email="hitman8@hitman.com"),
            ),
            ManagerUser(
                manager=User.objects.get(email="manager3@hitman.com"),
                user=User.objects.get(email="hitman9@hitman.com"),
            ),
        ],
    )


def down(apps, schema_editor):
    User = apps.get_model("cuser", "CUser")
    User.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_auto_20200916_1642"),
    ]
    operations = [migrations.RunPython(up, down)]
