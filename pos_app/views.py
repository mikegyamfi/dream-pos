from datetime import datetime
from itertools import groupby
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . import forms, models, helper


# Create your views here.
@login_required(login_url='login')
def home(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    if request.method == "POST":
        customer_phone = request.POST.get("customer-phone")
        customer_name = request.POST.get("customer-name")
        amount_paid = request.POST.get("customer-amount")
        if amount_paid != "":
            amount_paid = float(amount_paid)
        else:
            amount_paid = 0
        cart_items = models.Cart.objects.filter(domain=shop.domain)
        sales = []
        sale_ref = helper.ref_generator(shop.name)
        for item in cart_items:
            new_day_sale = models.DaysSale.objects.create(
                user=request.user,
                customer_name=customer_name,
                customer_phone=customer_phone,
                amount_paid=amount_paid,
                balance=amount_paid - (item.product_qty * item.product.price),
                sale_reference=sale_ref,
                product=item.product,
                quantity=item.product_qty,
                price=item.product.price,
                total_price=item.product_qty * item.product.price,
                domain=shop.domain
            )
            sales.append(new_day_sale)
            item.product.quantity_available -= item.product_qty
            item.product.save()
        for sale in sales:
            if sale.balance < 0:
                sale.balance = 0
            sale.save()
        cart_items.delete()
        messages.success(request, "Items sold")
        new_timeline = models.Timeline.objects.create(
            user=request.user,
            domain=shop.domain,
            activity="Sold items"
        )
        new_timeline.save()
        if customer_name == '' or customer_phone == '':
            return redirect('invoice', sale_reff=sales[0].sale_reference, name="Null", phone="Null", amount_paid=amount_paid)
        return redirect('invoice', sale_reff=sales[0].sale_reference, name=customer_name, phone=customer_phone, amount_paid=amount_paid)
    products = models.Product.objects.filter(domain=user.domain).order_by('name')
    day_sales = models.DaysSale.objects.filter(domain=user.domain)
    cart = models.Cart.objects.filter(domain=user.domain)
    cart_count = models.Cart.objects.filter(domain=user.domain).count()
    total = 0
    shop_total = 0
    day_total = 0
    for item in cart:
        total += item.product_qty * item.product.price

    for product in products:
        shop_total += product.quantity_available * product.price

    for sale in day_sales:
        day_total += sale.total_price
    context = {
        'products': products,
        'cart_items': cart,
        'count': cart_count,
        'cart_total': total,
        'shop_total': '{:,.2f}'.format(shop_total),
        'day_total': day_total,
        'shop_name': shop_name
    }

    return render(request, "layouts/index.html", context=context)


def sign_up(request):
    form = forms.CustomUserForm()
    if request.method == "POST":
        form = forms.CustomUserForm(request.POST)
        code = int(request.POST.get("code"))
        shop_exists = models.StoreInfo.objects.filter(code=code).exists()
        if not shop_exists:
            messages.warning(request, "Invalid Authorization Code. Contact Admin")
            return redirect('signup')
        shop = models.StoreInfo.objects.get(code=code)
        if form.is_valid():
            print("true")
            domain = shop.domain
            print("why")
            username = form.cleaned_data["username"]
            new_username = f"{username}@{domain}"
            form.save()
            user = models.CustomUser.objects.get(username=username)
            user.username = new_username
            user.domain = domain
            user.save()
            messages.info(request, f"Sign Up Successful. Your new username is {new_username} NB: Log in with that as your username")
            return redirect('login')
        else:
            print("nope")
    context = {'form': form}
    return render(request, "auth/sign-up.html", context=context)


def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('pass')

            print(name)
            print(password)

            user = authenticate(request, username=name, password=password)
            print(user)
            if user:
                login(request, user)
                messages.success(request, 'Log in Successful')
                return redirect('home')
            else:
                print("here")
                messages.info(request, 'Invalid username or password')
                return redirect('login')
    return render(request, "auth/login.html")


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    messages.success(request, "Log out successful")
    return redirect('home')


@login_required(login_url='login')
def add_product(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    form = forms.AddProductForm(domain=shop.domain)
    if request.method == "POST":
        form = forms.AddProductForm(domain=shop.domain, data=request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            name = form.cleaned_data["name"]
            price = form.cleaned_data["price"]
            quantity = form.cleaned_data["quantity"]
            size = form.cleaned_data["size"]

            print(category)
            print(name)
            print(price)
            print(quantity)

            if models.Product.objects.filter(name=name, size=size, category=category).exists():
                messages.warning(request, "Product already exists.")
                return redirect('add_product')

            new_product = models.Product.objects.create(
                user=request.user,
                domain=shop.domain,
                category=category,
                name=name,
                price=price,
                quantity_available=quantity,
                size=size
            )

            new_product.save()
            new_timeline = models.Timeline.objects.create(
                user=request.user,
                domain=shop.domain,
                activity=f"Added {name} {size} to stock"
            )
            new_timeline.save()
            messages.success(request, "Product Saved")
            return redirect('add_product')
    context = {'form': form, 'shop_name': shop_name}
    return render(request, "layouts/add_product.html", context=context)


@login_required(login_url='login')
def add_category(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    form = forms.AddCategoryForm()
    if request.method == "POST":
        form = forms.AddCategoryForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]

            new_category = models.Category.objects.create(
                user=request.user,
                name=name,
                description=description,
                domain=shop.domain
            )
            new_category.save()
            new_timeline = models.Timeline.objects.create(
                user=request.user,
                domain=shop.domain,
                activity=f"Added new category - {name}"
            )
            new_timeline.save()
            messages.success(request, "Category Saved")
            return redirect("add_category")
    context = {'form': form, 'shop_name': shop_name}
    return render(request, "layouts/add_category.html", context=context)


@login_required(login_url='login')
def product_list(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    all_products = models.Product.objects.filter(domain=shop.domain).order_by('name')
    total = 0
    out_of_stock_count = 0
    for prod in all_products:
        total += prod.quantity_available * prod.price
        if prod.quantity_available == 0:
            out_of_stock_count += 1
    context = {'products': all_products, 'shop_total': '{:,.2f}'.format(total), 'out': out_of_stock_count, 'shop_name': shop_name}
    return render(request, "layouts/product_list.html", context=context)


@login_required(login_url='login')
def edit_product(request, pk):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    product_to_be_edited = models.Product.objects.filter(id=pk, domain=shop.domain).first()
    print(product_to_be_edited.name)
    form = forms.EditProductForm(
        domain=shop.domain,
        initial={
            'category': product_to_be_edited.category,
            'name': product_to_be_edited.name,
        }
    )
    if request.method == "POST":
        form = forms.EditProductForm(domain=shop.domain, data=request.POST)
        if form.is_valid():
            product_to_be_edited.category = form.cleaned_data["category"]
            product_to_be_edited.name = form.cleaned_data["name"]
            product_to_be_edited.user = request.user
            product_to_be_edited.save()

            new_timeline = models.Timeline.objects.create(
                user=request.user,
                domain=shop.domain,
                activity=f"{product_to_be_edited} was edited"
            )
            new_timeline.save()

            messages.success(request, "Product Edited Successfully")
            return redirect("product_list")
    context = {'form': form, 'product': product_to_be_edited, 'shop_name': shop_name}
    return render(request, "layouts/edit_product.html", context=context)


@login_required(login_url='login')
def restock_product(request, pk):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    product_to_be_stocked = models.Product.objects.filter(id=pk, domain=shop.domain).first()
    print(product_to_be_stocked.name)
    form = forms.RestockProductForm(
        domain=shop.domain,
        initial={
            'category': product_to_be_stocked.category,
            'name': product_to_be_stocked.name,
            'quantity': product_to_be_stocked.quantity_available,
            'price': product_to_be_stocked.price
        }
    )
    if request.method == "POST":
        form = forms.RestockProductForm(domain=shop.domain, data=request.POST)
        if form.is_valid():
            product_to_be_stocked.category = form.cleaned_data["category"]
            product_to_be_stocked.name = form.cleaned_data["name"]
            product_to_be_stocked.price = form.cleaned_data["price"]
            product_to_be_stocked.quantity_available = form.cleaned_data["quantity"]
            product_to_be_stocked.user = request.user
            product_to_be_stocked.save()

            new_restock_history = models.RestockHistory.objects.create(
                user=request.user,
                product=product_to_be_stocked,
                quantity=form.cleaned_data["quantity"],
                domain=shop.domain,
                price=form.cleaned_data["price"]
            )

            new_restock_history.save()

            new_timeline = models.Timeline.objects.create(
                user=request.user,
                domain=shop.domain,
                activity=f"{product_to_be_stocked} was restocked"
            )
            new_timeline.save()

            messages.success(request, "Product Restocked Successfully")
            return redirect("product_list")
    context = {'form': form, 'product': product_to_be_stocked, 'shop_name': shop_name}
    return render(request, "layouts/restock.html", context=context)


@login_required(login_url='login')
def delete_product(request, pk):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    product_to_be_deleted = models.Product.objects.filter(id=pk, domain=shop.domain).first()
    product_to_be_deleted.delete()
    new_timeline = models.Timeline.objects.create(
        user=request.user,
        domain=shop.domain,
        activity=f"{product_to_be_deleted} was deleted."
    )
    new_timeline.save()
    messages.success(request, "Product deleted successfully")
    return redirect('product_list')


@login_required(login_url='login')
def add_to_cart(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    if request.method == "POST":
        print("got here")
        pk = request.POST.get('product_id')
        product_to_be_added_to_cart = models.Product.objects.filter(id=pk, domain=shop.domain).first()
        if product_to_be_added_to_cart.quantity_available <= 0:
            return JsonResponse({'status': 'Product is out of stock', 'icon': 'error'})
        if models.Cart.objects.filter(product=product_to_be_added_to_cart, domain=shop.domain).exists():
            cart_item = models.Cart.objects.filter(product=product_to_be_added_to_cart, domain=shop.domain).first()
            new_quantity = cart_item.product_qty + 1
            if new_quantity > product_to_be_added_to_cart.quantity_available:
                return JsonResponse({'status': 'More of the product is not available', 'icon': 'warning()'})
            cart_item.product_qty += 1
            cart_item.total_price = product_to_be_added_to_cart.price * new_quantity
            cart_item.save()
            return JsonResponse({'status': 'Quantity Updated', 'icon': ''})
        new_cart_object = models.Cart.objects.create(
            product=product_to_be_added_to_cart,
            product_qty=1,
            unit_price=product_to_be_added_to_cart.price,
            total_price=product_to_be_added_to_cart.price,
            domain=shop.domain
        )
        new_cart_object.save()
        return JsonResponse({'status': 'Product Added to Cart', 'icon': ''})


@login_required(login_url='login')
def sell_items(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    cart_items = models.Cart.objects.filter(domain=shop.domain)
    sales = []
    sale_ref = helper.ref_generator(shop.name)
    for item in cart_items:
        new_day_sale = models.DaysSale.objects.create(
            user=request.user,
            sale_reference=sale_ref,
            product=item.product,
            quantity=item.product_qty,
            price=item.product.price,
            total_price=item.product_qty * item.product.price,
            domain=shop.domain
        )
        sales.append(new_day_sale)
        item.product.quantity_available -= item.product_qty
        item.product.save()
    for sale in sales:
        sale.save()
    cart_items.delete()
    messages.success(request, "Items sold")
    return redirect('invoice', sale_reff=sales[0].sale_reference)


def invoice(request, sale_reff, name, phone, amount_paid):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    customer_goods = models.DaysSale.objects.filter(domain=user.domain, sale_reference=sale_reff)

    total = 0

    for item in customer_goods:
        total += item.total_price

    balance = 0

    if amount_paid == '0':
        balance = 0
    else:
        balance = float(amount_paid) - total

    context = {
        'shop_name': shop.name,
        'items': customer_goods,
        'date': datetime.now(),
        'total': total,
        'num': sale_reff,
        'name': name,
        'phone': phone,
        'amount_paid': amount_paid,
        'balance': balance
    }

    return render(request, "layouts/invoice.html", context=context)


@login_required(login_url='login')
def days_sales(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    sales_for_the_day = models.DaysSale.objects.filter(domain=shop.domain).order_by('date_created').reverse()
    total = 0
    days_sales_list = []
    for sale in sales_for_the_day:
        total += sale.total_price
    if request.method == "POST":
        for sale in sales_for_the_day:
            new_general_sale = models.SoldItem.objects.create(
                sale_reference=sale.sale_reference,
                user=request.user,
                domain=shop.domain,
                customer_name=sale.customer_name,
                customer_phone=sale.customer_phone,
                amount_paid=sale.amount_paid,
                balance=sale.balance,
                product=sale.product,
                quantity=sale.quantity,
                price=sale.price,
                total_price=sale.total_price,
                closed_date=datetime.today().date()
            )
            days_sales_list.append(new_general_sale)
        for sale in days_sales_list:
            sale.save()
        sales_for_the_day.delete()
        today_date = datetime.now().date()
        new_day_sale = models.IndividualDaySale.objects.create(
            total_sales=total,
            domain=shop.domain
        )
        new_day_sale.save()
        new_timeline = models.Timeline.objects.create(
            user=request.user,
            domain=shop.domain,
            activity=f"Sale was closed for {today_date}"
        )
        new_timeline.save()
        messages.success(request, f"Sales for the day closed. Total Sales for {today_date}: ₵{total}")
        return redirect('sales_for_the_day')
    context = {'sales': sales_for_the_day, 'total': '{:,.2f}'.format(total), 'count': sales_for_the_day.count(), 'shop_name': shop_name}
    return render(request, "layouts/products_sold.html", context=context)


@login_required(login_url='login')
def all_sales(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    all_sales_items = models.SoldItem.objects.filter(domain=shop.domain).order_by('date_created').reverse()
    total = 0
    for sale in all_sales_items:
        total += sale.total_price

    context = {'sales': all_sales_items, 'total': '{:,.2f}'.format(total), 'shop_name': shop_name}
    return render(request, "layouts/all_sales.html", context=context)


@login_required(login_url='login')
def individual_sales(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    shop_name = shop.name
    individual_sales_items = models.IndividualDaySale.objects.filter(domain=shop.domain).order_by('day').reverse()
    total = 0
    for sale in individual_sales_items:
        total += sale.total_sales
    context = {'sales': individual_sales_items, 'total': '{:,.2f}'.format(total), 'shop_name': shop_name}
    return render(request, "layouts/ind.html", context=context)


@login_required(login_url='login')
def check_sale(request, pk):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    day_to_be_checked = models.IndividualDaySale.objects.filter(id=pk, domain=shop.domain).first()
    money = day_to_be_checked.total_sales
    if day_to_be_checked.checked:
        messages.warning(request, "Day has been checked already")
        return redirect('everyday_sales')
    day_to_be_checked.checked = True
    day_to_be_checked.save()
    new_timeline = models.Timeline.objects.create(
        user=request.user,
        domain=shop.domain,
        activity=f"{day_to_be_checked} sales was checked successfully."
    )
    new_timeline.save()
    messages.success(request, f"Sales checked successfully. GHS{money} received.")
    return redirect('everyday_sales')


@login_required(login_url='login')
def delete_cart_item(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    if request.method == "POST":
        pk = request.POST.get('product_id')
        product_to_be_deleted = models.Cart.objects.filter(pk=pk, domain=shop.domain).first()
        if product_to_be_deleted.product_qty > 1:
            quantity = product_to_be_deleted.product_qty
            product_to_be_deleted.product_qty -= 1
            product_to_be_deleted.total_price = product_to_be_deleted.unit_price * (quantity - 1)
            product_to_be_deleted.save()
            return JsonResponse({'status': "Quantity reduced by 1"})
        product_to_be_deleted.delete()
        return JsonResponse({'status': "Item deleted"})


@login_required(login_url='login')
def out_of_stock(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    products_out_of_stock = models.Product.objects.filter(quantity_available=0)
    context = {
        'products': products_out_of_stock,
        'shop_name': shop.name
    }
    return render(request, "layouts/out.html", context=context)


def restock_history(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    restock_history_items = models.RestockHistory.objects.filter(domain=shop.domain).order_by('restock_date').reverse()

    context = {
        'items': restock_history_items,
        'shop_name': shop.name
    }

    return render(request, "layouts/restock_history.html", context=context)


def timeline(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)

    timeline_items = models.Timeline.objects.filter(domain=shop.domain).order_by('time').reverse()

    context = {
        'shop_name': shop.name,
        'timelines': timeline_items
    }

    return render(request, "layouts/timeline.html", context=context)


def not_found_404_page(request, exception):
    return render(request, "404.html")


