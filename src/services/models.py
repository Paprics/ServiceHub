from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        blank=False,
    )

    def __str__(self):
        return f'{self.title} | {self.category.name}'
