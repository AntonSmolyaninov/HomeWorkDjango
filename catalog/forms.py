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

    # Добавляем поле для статуса публикации (только для модераторов)
    is_published = forms.BooleanField(
        required=False,
        label='Опубликовано',
        help_text='Отметьте, чтобы опубликовать продукт',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Product
        fields = ['name_product', 'description_product', 'image', 'category', 'purchase_price']
        labels = {
            'name_product': 'Наименование',
            'description_product': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'purchase_price': 'Цена',
        }
        help_texts = {
            'name_product': 'Введите наименование продукта',
            'description_product': 'Введите описание продукта',
            'image': 'Загрузите изображение продукта (JPEG или PNG, до 5 МБ)',
            'category': 'Выберите категорию',
            'purchase_price': 'Укажите цену в рублях',
        }
        widgets = {
            'description_product': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание продукта...'}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с учетом прав пользователя"""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Если это редактирование существующего продукта
        if self.instance and self.instance.pk:
            # Показываем поле is_published только модераторам
            if self.user and self.user.groups.filter(name='Модератор продуктов').exists():
                self.fields['is_published'].initial = self.instance.is_published
            else:
                # Для обычных пользователей скрываем поле is_published
                self.fields.pop('is_published')
        else:
            # Для новых продуктов всегда скрываем поле is_published
            self.fields.pop('is_published')

    def clean_purchase_price(self):
        """Валидация цены"""
        price = self.cleaned_data.get('purchase_price')
        if price is not None:
            if price < 0:
                raise forms.ValidationError("Цена не может быть отрицательной.")
            if price > 1000000:
                raise forms.ValidationError("Цена не может превышать 1 000 000 рублей.")
        return price

    def clean_name_product(self):
        """Валидация названия продукта"""
        name = self.cleaned_data.get('name_product')
        if name:
            if len(name) < 3:
                raise forms.ValidationError("Название должно содержать минимум 3 символа.")
            if len(name) > 150:
                raise forms.ValidationError("Название не может превышать 150 символов.")
            self._validate_forbidden_words(name, "названии")
        return name

    def clean_description_product(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get('description_product')
        if description:
            if len(description) < 10:
                raise forms.ValidationError("Описание должно содержать минимум 10 символов.")
            self._validate_forbidden_words(description, "описании")
        return description

    def clean_image(self):
        """Валидация изображения"""
        image = self.cleaned_data.get('image')

        # Если изображение не загружено, это нормально (поле необязательное)
        if not image:
            return image

        self._validate_image_size(image)
        self._validate_image_format(image)
        return image

    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()

        # Дополнительная проверка для модераторов
        if self.user and self.user.groups.filter(name='Модератор продуктов').exists():
            is_published = cleaned_data.get('is_published')
            # Можно добавить дополнительные проверки для модераторов
            if is_published and not self.instance.owner:
                self.add_error('is_published', 'Нельзя опубликовать продукт без владельца')

        return cleaned_data

    def save(self, commit=True):
        """Сохранение формы с дополнительной обработкой"""
        instance = super().save(commit=False)

        # Если пользователь - модератор и указал is_published
        if self.user and self.user.groups.filter(name='Модератор продуктов').exists():
            if 'is_published' in self.cleaned_data:
                instance.is_published = self.cleaned_data['is_published']

        if commit:
            instance.save()
        return instance

    def _validate_forbidden_words(self, value, field_name):
        """Проверка на запрещенные слова"""
        value_lower = value.lower()
        found_words = []

        for word in FORBIDDEN_WORDS:
            if word.lower() in value_lower:
                found_words.append(word)

        if found_words:
            raise forms.ValidationError(
                f"Использование запрещенных слов в {field_name}: {', '.join(found_words)}"
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
        valid_types = ['image/jpeg', 'image/jpg', 'image/png']
        if image.content_type not in valid_types:
            raise forms.ValidationError(
                f"Можно загружать только JPEG или PNG изображения. "
                f"Загружен формат: {image.content_type}"
            )


class ProductModeratorForm(ProductForm):
    """Форма для модераторов с дополнительными возможностями"""

    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields + ['is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем дополнительные поля для модераторов
        self.fields['is_published'].widget.attrs.update({
            'class': 'form-check-input',
            'role': 'switch'
        })
        self.fields['is_published'].help_text = 'Отметьте для публикации продукта'


class ProductOwnerForm(ProductForm):
    """Форма для владельцев продуктов (без поля публикации)"""

    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле is_published, если оно появилось
        if 'is_published' in self.fields:
            self.fields.pop('is_published')
