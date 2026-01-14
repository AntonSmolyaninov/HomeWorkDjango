from django.contrib import admin

from catalog.models import Product, Category, ContactInfo


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_product', 'category', 'purchase_price')
    list_filter = ('category',)
    search_fields = ('name', 'description_product')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'address')



