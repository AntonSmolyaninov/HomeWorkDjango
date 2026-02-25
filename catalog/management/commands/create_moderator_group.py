from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()  # Получаем актуальную модель пользователя


class Command(BaseCommand):
    help = 'Создает группу модераторов продуктов и назначает разрешения'

    def handle(self, *args, **options):
        # Создаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем необходимые разрешения
        # Кастомное разрешение на отмену публикации
        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type
        )

        # Стандартное разрешение на удаление
        can_delete = Permission.objects.get(
            content_type=content_type,
            codename='delete_product'
        )

        # Очищаем старые разрешения и добавляем новые
        moderator_group.permissions.clear()
        moderator_group.permissions.add(can_unpublish, can_delete)

        # Добавляем также разрешение на просмотр всех продуктов
        can_view = Permission.objects.get(
            content_type=content_type,
            codename='view_product'
        )
        moderator_group.permissions.add(can_view)

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" успешно создана')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" уже существует, разрешения обновлены')
            )

        self.stdout.write(
            self.style.SUCCESS('Назначены разрешения: can_unpublish_product, delete_product, view_product')
        )
