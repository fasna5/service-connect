from django.urls import path
from .views import BlockServiceProviderView

urlpatterns = [
    path('block-service-provider/', BlockServiceProviderView.as_view(), name='block_service_provider'),
]