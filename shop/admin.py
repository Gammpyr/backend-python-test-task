from django.contrib import admin

from shop.models import Category, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'subcategory', )
    list_filter = 'subcategory'
    search_field = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category',]
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'price')
        }),
        ('Изображения', {
            'fields': ('image', 'image_small', 'image_medium', 'image_large'),
            'description': 'Оригинальное изображение будет автоматически преобразовано в 3 размера'
        }),
    )

