from django import forms
from django.conf import settings
from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class StyleFormMixin:
    """Миксин для стилизации полей формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования продуктов"""

    class Meta:
        model = Product
        fields = '__all__'

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_name_product(self):
        name = self.cleaned_data.get('name_product')
        if name:
            self._validate_forbidden_words(name, "названии")
        return name

    def clean_description_product(self):
        description = self.cleaned_data.get('description_product')
        if description:
            self._validate_forbidden_words(description, "описании")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        self._validate_image_size(image)
        self._validate_image_format(image)
        return image

    def _validate_forbidden_words(self, value, field_name):
        """Проверка на запрещенные слова"""
        value_lower = value.lower()
        for word in FORBIDDEN_WORDS:
            if word.lower() in value_lower:
                raise forms.ValidationError(
                    f"Использование слова '{word}' в {field_name} запрещено."
                )

    def _validate_image_size(self, image, max_size_mb=5):
        """Проверка размера изображения"""
        max_size = max_size_mb * 1024 * 1024
        if image.size > max_size:
            current_size_mb = image.size / 1024 / 1024
            raise forms.ValidationError(
                f"Размер изображения не должен превышать {max_size_mb} МБ. "
                f"Текущий размер: {current_size_mb:.1f} МБ"
            )

    def _validate_image_format(self, image):
        """Проверка формата изображения"""
        valid_types = ['image/jpeg', 'image/png', 'image/jpg']
        if image.content_type not in valid_types:
            raise forms.ValidationError(
                f"Можно загружать только JPEG или PNG изображения. "
                f"Загружен формат: {image.content_type}"
            )