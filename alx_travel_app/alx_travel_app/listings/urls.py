from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'listings', views.ListingViewSet)
router.register(r'listing-images', views.ListingImageViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'bookings', views.BookingViewSet, basename='booking')

app_name = 'listings'

urlpatterns = [
    # API Root
    path('', include(router.urls)),

    # Custom endpoints
    # path('custom-endpoint/', views.custom_view, name='custom-endpoint'),
]