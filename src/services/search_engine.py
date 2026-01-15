# src/search/search_engine.py
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from services.models import Product, Package, AdditionalService, FAQ, Category

class SearchEngine:

    @staticmethod
    def search(query: str, category_id=None):

        results = {}

        if not query:
            return results

        products = Product.objects.all()
        if category_id and category_id != 'all':
            products = products.filter(category_id=category_id)

        products = products.annotate(
            search=SearchVector('title', 'description'),
        ).filter(search=SearchQuery(query))

        results['products'] = products

        packages = Package.objects.annotate(
            search=SearchVector('name', 'description'),
        ).filter(search=SearchQuery(query))
        if category_id and category_id != 'all':
            packages = packages.filter(product__category_id=category_id)
        results['packages'] = packages

        additional_services = AdditionalService.objects.annotate(
            search=SearchVector('name', 'description'),
        ).filter(search=SearchQuery(query))
        if category_id and category_id != 'all':
            additional_services = additional_services.filter(product__category_id=category_id)
        results['additional_services'] = additional_services

        faqs = FAQ.objects.annotate(
            search=SearchVector('question', 'answer'),
        ).filter(search=SearchQuery(query))
        if category_id and category_id != 'all':
            faqs = faqs.filter(product__category_id=category_id)
        results['faqs'] = faqs

        return results
