from django.urls import path
from adminapp.views import UserDetails


urlpatterns=[
    path('userdetails/',UserDetails.as_view(),name='userdetails'),
]

