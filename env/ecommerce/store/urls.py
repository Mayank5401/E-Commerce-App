from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cod_checkout/', views.cod_checkout, name='cod_checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('order_success/<int:order_id>/', views.order_success, name="order_success"),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_history, name='order_history'),
    path('rate/<int:product_id>/', views.rate_product, name='rate_product'),
     path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),

]
