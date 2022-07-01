from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import ProductListView,ProductDetailView,add_to_cart,remove_from_cart
app_name = 'core'
urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
    path('product/<slug>/', ProductDetailView.as_view(), name="product-detail"),
    path('add_to_cart/<slug>/',add_to_cart, name="add-to-cart"),
    path('remove_from_cart/<slug>/',remove_from_cart, name="remove-from-cart"),
]

