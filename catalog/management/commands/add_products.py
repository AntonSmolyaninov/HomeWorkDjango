from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет все существующие категории и продукты и добавляет тестовые данные"

    def handle(self, *args, **options):
        self.stdout.write("Удаляю все продукты...")
        Product.objects.all().delete()

        self.stdout.write("Удаляю все категории...")
        Category.objects.all().delete()

        self.stdout.write("Добавляю тестовые категории...")
        cat1 = Category.objects.create(
            name_category="Рассылки",
            description_category="Сервисы для массовых рассылок",
        )
        cat2 = Category.objects.create(
            name_category="Телеграм боты", description_category="Боты для Telegram"
        )
        cat3 = Category.objects.create(
            name_category="Веб-приложения",
            description_category="Готовые веб-приложения",
        )

        self.stdout.write("Добавляю тестовые продукты...")
        Product.objects.create(
            name_product="Email Pro",
            description_product="Платформа для email рассылок",
            category=cat1,
            purchase_price=140,
        )
        Product.objects.create(
            name_product="Telegram Helper Bot",
            description_product="Бот-помощник для Telegram",
            category=cat2,
            purchase_price=200,
        )
        Product.objects.create(
            name_product="Dashboard WebApp",
            description_product="Современная веб-панель управления",
            category=cat3,
            purchase_price=500,
        )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно добавлены!"))
