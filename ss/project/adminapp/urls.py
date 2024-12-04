from django.urls import path,include
from adminapp.views import UserDetails,CompletedPaymentListView,ServiceRequestListView,SubcategoryListView,SubcategorySearch,SubcategorySortView
from rest_framework.routers import DefaultRouter
# Initialize the router and register the viewset
router = DefaultRouter()
router.register(r'subcategories', SubcategorySearch, basename='subcategory')





urlpatterns=[
    path('api/', include(router.urls)),  # Include the router URLs in your application
    path('sort/', SubcategorySortView.as_view(), name='sort'),

    path('userdetails/',UserDetails.as_view(),name='userdetails'),
    path('payment/',CompletedPaymentListView.as_view(),name='payment'),
    path('recent/',ServiceRequestListView.as_view(),name='recent'),
    path('subcategory/',SubcategoryListView.as_view(),name='subcategory'),
]

# To debug, you can print the urlpatterns
for url in urlpatterns:
    print(url)