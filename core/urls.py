from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import (
    ProductListView,
    ProductDetailView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    checkout_view,
    remove_single_item_from_cart,
    CheckoutView)
app_name = 'core'
urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
    path('order-summary/',OrderSummaryView.as_view(), name="order-summary"),
    path('checkout/',CheckoutView.as_view(), name="check-out"),
    path('product/<slug>/', ProductDetailView.as_view(), name="product-detail"),
    path('add_to_cart/<slug>/',add_to_cart, name="add-to-cart"),
    path('remove_from_cart/<slug>/',remove_from_cart, name="remove-from-cart"),
    path('remove_single_item_from_cart/<slug>/',remove_single_item_from_cart, name="remove-single-item-from-cart"),
]

