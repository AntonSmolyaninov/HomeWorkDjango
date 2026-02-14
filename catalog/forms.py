from django import forms
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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                # Стиль для чекбоксов
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'
                # Стиль для файла
                elif isinstance(field.widget, forms.FileInput):
                    field.widget.attrs['class'] = 'form-control-file'
                # Для остальных — Bootstrap-овский form-control
                else:
                    field.widget.attrs['class'] = 'form-control'

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_name_product(self):
        name = self.cleaned_data.get('name_product')
        if name:
            for word in FORBIDDEN_WORDS:
                if word.lower() in name.lower():
                    raise forms.ValidationError(
                        f"Использование слова '{word}' в названии запрещено."
                    )
        return name

    def clean_description_product(self):
        description = self.cleaned_data.get('description_product')
        if description:
            for word in FORBIDDEN_WORDS:
                if word.lower() in description.lower():
                    raise forms.ValidationError(
                        f"Использование слова '{word}' в описании запрещено."
                    )
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверяем размер файла
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise forms.ValidationError("Размер изображения не должен превышать 5 МБ.")

            # Проверяем формат
            valid_types = ['image/jpeg', 'image/png']
            if image.content_type not in valid_types:
                raise forms.ValidationError("Можно загружать только JPEG или PNG изображения.")
        return image