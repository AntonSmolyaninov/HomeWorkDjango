from django.db import models


class Product(models.Model):
    name_product = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description_product = models.TextField(
        max_length=150, verbose_name="Описание", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="'catalog/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изоброжение продукта",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите наименование категории",
        blank=True,
        null=True,
        related_name="products",
    )
    purchase_price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_product} {self.description_product}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name_product"]


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