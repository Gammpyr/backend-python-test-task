import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to="category/images/",
        null=False,
        blank=True,
        verbose_name='Изображение'
    )
    subcategory = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Подкатегория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}' + f' ({self.subcategory})' if self.subcategory else ''

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Products(models.Model):
    """Модель продуктов"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to="products/images/",
        null=True,
        blank=True,
        verbose_name="Изображение"
    )
    price = models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Цена')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name='Категории',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image_small = models.ImageField(upload_to='products/small/', blank=True, verbose_name="Маленькое (150x150)")
    image_medium = models.ImageField(upload_to='products/medium/', blank=True, verbose_name="Среднее (300x300)")
    image_large = models.ImageField(upload_to='products/large/', blank=True, verbose_name="Большое (600x600)")

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"
        ordering = ['name']

    def __str_(self):
        return f'{self.category} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        if self.image:
            self.create_thumbnail_images()

    def create_thumbnail_images(self):
        """Создание трех версий изображения"""

        # Размеры для изображений (ширина, высота)
        sizes = {
            'image_small': (150, 150),
            'image_medium': (300, 300),
            'image_large': (600, 600)
        }

        img_original = Image.open(self.image.path)

        if img_original.mode in ('RGBA', 'P'):
            img_original = img_original.convert('RGB')

        for field_name, size in sizes.items():
            img = img_original.copy()

            img.thumbnail(size, Image.Resampling.LANCZOS)

            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)

            name_parts = os.path.splitext(os.path.basename(self.image.name))
            thumb_filename = f"{name_parts[0]}_{size[0]}x{size[1]}.jpg"

            getattr(self, field_name).save(thumb_filename, ContentFile(thumb_io.getvalue()), save=False)

        super().save(update_fields=['image_small', 'image_medium', 'image_large'])
