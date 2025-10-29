from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Product
from .forms import ProductForm

def home(request):
    products = Product.objects.all().order_by('-created_at')[:6]
    return render(request, 'products/home.html', {'products':products})

@login_required
def my_products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'products/my_products.html', {'products':products})

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

def list_products(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

def compare_products(request):
    products = Product.objects.all()
    return render(request, 'products/compare.html', {'products': products})


#CRUD de my_products
