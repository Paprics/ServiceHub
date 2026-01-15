# src/services/views.py
from django.shortcuts import render
from django.views import View
from .models import Category, Product, AdditionalService, Package, FAQ

from .search_engine import SearchEngine

class IndexView(View):
    template_name = 'index.html'
    results_template = '_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        selected_category = request.GET.get('scope', 'all')

        categories = Category.objects.all()

        print("HX-Request header:", request.headers.get('HX-Request'))
        print("META HTTP_HX_REQUEST:", request.META.get('HTTP_HX_REQUEST'))

        # HTMX request?
        if request.headers.get('HX-Request') == 'true':
            results = SearchEngine.search(query=query, category_id=selected_category)
            print("DEBUG RESULTS:", results)
            return render(request, self.results_template, {'results': results})



        # обычная страница
        context = {
            'categories': categories,
            'query': query,
            'selected_category': selected_category,
        }
        return render(request, self.template_name, context)
