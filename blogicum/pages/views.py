from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def access_is_denied(request, exception):
    return render(request, 'pages/403csrf.html', status=403)


def error_internal_server(request):
    return render(request, 'pages/500.html', status=500)
