import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models, helper


@login_required(login_url='login')
def checkouts(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    if user.role != "Cashier":
        messages.info(request, "Access Restricted")
        return redirect('home')
    else:
        all_checkouts = models.CashierCart.objects.filter(domain=shop.domain).order_by('cart_reference', 'created_at').distinct('cart_reference')
        all_c = models.CashierCart.objects.filter(domain=shop.domain)
        total = 0
        for i in all_c:
            print(i.total_price)
            total += i.total_price
        print(total)

        context = {
            'checkouts': all_checkouts,
            'shop_name': f"{shop.name} (Cashier Portal)",
            'total': total
        }
        return render(request, 'layouts/checkouts.html', context=context)


@login_required(login_url='login')
def checkout_details(request, ref):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    items = models.CashierCart.objects.filter(cart_reference=ref, domain=shop.domain)
    item = items.first()
    visited = item.visited
    date = datetime.datetime.now()

    total = 0

    for i in items:
        total += i.total_price

    context = {
        'shop_name': f"{shop.name} (Cashier Portal)",
        'shop': shop,
        'items': items,
        'ref': ref,
        'date': date,
        'total': total,
        'visited': visited
    }

    return render(request, "layouts/checkout_details.html", context=context)


@login_required(login_url='login')
def send_to_cashier(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)

    cart_items = models.Cart.objects.filter(user=user, domain=shop.domain)
    new_reference = helper.ref_generator(shop.shop_receipt_generation_prefix)

    for item in cart_items:
        print(item.cart_reference)
        new_cashier_cart_item = models.CashierCart.objects.create(
            user=models.CustomUser.objects.get(role="Cashier", domain=shop.domain),
            cart_reference=new_reference,
            product=item.product,
            domain=shop.domain,
            product_qty=item.product_qty,
            unit_price=item.unit_price,
            total_price=item.total_price,
        )
        new_cashier_cart_item.save()
    cart_items.delete()
    messages.info(request, f"Sent to Cashier. Checkout reference is #{new_reference}")
    return redirect('home')


@login_required(login_url='login')
def delete_checkout(request, ref):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    if user.role != "Cashier":
        messages.success(request, "Access Denied")
        return redirect("home")
    else:
        checkout_to_be_deleted = models.CashierCart.objects.filter(domain=shop.domain, cart_reference=ref)
        if checkout_to_be_deleted:
            checkout_to_be_deleted.delete()
            messages.info(request, "Checkout deleted")
            return redirect('checkouts')
        else:
            messages.info(request, "No checkout matching this reference was found")
            return redirect('checkouts')


@login_required(login_url='login')
def save_details(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        amount_paid = request.POST.get("amount_paid")
        mode = request.POST.get("mode")
        ref = request.POST.get("ref")
        balance = request.POST.get("balance")
        discount = request.POST.get("discount")

        if models.DaySaleOrder.objects.filter(sale_reference=ref, domain=shop.domain).exists():
            messages.success(request, "Sale already exists. Moving on to printing")
            print("already exists")
            return JsonResponse({'status': "Done"})

        cashier_cart_items = models.CashierCart.objects.filter(cart_reference=ref, domain=shop.domain)
        total = 0
        for i in cashier_cart_items:
            total += i.total_price

        print(name)
        print(contact)
        print(amount_paid)
        print(mode)
        print(balance)
        print(discount)

        new_day_sale_order = models.DaySaleOrder()
        new_day_sale_order.domain = shop.domain
        new_day_sale_order.customer_name = name
        new_day_sale_order.customer_phone = contact
        new_day_sale_order.total_price = total
        new_day_sale_order.discount = discount
        new_day_sale_order.balance = balance
        new_day_sale_order.amount_paid = amount_paid
        new_day_sale_order.sale_reference = ref
        new_day_sale_order.user = request.user
        new_day_sale_order.payment_mode = mode

        new_day_sale_order.save()


        for item in cashier_cart_items:
            print("saving")
            new_day_sale = models.DaysSale.objects.create(
                domain=shop.domain,
                sale=new_day_sale_order,
                product=item.product,
                sale_reference=ref,
                quantity=item.product_qty,
                price=item.unit_price,
                total_price=item.product_qty * item.unit_price
            )
            order_sale = models.Product.objects.get(id=item.product.id)
            order_sale.quantity_available -= item.product_qty
            order_sale.save()
            new_day_sale.save()

            item.visited = True
            item.save()
        print("done")
        messages.success(request, "Saved")
        return JsonResponse({'status': 'Done'})

