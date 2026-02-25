from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model

from catalog.forms import ProductForm, ProductModeratorForm, ProductOwnerForm
from catalog.models import ContactInfo, Product, Category  # Импортируем Category

User = get_user_model()


class HomePageView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "latest_products"

    def get_queryset(self):
        # Для обычных пользователей показываем только опубликованные
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Модератор продуктов').exists():
            # Модераторы видят все продукты
            return Product.objects.all().order_by("-created_at")[:6]
        else:
            # Обычные пользователи видят только опубликованные
            return Product.objects.filter(is_published=True).order_by("-created_at")[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем статистику
        context['total_products'] = Product.objects.filter(is_published=True).count()
        context['total_categories'] = Category.objects.count()  # Теперь Category импортирована
        context['total_sellers'] = User.objects.filter(products__isnull=False).distinct().count()

        # Проверяем, является ли пользователь модератором
        if self.request.user.is_authenticated:
            context['is_moderator'] = self.request.user.groups.filter(name='Модератор продуктов').exists()
        else:
            context['is_moderator'] = False

        return context


class ContactPageView(ListView):
    model = ContactInfo
    template_name = "contacts.html"
    context_object_name = "contacts"


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Фильтр по статусу для модераторов
        status = self.request.GET.get('status')
        if status == 'pending' and user.is_authenticated and user.groups.filter(name='Модератор продуктов').exists():
            queryset = queryset.filter(is_published=False)

        # Фильтр по владельцу
        owner_id = self.request.GET.get('owner')
        if owner_id and user.is_authenticated:
            queryset = queryset.filter(owner_id=owner_id)

        # Фильтр по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name_category=category)

        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name_product__icontains=search) |
                Q(description_product__icontains=search)
            )

        # Если пользователь не модератор, показываем только опубликованные
        if not user.is_authenticated or not user.groups.filter(name='Модератор продуктов').exists():
            queryset = queryset.filter(is_published=True)

        return queryset.select_related('category', 'owner').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_moderator'] = user.is_authenticated and user.groups.filter(name='Модератор продуктов').exists()
        context['categories'] = Category.objects.all()  # Добавляем категории для фильтрации

        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        product = self.get_object()

        # Проверяем доступ к неопубликованному продукту
        if not product.is_published:
            is_moderator = request.user.is_authenticated and request.user.groups.filter(
                name='Модератор продуктов').exists()
            is_owner = request.user.is_authenticated and request.user == product.owner

            if not (is_moderator or is_owner):
                messages.error(request, 'Этот продукт еще не опубликован и доступен только владельцу и модераторам')
                return redirect('catalog:product_list')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context.update({
                'is_moderator': user.groups.filter(name='Модератор продуктов').exists(),
                'is_owner': user == self.object.owner,
                'can_unpublish': user.has_perm('catalog.can_unpublish_product'),
            })

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductOwnerForm
    template_name = "product_form.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        messages.success(self.request, 'Продукт успешно создан и отправлен на модерацию')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "product_form.html"
    login_url = '/users/login/'

    def get_form_class(self):
        user = self.request.user
        if user.groups.filter(name='Модератор продуктов').exists():
            return ProductModeratorForm
        return ProductOwnerForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        user = self.request.user
        product = self.get_object()

        if user.groups.filter(name='Модератор продуктов').exists():
            return True

        return user == product.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не можете редактировать этот продукт')
        return redirect('catalog:product_detail', pk=self.get_object().pk)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def test_func(self):
        user = self.request.user
        product = self.get_object()

        is_owner = user == product.owner
        is_moderator = user.groups.filter(name='Модератор продуктов').exists()

        return is_owner or is_moderator

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого продукта')
        return redirect('catalog:product_detail', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Продукт "{product.name_product}" успешно удален')
        return super().delete(request, *args, **kwargs)


@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_published = False
        product.save()
        messages.success(request, f'Продукт "{product.name_product}" снят с публикации')
        return redirect('catalog:product_detail', pk=pk)

    return render(request, 'unpublish_confirm.html', {'product': product})
