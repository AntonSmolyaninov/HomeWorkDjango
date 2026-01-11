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
        upload_to="product/image",
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
    description_category = models.DateField(verbose_name="Описание категории")

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name_category"]

