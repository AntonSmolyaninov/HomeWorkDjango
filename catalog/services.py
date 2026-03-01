from django.core.cache import cache
from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_all_products():
    """Получает все продукты с кэшированием"""
    if not CACHE_ENABLED:
        return Product.objects.all().select_related('category', 'owner')

    products = cache.get('all_products')
    if not products:
        products = Product.objects.all().select_related('category', 'owner')
        cache.set('all_products', products, 300)
    return products
