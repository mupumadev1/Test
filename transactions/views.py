import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import Transactions, Vendors
from .helpers import format_request_data


def is_ajax(request):
    """ Check if request is an ajax request """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def display_transactions(request):
    """
    Display datermit, idinvc, amtpaym, codecurn, idvend From the transactions 
    table and bsbno, accno, accname From the Vendors table where idvend in transactions table is equal to vendorid 
    in vendors table and pass it to the template as one data structure
    """
    if request.method == 'GET':
        try:
            transaction_info = Transactions.objects.values('idbank', 'idvend', 'datermit', 'amtpaym', 'paymcode',
                                                           'codecurn', 'rateexchhc', 'idinvc').order_by('-datermit',
                                                                                                        '-idvend').all()
            vendor_info = Vendors.objects.values('vendorid', 'bsbno', 'accno', 'accname').all()
            paginator = Paginator(transaction_info, 10)

            page_number = request.GET.get('page')
            type(page_number)
            page_obj = paginator.get_page(page_number)
            return render(request, 'transactions/dashboard.html',
                          {'transaction_info': page_obj, 'vendor_info': vendor_info})
        except Exception as e:
            print(e)
            return render(request, 'transactions/dashboard.html', {'transactions': []}, {'vendors': []})


def search_idvend(request):
    """ Search by idvend and return JSON response if found """
    if request.method == 'GET':
        try:
            vendor_id = request.GET.get('vendor_id')
            vendor_ids = Transactions.objects.filter(idvend__icontains=vendor_id).values('idvend')[:5]
            return JsonResponse(list(vendor_ids), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse([], safe=False)


def search_idinvc(request):
    """ Search by idinvc in Request list and return JSON resposne if found """
    if request.method == 'GET':
        try:
            # Get invoice ids from request
            invoice_ids = request.GET.get('invoice_ids')
            if invoice_ids:
                transactions = Transactions.objects.filter(idinvc__in=invoice_ids).values('idbank', 'idvend',
                                                                                          'datermit', 'amtpaym',
                                                                                          'paymcode', 'codecurn',
                                                                                          'rateexchhc', 'idinvc').all()
                return JsonResponse(list(transactions), safe=False)
            else:
                return JsonResponse({'message': 'No invoice ids provided'}, safe=False)
        except Exception as e:
            print(e)
            message = 'Error: ' + str(e)
            return JsonResponse({'message': message}, safe=False)


def get_idvend_transactions(request):
    """ Search by idvend and return JSON response if found """
    if request.method == 'GET':
        try:
            vendor_id = request.GET.get('vendor_id')
            transaction_info = Transactions.objects.filter(idvend=vendor_id).values('idvend', 'datermit', 'amtpaym',
                                                                                    'codecurn', 'idinvc')[:10]
            vendor_info = Vendors.objects.filter(vendorid=vendor_id).values('vendorid', 'bsbno', 'accno',
                                                                            'accname').all()
            return JsonResponse({'transaction_info': list(transaction_info), 'vendor_info': list(vendor_info)},
                                safe=False)
        except Exception as e:
            print(e)
            return JsonResponse([], safe=False)


def search_idinvc(request):
    """ Search by idinvc in Request list and return JSON resposne if found """
    if request.method == 'POST':
        if is_ajax(request):
            try:
                # Get invoice ids from request
                invoice_ids = format_request_data(request.POST.get('invoice_ids[]'))
                transaction_info = Transactions.objects.filter(idinvc__in=invoice_ids).values(
                    'idbank', 'idvend', 'datermit', 'amtpaym', 'codecurn', 'idinvc').order_by('-datermit',
                                                                                              '-idvend').all()
                vendor_info = Vendors.objects.values('vendorid', 'bsbno', 'accno', 'accname').all()
                return JsonResponse({'transaction_info': list(transaction_info), 'vendor_info': list(vendor_info)},
                                    safe=False)
            except Exception as e:
                print(e)
                message = 'Error: ' + str(e)
                return JsonResponse({'message': message}, safe=False)
        else:
            return JsonResponse({'message': 'Not an ajax request'}, safe=False)
    else:
        return JsonResponse({'message': 'Not a POST request'}, safe=False)


# function to get list of beneficiaries from API endpoint
def get_beneficiaries():
    pass


# Function that receives request of posted transactions and sends them to an api endpoint and returns a response
def post_transactions(request):
    if request.method == 'POST':
        invoice_ids = format_request_data(request.POST.get('invoice_ids[]'))
        transaction_info = Transactions.objects.filter(idinvc__in=invoice_ids).values('idbank', 'idvend', 'amtpaym',
                                                                                      'codecurn').all()
        vendor_ids = [transaction['idvend'] for transaction in transaction_info]
        vendor_info = Vendors.objects.filter(vendorid__in=vendor_ids).values('vendorid', 'bsbno', 'accno',
                                                                             'accname').all()

        # Create a dictionary of vendor ids and their corresponding bsbno, accno, accname, idbank, amtpaym and codecurn
        vendor_dict = {}
        for vendor in vendor_info:
            vendor_dict[vendor['vendorid']] = {'bsbno': vendor['bsbno'], 'accno': vendor['accno'],
                                               'accname': vendor['accname']}
        for transaction in transaction_info:
            if transaction['idvend'] in vendor_dict:
                vendor_dict[transaction['idvend']].update(
                    {'idbank': transaction['idbank'], 'amtpaym': transaction['amtpaym'],
                     'codecurn': transaction['codecurn']})

        # Get List of beneficiaries
        beneficiaries = get_beneficiaries()

        # Create a list of dictionaries of transactions to be sent to the api endpoint
        ftList = [{
            "amount": vendor_dict[vendor]['amtpaym'],
            "remarks": "Payment for invoice",
            "bankCode": vendor_dict[vendor]['idbank'],
            "beneName": vendor_dict[vendor]['accname'],
            "benePhoneno": "0000000000",
            "branchCode": vendor_dict[vendor]['bsbno'],
            "destinationAccount": vendor_dict[vendor]['accno'],
            "destinationBranch": vendor_dict[vendor]['bsbno'],
            "destinationCurrency": vendor_dict[vendor]['codecurn'],
            "nationalClearingCode": "000000",
            "sourceAccount": "0000000000000",
            "sourceBranch": "000000",
            "srcCurrency": vendor_dict[vendor]['codecurn'],
            "swiftCode": "00000",
            "transferType": "IAT",
            "beneTransfer": False,
        } for vendor in vendor_dict]

        print(ftList)

        # Send the list of transactions to the api endpoint
        url = 'https://api.test.com/ft'
        headers = {'Content-Type': 'application/json'}
        params = {
            "service": "CORE_BANKING_FT",
            "request": {
                "ftList": ftList
            }
        }

        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()
            return JsonResponse({'message': 'Transaction(s) Recieved and Posted'}, safe=False)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'message': 'Error: ' + str(e)}, safe=False)
