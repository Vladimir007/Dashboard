from django.template.defaulttags import register
from django.views.generic import ListView, TemplateView

from Dashboard.views import StreamingResponseView

from core.models import Action, Unit, Category, ActionAnomaly
from core.download import ActionsFileGenerator, UnitsFileGenerator, CategoriesFileGenerator


@register.filter
def index(indexable, i):
    return indexable[i]


class ActionView(ListView):
    template_name = 'core/action_tree.html'

    def get_queryset(self):
        return Action.objects.filter(parent=None)

    def get_context_data(self, *args, **kwargs):
        context = super(ActionView, self).get_context_data(*args, **kwargs)
        context['anomalies'] = ActionAnomaly.objects.select_related('action1', 'action2')
        return context


class UnitView(ListView):
    template_name = 'core/unit_tree.html'

    def get_queryset(self):
        return Unit.objects.filter(parent=None)


class CategoryView(ListView):
    template_name = 'core/category_tree.html'

    def get_queryset(self):
        return Category.objects.filter(parent=None)


class DownloadActionsView(StreamingResponseView):
    def get_generator(self):
        return ActionsFileGenerator()


class DownloadUnitsView(StreamingResponseView):
    def get_generator(self):
        return UnitsFileGenerator()


class DownloadCategoriesView(StreamingResponseView):
    def get_generator(self):
        return CategoriesFileGenerator()


class TripleLinksView(TemplateView):
    template_name = 'core/links.html'

    def get_context_data(self, **kwargs):
        context = super(TripleLinksView, self).get_context_data(**kwargs)
        context['actions'] = Action.objects.filter(parent=None)
        context['units'] = Unit.objects.filter(parent=None)
        context['categories'] = Category.objects.filter(parent=None)
        return context
