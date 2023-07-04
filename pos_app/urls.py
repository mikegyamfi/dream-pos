from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('add_product', views.add_product, name='add_product'),
    path('product_list', views.product_list, name='product_list'),
    path('edit_product/<int:pk>', views.edit_product, name='edit_product'),
    path('out_of_stock', views.out_of_stock, name='out_of_stock'),
    path('restock_product/<int:pk>', views.restock_product, name='restock_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),

    path('sell_items/', views.sell_items, name='sell_items'),
    path('day_s_sales/', views.days_sales, name='sales_for_the_day'),
    path('all_sales', views.all_sales, name='all_sales'),
    path('everyday_sales', views.individual_sales, name='everyday_sales'),
    path('check_sales/<int:pk>', views.check_sale, name='check_sale'),
    path('invoice/<str:sale_reff>/<str:name>/<str:phone>/<str:amount_paid>/<str:mode>', views.invoice, name='invoice'),
    path('restock_history', views.restock_history, name='restock_history'),
    path('timeline', views.timeline, name='timeline'),

    path('add_category', views.add_category, name='add_category'),

    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('sign_up', views.sign_up, name='signup'),

    path('shop_info', views.shop_info, name='shop_info'),

    path('google272847792544ccb7.html', views.verification, name='google272847792544ccb7.html')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


