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