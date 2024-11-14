from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('login/',views.login_view,name='login'),
    path('fetch_service_provider_data/',views.fetch_service_provider_data,name='fetch_service_provider_data')
]