from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            # If no cart exists, initialize an empty cart
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def save(self):
        # Ensure the session is marked as modified so the cart is saved
        self.session.modified = True

    def __iter__(self):
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            item['product'] = product
            item['total_price'] = item['quantity'] * product.price
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['quantity'] * item['price'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True
