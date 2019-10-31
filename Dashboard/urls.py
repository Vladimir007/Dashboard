from django.contrib import admin
from django.urls import path, include

from Dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),

    path('', include(('core.urls', 'core'), namespace='core')),
]
