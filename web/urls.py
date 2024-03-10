from django.urls import path
from . import views

urlpatterns = [
    path("", views.web_index, name="web_index"),

    # Category ##################################################
    path("category/<slug:slug>/", views.web_category, name="web_category"),

    # Products ##################################################
    path("product/<slug:slug>/", views.web_product, name="web_product"),
    path("products/", views.web_products, name="web_products"),
    path("products/discount/", views.web_products_discount, name="web_products_disocunt"),

    # Cart ##################################################
    path("cart/", views.web_cart, name="web_cart"),
    path("cart/get/", views.web_cart_get, name="web_cart_get"),
    path("order/send/", views.web_order_send, name="web_order_send"),
    path("masters/", views.web_masters, name="web_masters"),
]