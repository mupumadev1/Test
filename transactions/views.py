from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Transactions, Vendors


def display_transactions(request):
    if request.method == 'GET':
        try:
            transactions = Transactions.objects.values('idbank', 'idvend', 'datermit', 'amtpaym', 'paymcode', 'codecurn', 'rateexchhc')[:10]
            return render(request, 'transactions/dashboard.html', {'transactions': transactions})
        except Exception as e:
            print(e)
            return render(request, 'transactions/dashboard.html', {'transactions': []})

# Search by idvend and return JSON response if found
def search_idvend(request):
    if request.method == 'GET':
        try:
            vendor_id = request.GET.get('vendor_id')
            vendor_ids = Transactions.objects.filter(idvend__icontains=vendor_id).values('idvend')[:5]
            return JsonResponse(list(vendor_ids), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse([], safe=False)
        
# Search by idvend and return JSON response if found
def get_idvend_transactions(request):
    if request.method == 'GET':
        try:
            vendor_id = request.GET.get('vendor_id')
            transactions = Transactions.objects.filter(idvend=vendor_id).values('idbank', 'idvend', 'datermit', 'amtpaym', 'paymcode', 'codecurn', 'rateexchhc')[:10]
            return JsonResponse(list(transactions), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse([], safe=False)
