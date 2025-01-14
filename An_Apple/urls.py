from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('account/', views.account, name='account'),
    path('register/', views.register, name='register'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view/', views.view_cart, name='view_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product_filter, name='product_filter'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:  # Only serve static files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
