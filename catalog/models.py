from django.db import models
from django.conf import settings


class Product(models.Model):
    class PublicationStatus(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'
        ARCHIVED = 'archived', 'В архиве'

    name_product = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description_product = models.TextField(
        verbose_name="Описание", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="catalog/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        "Category",  # Используем строковое название модели
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию",
        blank=True,
        null=True,
        related_name="products",
    )
    purchase_price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Поле владельца
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        related_name="products",
        help_text="Владелец продукта"
    )

    # Поле статуса публикации
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Отметьте, чтобы опубликовать продукт"
    )

    publication_status = models.CharField(
        max_length=20,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        verbose_name="Статус публикации"
    )

    def __str__(self):
        return f"{self.name_product}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name_product", "-created_at"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]


class Category(models.Model):
    name_category = models.CharField(max_length=200, verbose_name="Название категории")
    description_category = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name_category"]


class ContactInfo(models.Model):
    company_name = models.CharField("Компания", max_length=255, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)
    inn = models.CharField("ИНН", max_length=20, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    working_hours = models.CharField("Часы работы", max_length=100, blank=True)

    def __str__(self):
        return self.company_name or "Контактные данные"
