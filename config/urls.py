from django.contrib import admin
from django.urls import path
from foo_app import views


urlpatterns = [
    ## main ---------------------------------------------------------
    path('info/', views.info, name='info_url'),
    ## other --------------------------------------------------------
    path('', views.root, name='root_url'),
    path('admin/', admin.site.urls),
    path('error_check/', views.error_check, name='error_check_url'),
    path('version/', views.version, name='version_url'),
]
