from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, WishlistItem, Cart
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import Product, Cart, CartItem
from .cart import Cart
from django.contrib.auth.forms import UserCreationForm
from twilio.rest import Client
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from io import BytesIO
from reportlab.lib.pagesizes import letter
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from reportlab.pdfgen import canvas
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import json
from io import BytesIO
from django.contrib.auth.decorators import login_required

def home(request):
    category = request.GET.get('category')
    filters = {
        'storage': request.GET.get('storage'),
        'condition': request.GET.get('condition'),
        'min_price': request.GET.get('min_price'),
        'max_price': request.GET.get('max_price'),
    }

    products = Product.objects.all()
    if category:
        products = products.filter(type=category)
    if filters['storage']:
        products = products.filter(storage_size=filters['storage'])
    if filters['condition']:
        products = products.filter(condition=filters['condition'])
    if filters['min_price']:
        products = products.filter(price__gte=filters['min_price'])
    if filters['max_price']:
        products = products.filter(price__lte=filters['max_price'])
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'An_Apple/home.html', {'featured_products': featured_products})

def account(request):
    # Logic for the account page, like user profile
    return render(request, 'account.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')  # Redirect to home or any other page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'An_Apple/register.html', {'form': form})

def cart(request):
    # If the user is not authenticated, allow access to the cart but restrict checkout
    if not request.user.is_authenticated:
        # You can still display the cart page without requiring login
        cart_items = Cart.objects.filter(user=request.user)
        cart_total = sum(item.total_price for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

    # For authenticated users, allow checkout
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

def get_cart(request):
    from An_Apple.models import Cart
    session_key = request.session.session_key or request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request, product_id):
    # Get the product by ID
    product = Product.objects.get(id=product_id)
    session_key = request.session.session_key

    # If no session exists, create one
    if not session_key:
        request.session.create()

    # Get or create a cart based on the session key
    cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the product already exists in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If it's a new item, set the price
        cart_item.price = product.price
        cart_item.save()

    return redirect('cart:view_cart')  # Redirect to the cart view

def view_cart(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(session_key=session_key).first()

    if cart:
        items = cart.items.all()
        total_price = sum(item.price * item.quantity for item in items)
    else:
        items = []
        total_price = 0

    return render(request, 'cart/view_cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

def remove_from_cart(request, cart_item_id):
    try:
        # Get the CartItem object by ID
        cart_item = CartItem.objects.get(id=cart_item_id)
        
        # Delete the item from the cart
        cart_item.delete()
        
        # Redirect back to the cart view
        return redirect('cart:view_cart')
    except CartItem.DoesNotExist:
        # If the item doesn't exist, redirect back to the cart
        return redirect('cart:view_cart')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        return render(request, 'An_Apple/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')

def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        WishlistItem.objects.get_or_create(user=request.user, product=product)
        return redirect('wishlist')
    else:
        return redirect('login')

def remove_from_wishlist(request, wishlist_item_id):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id, user=request.user)
        wishlist_item.delete()
        return redirect('wishlist')
    else:
        return redirect('login')

def contact(request):
    return render(request, 'An_Apple/contact.html')

def product_filter(request):
    products = Product.objects.all()
    condition = request.GET.getlist('condition')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if condition:
        products = products.filter(condition__in=condition)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'An_Apple/product_filter.html', {'products': products})

@login_required
def checkout(request):
    cart = Cart(request)
    cart_items = list(cart)  # Convert generator to list for reuse
    cart_total = cart.get_total_price()
    
    if request.method == 'POST' and request.FILES.get('proof_of_payment'):
        proof_of_payment = request.FILES['proof_of_payment']
        # Handle proof of payment logic here
        
        return HttpResponse("Proof of payment submitted successfully.")
    
    return render(request, 'An_Apple/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    }) 

@csrf_exempt
def checkout_view(request):
    if request.method == 'POST':
        cart_data = json.loads(request.body)
        request.session['cart_data'] = cart_data  # Save cart data in the session
        return redirect('checkout')

    # Retrieve cart data from session for display
    cart_data = request.session.get('cart_data', {})
    return render(request, 'checkout.html', {'cart_data': cart_data})

def send_payment_email(user_email, cart_items, cart_total, file_url):
    subject = 'Apple eStore - Payment Confirmation'
    message = f"Dear {user_email},\n\nThank you for your purchase!\n\nOrder Details:\n"
    
    for item in cart_items:
        message += f"{item['product'].name} - {item['quantity']} x ${item['product'].price} = ${item['total_price']}\n"
    
    message += f"\nTotal Amount: ${cart_total}\n\nProof of Payment: {file_url}"
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

def send_whatsapp_message(file_path, to_number):
    client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
    
    # Send a message with the PDF as an attachment
    message = client.messages.create(
        body="Payment Proof and Order Details",
        from_="whatsapp:+14155238886",  # Twilio WhatsApp sandbox number
        to=f"whatsapp:{to_number}",
        media_url=[file_path]
    )

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page or wherever you'd like
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})