from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from catalog.models import Author, Book, BookInstance, Genre


class Command(BaseCommand):
    help = "Create the LibraryMember group with view-only permissions for catalog models."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="LibraryMember")
        models = [Author, Book, BookInstance, Genre]
        permissions = []
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions.extend(Permission.objects.filter(content_type=content_type, codename__startswith="view_"))
        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS(
            f'LibraryMember group {"created" if created else "updated"} with {len(permissions)} view permissions.'
        ))
