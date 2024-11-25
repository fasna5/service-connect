from django.urls import path
from franchise.views import FranchiseeStatsView


urlpatterns=[
    path('franchisee/',FranchiseeStatsView.as_view(),name='franchisee'),
]


