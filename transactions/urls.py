from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

# Import views
from django.views.generic import TemplateView
from .views import (search_idvend, display_transactions,
                    get_idvend_transactions, search_invoice_id, post_transactions)


app_name = 'transactions'
urlpatterns = [
    path('', display_transactions, name='transactions'),
    path('history', TemplateView.as_view(template_name='transactions/trans-history.html'), name='trans-history'),
    path('search/', search_idvend, name='search-description'),
    path('get-vendor-transactions/', get_idvend_transactions, name='get-vendor-transactions'),
    path('search-invoices/', search_invoice_id, name='search-invoices'),
    path('post-transactions/', post_transactions, name='post-transactions'),
]

urlpatterns += staticfiles_urlpatterns()