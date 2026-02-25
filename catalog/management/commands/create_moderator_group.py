from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов продуктов и назначает разрешения'

    def handle(self, *args, **options):
        # Получаем или создаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        content_type = ContentType.objects.get_for_model(Product)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['can_unpublish_product', 'delete_product']
        )

        for permission in permissions:
            moderator_group.permissions.add(permission)

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" успешно создана')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" уже существует, разрешения обновлены')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Назначены разрешения: {", ".join([p.codename for p in permissions])}')
        )
