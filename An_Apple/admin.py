from django.contrib import admin
from django.db import models
from .models import Cart, CartItem, Product, WishlistItem

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'original_price', 'is_featured')
    list_filter = ('product_type', 'is_featured')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
