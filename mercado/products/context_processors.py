from .models import Cart, CartItem

def cart_context(request):
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items_count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            pass
    return {'cart_items_count': cart_items_count}