from catalog.models import Product


def moderator_context(request):
    """Контекстный процессор для добавления данных модератора"""
    context = {}

    if request.user.is_authenticated:
        # Проверяем, является ли пользователь модератором
        is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

        if is_moderator:
            # Считаем количество продуктов на модерации
            context['pending_products_count'] = Product.objects.filter(is_published=False).count()

    return context