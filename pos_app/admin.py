from django.contrib import admin

from pos_app import models


class DaysSaleAdmin(admin.ModelAdmin):
    list_display = ['domain', 'sale', 'product', 'quantity', 'price', 'total_price', 'date_created']


class SoldItemAdmin(admin.ModelAdmin):
    list_display = ['domain', 'product', 'quantity', 'price', 'total_price', 'closed_date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['domain', 'name', 'category', 'price', 'quantity_available', 'size']


class IndividualDaySaleAdmin(admin.ModelAdmin):
    list_display = ['domain', 'day', 'total_sales', 'checked']


class StoreInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'code']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart_reference', 'domain', 'product', 'product_qty']


class CashierCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart_reference', 'domain', 'product', 'product_qty']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['domain', 'name']


# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.DaysSale, DaysSaleAdmin)
admin.site.register(models.SoldItem, SoldItemAdmin)
admin.site.register(models.IndividualDaySale, IndividualDaySaleAdmin)
admin.site.register(models.StoreInfo, StoreInfoAdmin)
admin.site.register(models.RestockHistory)
admin.site.register(models.Timeline)
admin.site.register(models.CashierCart, CashierCartAdmin)
admin.site.register(models.DaySaleOrder)
admin.site.register(models.SoldOrder)
