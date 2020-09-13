from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations


def up(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, db_alias)
    Group = apps.get_model("auth", "Group")
    Group.objects.using(db_alias).bulk_create(
        [Group(name="hitman"), Group(name="manager")]
    )


def down(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["hitman", "manager"]).delete()


class Migration(migrations.Migration):
    dependencies = []
    operations = [migrations.RunPython(up, down)]
