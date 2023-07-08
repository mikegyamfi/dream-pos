import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models


@login_required(login_url='login')
def checkouts(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    if user.role != "Cashier":
        messages.info(request, "Access Restricted")
        return redirect('home')
    else:
        all_checkouts = models.CashierCart.objects.filter(domain=shop.domain).order_by('cart_reference', 'created_at').distinct('cart_reference')
        context = {
            'checkouts': all_checkouts,
            'shop_name': f"{shop.name} (Cashier Portal)",
        }
        return render(request, 'layouts/checkouts.html', context=context)


@login_required(login_url='login')
def checkout_details(request, ref):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)
    items = models.CashierCart.objects.filter(cart_reference=ref)
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
        'total': total
    }

    return render(request, "layouts/checkout_details.html", context=context)


@login_required(login_url='login')
def send_to_cashier(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    shop = models.StoreInfo.objects.get(domain=user.domain)

    cart_items = models.Cart.objects.filter(user=user, domain=shop.domain)

    for item in cart_items:
        new_cashier_cart_item = models.CashierCart.objects.create(
            user=models.CustomUser.objects.get(role="Cashier", domain=shop.domain),
            cart_reference=item.cart_reference,
            product=item.product,
            domain=shop.domain,
            product_qty=item.product_qty,
            unit_price=item.unit_price,
            total_price=item.total_price,
        )
        new_cashier_cart_item.save()
    cart_items.delete()
    messages.info(request, "Sent to Cashier")
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
        else:
            messages.info(request, "No checkout matching this reference was found")
            return redirect(checkouts)


