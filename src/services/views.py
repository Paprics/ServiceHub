from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import Category


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


