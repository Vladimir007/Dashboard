from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from core.models import Action, Unit, Category, TripleLink, ActionAnomaly
from core.serializers import (
    ActionSerializer, UnitSerializer, CategorySerializer, TripleLinkSerializer, ActionAnomalySerializer
)
from core.upload import UploadActions, UploadUnits, UploadCategories


class ActionAPIViewset(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def get_serializer(self, *args, **kwargs):
        fields = None
        if self.request.method == 'POST':
            fields = {'parent', 'phrases'}
        elif self.request.method in {'PUT', 'PATCH'}:
            fields = {'phrases'}
        return super().get_serializer(*args, fields=fields, **kwargs)


class UnitAPIViewset(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_serializer(self, *args, **kwargs):
        fields = None
        if self.request.method == 'POST':
            fields = {'parent', 'names'}
        elif self.request.method in {'PUT', 'PATCH'}:
            fields = {'names'}
        return super().get_serializer(*args, fields=fields, **kwargs)


class CategoryAPIViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer(self, *args, **kwargs):
        fields = None
        if self.request.method == 'POST':
            fields = {'parent', 'name'}
        elif self.request.method in {'PUT', 'PATCH'}:
            fields = {'name'}
        return super().get_serializer(*args, fields=fields, **kwargs)


class TripleLinkViewSet(ModelViewSet):
    queryset = TripleLink.objects.all()
    serializer_class = TripleLinkSerializer


class ActionAnomalyViewSet(ModelViewSet):
    queryset = ActionAnomaly.objects.all()
    serializer_class = ActionAnomalySerializer


class TreeChildrenAPIBaseView(APIView):
    model = None
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, pk):
        assert self.model is not None, 'Wrong usage!'

        is_form = request.query_params.get('form')
        if is_form == 'true':
            template_name = 'core/tree_children.html'
        else:
            template_name = 'core/links_tree.html'

        return Response({
            'object_list': self.model.objects.filter(parent_id=pk)
        }, template_name=template_name)


class ActionChildrenAPIView(TreeChildrenAPIBaseView):
    model = Action


class UnitChildrenAPIView(TreeChildrenAPIBaseView):
    model = Unit


class CategoryChildrenAPIView(TreeChildrenAPIBaseView):
    model = Category


class UploadActionsAPIView(APIView):
    def post(self, request):
        UploadActions(request.FILES['file'])
        return Response({})


class UploadUnitsAPIView(APIView):
    def post(self, request):
        UploadUnits(request.FILES['file'])
        return Response({})


class UploadCategoriesAPIView(APIView):
    def post(self, request):
        UploadCategories(request.data['columns'], request.FILES['file'])
        return Response({})


class RemoveTripleLinkAPIView(APIView):
    def delete(self, request):
        TripleLink.objects.filter(
            action_id=request.data['action'],
            unit_id=request.data['unit'],
            category_id=request.data['category']
        ).delete()
        return Response({})


class CheckTripleLinkAPIView(APIView):
    def get(self, request):
        return Response({
            'exists': TripleLink.objects.filter(
                action_id=request.query_params['action'],
                unit_id=request.query_params['unit'],
                category_id=request.query_params['category']
            ).exists()
        })
