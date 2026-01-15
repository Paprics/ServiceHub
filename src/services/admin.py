from django.contrib import admin
from .models import Product, Category, Package, FAQ, AdditionalService


admin.site.register(Product)


admin.site.register(Category)


admin.site.register(Package)


admin.site.register(FAQ)


admin.site.register(AdditionalService)