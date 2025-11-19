from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from .models import Product, Cart, CartItem
from .forms import ProductForm
import json
import mercadopago


#home
def home(request):
    products = Product.objects.all().order_by('-created_at')[:6]
    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()

    return render(request, 'products/home.html', {
        'products': products,
        'cart_item_count' : cart_item_count
        })

#mis productos
@login_required
def my_products(request):
    products_list = Product.objects.filter(user=request.user).order_by('id')
    paginator = Paginator(products_list, 5)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item_count = sum(item.quantity for item in cart.items.all())
        
    return render(request, 'products/my_products.html', {
        'products': products,
        'cart_item_count' : cart_item_count
    })

#create product
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products:list')
    else:
        form = ProductForm()
    return render(request, 'products/create.html', {'form':form})

@require_http_methods(["POST"])
@login_required
def create_product_ajax(request):
    """Vista para crear un producto vía AJAX."""
    if request.method == 'POST' and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            name = request.POST.get("name")
            price = request.POST.get("price")
            description = request.POST.get("description")
            stock = request.POST.get("stock")
            image = request.FILES.get("image")

            if not name or not price:
                return JsonResponse({"success": False, "error": "Nombre y precio son obligatorios."})
            try:
                price = float(price)
                if price < 0:
                    return JsonResponse({"success": False, "error": "El precio debe ser positivo."})
                stock = int(stock) if stock else 0
                if stock < 0:
                    return JsonResponse({"success": False, "error": "El stock no puede ser negativo."})
            except (ValueError, TypeError):
                return JsonResponse({"success": False, "error": "Precio o stock inválidos."})
            
            product = Product.objects.create(
                user=request.user,
                name=name,
                price=price,
                description=description,
                stock=stock,
                image=image
            )

            products = Product.objects.filter(user=request.user).order_by('-id')
            html = render_to_string("products/my_products_list.html", {"products": products}, request=request)

            return JsonResponse({"success": True, "products_html": html})
        except Exception as e:
            import traceback
            print("Error en create_product_ajax:", str(e))
            print(traceback.format_exc())
            return JsonResponse({"success": False, "error": f"Error interno: {str(e)}"})
    return JsonResponse({"success": False, "error": "Solicitud inválida."})

#Edit product
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit.html', {'form': form, 'product': product})

@require_http_methods(["POST"])
@login_required
def edit_product_ajax(request, pk):
    """Vista para editar un producto vía AJAX."""
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            products = Product.objects.filter(user=request.user)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item_count = sum(item.quantity for item in cart.items.all())

            html = render_to_string('products/my_products_list.html', {
                'products': products,
                'cart_item_count': cart_item_count
            }, request=request)

            return JsonResponse({
                'success': True,
                'html': html
            })
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})

#Delete product
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('products:my_products')
    return redirect('products:my_products')

#scraping
def compare_products(request):
    products = Product.objects.all()
    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()
    return render(request, 'products/compare.html', {
        'products': products,
        'cart_item_count': cart_item_count
    })


#agregar al Carrito
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('products:home')

@require_http_methods(["POST"])
@login_required
def add_to_cart_ajax(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({
        "success": True,
        "message": f"{product.name} agregado al carrito",
        "cart_count": cart.items.count()
    })

#Borrar del carrito
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('products:view_cart')

#Abrir carrito
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.get_total_price() for item in items)
    return render(request, 'products/cart.html', {'items': items, 'total': total})

#Numerito del carrito
def cart_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = cart.items.count()
    else:
        count = 0
    return JsonResponse({'count': count})

#modal items del carrito
@login_required
def get_cart_items(request):
    """vista para devolver los items del carrito como HTML parcial"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.get_total_price() for item in items)
    cart_html = render_to_string('products/cart_dropdown_items.html', {'items': items, 'total': total}, request=request)

    return JsonResponse({
        'html': cart_html,
        'count': sum(item.quantity for item in items)
    })

#Para aumentar el numero de un product en el carrito
@login_required
@require_http_methods(["POST"])
def update_cart_item_quantity(request, item_id):
    try:
        data = json.loads(request.body)
        quantity_change = data.get('quantity_change', 0)
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        product = cart_item.product

        try:
            quantity_change = int(quantity_change)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Cantidad inválida'}, status=400)

        new_quantity = cart_item.quantity + quantity_change

        if new_quantity > product.stock:
            return JsonResponse({
                'success': False,
                'error': f'No hay suficiente stock. Solo hay {product.stock} unidades disponibles'
            }, status=400)

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            final_quantity = cart_item.quantity
        else:
            cart_item.delete()
            final_quantity = 0
            

        cart, created = Cart.objects.get_or_create(user=request.user)
        new_total = sum(item.get_total_price() for item in cart.items.all())
        new_count = sum(item.quantity for item in cart.items.all())
        
        return JsonResponse({
            'success': True,
            'new_count': new_count,
            'new_total': float(new_total),
            'new_quantity': final_quantity,
            'product_stock': product.stock
        })
    #para ver errores
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    except Exception as e:
        print(f"Error en update_cart_item_quantity: {e}")
        return JsonResponse({'success': False, 'error': 'Error interno del servidor'}, status=500)


#Vista para mercadopago
@login_required
def create_preference(request):
    """Vista para crear una preferencia de pago en MP"""
    if request.method == 'POST':
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()

            if not cart_items:
                return JsonResponse({'error': 'El carrito está vacio'}, status=400)

            if not hasattr(mercadopago, 'SDK'):
                raise Exception("SDK de Mercado Pago no disponible")

            access_token = settings.MERCADOPAGO_ACCESS_TOKEN
            if not access_token:
                raise Exception("Access Token de Mercado Pago no configurado")
            
            sdk = mercadopago.SDK(access_token)

            # Preparar los prodcuts
            items = []
            for cart_item in cart_items:
                try:
                    unit_price = float(cart_item.product.price)
                except (ValueError, TypeError):
                    unit_price = 0.0

                items.append({
                    "id": str(cart_item.product.id),
                    "title": cart_item.product.name[:60],
                    "quantity": cart_item.quantity,
                    "unit_price": unit_price,
                    "currency_id": "ARS",
                })

            #preferencia
            preference_data = {
                "items": items,
                "back_urls": {
                    "success": request.build_absolute_uri('/products/payment/success/'),
                    "failure": request.build_absolute_uri('/products/payment/failure/'),
                    "pending": request.build_absolute_uri('/products/payment/pending/'),
                },
                "binary_mode": True,
            }

            print("Creando preferencia con datos:", preference_data)

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            print("Preferencia creada:", preference)

            # Devolver la URL de inicio del checkout
            return JsonResponse({
                'init_point': preference['init_point'],
                'id': preference['id']
            })

        except Exception as e:
            print(f"Error creando preferencia de pago: {e}")
            return JsonResponse({'error': f'Error interno al crear la preferencia de pago: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

#Despues de pagar y sale bien
def payment_success(request):
    #Vacia el carrito
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass
    return HttpResponse("""
        <script>
            alert('¡Gracias por tu compra! Tu pago ha sido procesado exitosamente.');
            window.location.href = '/'; // Redirige al home
        </script>
    """)
#Si el pago male sal
def payment_failure(request):
    return HttpResponse("""
        <script>
            alert('Hubo un problema con tu pago. Inténtalo de nuevo.');
            window.location.href = '/'; // Redirige al home
        </script>
    """)
#si el pago quedo raro
def payment_pending(request):
    return HttpResponse("""
        <script>
            alert('Tu pago está siendo procesado. Te avisaremos cuando esté confirmado.');
            window.location.href = '/'; // Redirige al home
        </script>
    """)


def search_products(request):
    q = request.GET.get('q', '').strip()
    if q == "":
        return JsonResponse({'html': ''})
    products = Product.objects.filter(name__icontains=q)[:10]
    html = render_to_string('products/search_products.html', {
        'products': products
        }, request=request)
    return JsonResponse({'html': html})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    products = Product.objects.exclude(id=product.id)[:8]

    return render(request, 'products/detail.html', {
        'product': product,
        'products': products
    })

def product_list(request):
    products = Product.objects.all()
    nombre = request.GET.get('nombre', '').strip()
    if nombre:
        products = products.filter(name__icontains=nombre)
    orden = request.GET.get('orden')
    if orden == "asc":
        products = products.order_by("price")
    elif orden == "desc":
        products = products.order_by("-price")

    paginator = Paginator(products, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()
    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "cart_item_count": cart_item_count
    }

    return render(request, "products/list.html", context)
