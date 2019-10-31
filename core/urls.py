from django.urls import path, include

from rest_framework.routers import DefaultRouter

from core import views, api


router = DefaultRouter()
router.register('action', api.ActionAPIViewset, 'api-action')
router.register('unit', api.UnitAPIViewset, 'api-unit')
router.register('category', api.CategoryAPIViewset, 'api-category')
router.register('links', api.TripleLinkViewSet, 'api-links')
router.register('anomaly', api.ActionAnomalyViewSet, 'api-anomaly')

urlpatterns = [
    path('api/', include(router.urls)),

    path('action/', views.ActionView.as_view(), name='action-tree'),
    path('unit/', views.UnitView.as_view(), name='unit-tree'),
    path('category/', views.CategoryView.as_view(), name='category-tree'),
    path('links/', views.TripleLinksView.as_view(), name='links'),

    path('api/action-children/<int:pk>/', api.ActionChildrenAPIView.as_view(), name='api-action-children'),
    path('api/unit-children/<int:pk>/', api.UnitChildrenAPIView.as_view(), name='api-unit-children'),
    path('api/category-children/<int:pk>/', api.CategoryChildrenAPIView.as_view(), name='api-category-children'),

    path('api/actions-upload/', api.UploadActionsAPIView.as_view(), name='upload-actions'),
    path('api/units-upload/', api.UploadUnitsAPIView.as_view(), name='upload-units'),
    path('api/categories-upload/', api.UploadCategoriesAPIView.as_view(), name='upload-categories'),

    path('actions-download/', views.DownloadActionsView.as_view(), name='download-actions'),
    path('units-download/', views.DownloadUnitsView.as_view(), name='download-units'),
    path('categories-download/', views.DownloadCategoriesView.as_view(), name='download-categories'),

    path('api/check-link/', api.CheckTripleLinkAPIView.as_view(), name='api-check-link'),
    path('api/destroy-link/', api.RemoveTripleLinkAPIView.as_view(), name='api-destroy-link'),
]
