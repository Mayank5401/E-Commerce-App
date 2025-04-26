from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from django.http import JsonResponse ,HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, CartItem,Order, OrderItem, Category, Rating
from django.forms import forms
from .paypal_config import client_id
from django.template.loader import render_to_string
from django.utils import timezone
import pdfkit

PDFKIT_CONFIG = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
)

@login_required
def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'store/home.html', context)

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'store/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    avg_rating = Rating.objects.filter(product=product).aggregate(Avg('score'))['score__avg']
    reviews = Rating.objects.filter(product=product).select_related('user')

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else None
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f"Updated quantity of {product.title} in your cart.")
    else:
        messages.success(request, f"Added {product.title} to your cart.")

    return redirect('view_cart')

@login_required
def update_cart(request, product_id):
    action = request.POST.get('action')
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
    except CartItem.DoesNotExist:
        messages.warning(request, f"{product.title} is not in your cart.")

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total() for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('view_cart')  

    total_price = sum(item.get_total() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'paypal_client_id': client_id,  
    }

    return render(request, 'store/checkout.html', context)

@login_required
def cod_checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('view_cart')

        total_price = sum(item.get_total() for item in cart_items)

        # Create the Order
        order = Order.objects.create(
            user=request.user,
            placed_at=timezone.now(),
            total_price=total_price,
            is_paid=False,
            payment_method='cod'
        )

        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear user's cart
        cart_items.delete()

        messages.success(request, "Order placed successfully. Pay upon delivery.")
        return redirect(reverse('order_success', kwargs={'order_id': order.id}))

    return redirect('checkout')

@csrf_exempt
@login_required
def payment_success(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return JsonResponse({'error': 'Cart is empty.'}, status=400)

        total_price = sum(item.get_total() for item in cart_items)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            placed_at=timezone.now(),
            total_price=total_price,
            is_paid=True,  # Since PayPal was used
            payment_method='paypal'
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart_items.delete()

        return JsonResponse({'message': 'Payment successful', 'order_id': order.id})


    return JsonResponse({'error': 'Invalid request'}, status=400)
    
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order:
        CartItem.objects.all().delete()
    return render(request, 'store/order_success.html', {'order': order})

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(user=request.user, product=product).delete()
    return redirect('view_cart')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-placed_at')
    return render(request, 'store/order_history.html', {'orders': orders})

from .forms import RatingForm

@login_required
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    'score': form.cleaned_data['score'],
                    'review': form.cleaned_data['review']
                }
            )
            messages.success(request, "Thanks for rating!")
            return redirect('product_detail', product_id=product.id)
    else:
        form = RatingForm()
    return render(request, 'store/rate_product.html', {'product': product, 'form': form})

@login_required
def generate_invoice(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    html_string = render_to_string('store/invoice.html', {'order': order})
    pdf = pdfkit.from_string(html_string, False, configuration=PDFKIT_CONFIG)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{order.id}.pdf'

    return response