# src/search/search_engine.py
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from services.models import Product, Package, AdditionalService, FAQ
from services.models import Category

class SearchEngine:

    MODEL_MAPPING = {
        'product': Product,
        'package': Package,
        'additional_service': AdditionalService,
        'faq': FAQ,
    }

    @staticmethod
    def search(query: str, category_id=None):
        """
        Возвращает словарь результатов для всех моделей с ранжированием.
        """
        results = {}

        if not query:
            return results

        # Поиск по Product
        products = Product.objects.all()
        if category_id and category_id != 'all':
            products = products.filter(category_id=category_id)

        products = products.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=SearchQuery(query))

        results['products'] = products

        # Поиск по Package
        packages = Package.objects.annotate(
            search=SearchVector('name', 'description'),
        ).filter(search=SearchQuery(query))
        if category_id and category_id != 'all':
            packages = packages.filter(product__category_id=category_id)
        results['packages'] = packages

        # Поиск по AdditionalService
        additional_services = AdditionalService.objects.annotate(
            search=SearchVector('name', 'description'),
        ).filter(search=SearchQuery(query))
        if category_id and category_id != 'all':
            additional_services = additional_services.filter(product__category_id=category_id)
        results['additional_services'] = additional_services

        # Поиск по FAQ
        faqs = FAQ.objects.annotate(
            search=SearchVector('question', 'answer'),
        ).filter(search=SearchQuery(query))
        if category_id and category_id != 'all':
            faqs = faqs.filter(product__category_id=category_id)
        results['faqs'] = faqs

        return results
