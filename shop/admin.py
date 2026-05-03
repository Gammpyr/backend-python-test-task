from django import forms
from django.contrib import admin

from shop.models import Category, Product, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'subcategory', )
    list_filter = ['subcategory']
    search_fields = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(subcategories__isnull=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'slug', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'price')
        }),
        ('Изображения', {
            'fields': ('image', ),
            'description': 'Изображение будет автоматически преобразовано в 3 размера'
        }),
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['user']
    search_fields = ('user', )