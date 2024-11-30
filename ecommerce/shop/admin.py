from django.contrib import admin
from .models import Kategori, Product, Cart, CartItem, Order, OrderItem

# Gunakan dekorator untuk pendaftaran model Kategori
@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'price', 'stock_produk', 'is_active', 'category', 'created_at')
    list_filter = ('is_active', 'category')

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'created_at', 'updated_at')  # Tambahkan metode custom
    
    def user_username(self, obj):
        return obj.user.username  # Mengambil username dari objek user yang terkait
    user_username.short_description = 'Username'  # Menambahkan label kolom

# Model lain tetap menggunakan admin.site.register
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
