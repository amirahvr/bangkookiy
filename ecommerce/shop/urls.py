from django.urls import path
from . import views

urlpatterns = [
    # Halaman daftar produk
    path('', views.product_list, name='product_list'),
    # Halaman daftar produk berdasarkan kategori
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    # Halaman detail produk
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # Menambahkan produk ke keranjang
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    # Menampilkan keranjang
    path('cart/', views.cart_detail, name='cart_detail'),
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    # Halaman detail pesanan
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    # Menambahkan produk (admin atau pengguna tertentu)
    path('add-product/', views.add_product, name='add_product'),
]
