from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .filter import ProductFilter
from .models import Category, Product
from users.models import Customer, User
from orders.models import Order
from cart.forms import CartAddProductForm
from .forms import ProductForm, CategoryForm, RFQForm


def home(request):
    if request.user.is_staff:
        return redirect('products:employee_home')
    elif request.user.username:
        return redirect('products:product_list')
    else:
        return redirect('users:home')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs
    return render(request,
                  'buildingsupply/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'productFilter': productFilter})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    user = request.user
    cart_product_form = CartAddProductForm()
    return render(request,
                  'buildingsupply/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'user': user})


@staff_member_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)

            product.save()

            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'buildingsupply/product_new.html', {'form': form})


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            product.updated = timezone.now()
            product.save()

            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'buildingsupply/product_edit.html', {'form': form})


@staff_member_required
def category_list_emp(request):
    categories = Category.objects.all()
    return render(request, 'buildingsupply/categories_list.html',
                  {'categories': categories})


@staff_member_required
def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('products:category_list')
    else:
        form = CategoryForm()
    return render(request, 'buildingsupply/category_new.html', {'form': form})


@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            category.save()
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'buildingsupply/category_edit.html', {'form': form,
                                                                 'pk': pk})


@staff_member_required
def employee_home(request):
    categoryCount = str(Category.objects.all().count())
    productsCount = str(Product.objects.all().count())
    customerCount = str(Customer.objects.all().count())
    orderCount = str(Order.objects.all().count())
    context = {"categoryCount": categoryCount,
               "productsCount": productsCount,
               "customerCount": customerCount,
               "orderCount": orderCount}

    return render(request, 'buildingsupply/employee_home.html', {'context': context})


def category_list(request):
    categories = Category.objects.all()
    context = {

        "categories": categories,
    }
    return context


@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect('products:category_list_emp')
    return render(request, 'buildingsupply/category_delete.html', {'category': category})


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('products:product_list')
    return render(request, 'buildingsupply/product_delete.html', {'product': product})


def RFQ(request):
    form = RFQForm(request.POST, request.FILES)
    if form.is_valid():

        form.save()
        return render(request, 'buildingsupply/request_done.html')

    else:
        form = RFQForm()

    return render(request, 'buildingsupply/RFQ.html', {'form': form})
