from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Kategori, Product, Cart, CartItem, Order, OrderItem
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib import messages

# Daftar produk
def product_list(request):
    categories = Kategori.objects.all()
    products = Product.objects.filter(is_active=True)

    # Debugging output
    print("Categories:", categories)
    print("Products:", products)

    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'products': products
    })
# Detail produk
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Kategori.objects.all()  # Mengambil semua kategori
    return render(request, 'shop/product_detail.html', {
        'product': product, 
        'categories': categories})

def category_detail(request, slug):
    print(f"Slug diterima: {slug}")  # Log slug

    try:
        category = get_object_or_404(Kategori, slug=slug)
        print(f"Kategori ditemukan: {category.name}")  # Log kategori
    except Exception as e:
        print(f"Error: {e}")
        return render(request, '404.html')  # Atau tampilkan halaman error

    products = Product.objects.filter(category=category, is_active=True)
    print(f"Produk dalam kategori: {products.count()}")  # Log jumlah produk

    categories = Kategori.objects.all()
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })


@login_required
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Ambil quantity dari form, set default 1 jika tidak ada atau invalid
    try:
        quantity = int(request.POST.get('quantity', 1))  # Default 1 jika tidak ada quantity
    except ValueError:
        quantity = 1  # Jika ada error saat konversi, set ke 1

    # Validasi quantity tidak melebihi stok yang tersedia
    if quantity > product.stock_produk:
        messages.error(request, f"Jumlah yang diminta melebihi stok yang tersedia. Stok produk: {product.stock_produk}.")
        return redirect('product_detail', slug=product.slug)
    
    # Ambil atau buat keranjang belanja untuk user
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Periksa apakah produk sudah ada dalam keranjang
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        # Jika produk sudah ada, tambahkan kuantitasnya
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Produk {product.name} telah diperbarui di keranjang.')
    else:
        # Jika produk baru, set kuantitasnya
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Produk {product.name} telah ditambahkan ke keranjang.')
    
    # Redirect ke halaman keranjang setelah menambah produk
    return redirect('cart_detail')



@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = cart.total_price  # Menggunakan properti total_price dari Cart
    
    return render(request, 'shop/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    messages.success(request, 'Produk telah dihapus dari keranjang.')
    return redirect('cart_detail')


# Checkout

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if cart.total_items == 0:
        messages.error(request, 'Keranjang belanja Anda kosong!')
        return redirect('cart_detail')
    
    # Buat order baru
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price,  # Total harga yang dihitung dari Cart
        status='PENDING'
    )
    
    # Tambahkan produk ke order
    for item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    
    # Hapus item dari keranjang setelah checkout
    cart.cartitem_set.all().delete()
    
    # Mengarahkan ke halaman detail pesanan setelah checkout
    messages.success(request, 'Pesanan Anda telah diproses! Berikut adalah detail pesanan Anda.')
    return redirect('order_detail', order_id=order.id)

# Detail pesanan (termasuk konfirmasi)
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.order_items.all()  # Mengambil semua OrderItem terkait dengan Order

    # Menghitung total price untuk setiap item (quantity * price)
    for item in order_items:
        item.total_price = item.quantity * item.price

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order.total_amount,
        'order_status': order.get_status_display(),
    }

    return render(request, 'shop/order_detail.html', context)


# Tambah produk (admin atau pengguna tertentu)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Ganti dengan URL tujuan
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

def save_category(request):
    if request.method == 'POST':
        category_slug = request.POST.get('category_slug')
        if category_slug:
            try:
                category = Kategori.objects.get(slug=category_slug)
                # Tambahkan logika penyimpanan data kategori
                messages.success(request, 'Kategori berhasil disimpan.')
                return redirect('some_view_name')  # Ganti dengan nama view tujuan
            except Kategori.DoesNotExist:
                messages.error(request, 'Kategori tidak ditemukan.')
        else:
            messages.error(request, 'Slug kategori tidak ditemukan.')
    else:
        messages.error(request, 'Metode tidak diizinkan.')

    return redirect('some_view_name')