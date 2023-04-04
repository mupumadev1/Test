import json

import requests
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render

from .helpers import CustomPaginator
# Create your views here.
from .models import Transactions, Vendors


def is_ajax(request):
    """ Check if request is an ajax request """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def paginate_data(data, page_number, page_size=10):
    """ Paginate data and return page object and number of pages """
    paginator = CustomPaginator(data, page_size)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj, paginator.num_pages


def display_transactions(request):
    """
        Display datermit, idinvc, amtpaym, codecurn, idvend From the transactions table and bsbno,
        accno, accname From the Vendors table where idvend in transactions table is equal to vendorid
        in vendors table and pass it to the template
    """
    if request.method == 'GET':
        try:
            transaction_info = Transactions.objects.values('idbank', 'idvend', 'datermit', 'amtpaym', 'paymcode',
                                                           'codecurn', 'rateexchhc', 'idinvc').order_by('-datermit',
                                                                                                        '-idvend').all()
            vendor_info = Vendors.objects.values('vendorid', 'bsbno', 'accno', 'accname').all()

            page_number = request.GET.get('page')
            if page_number is None:
                page_number = 1
            page_obj, number_of_pages = paginate_data(transaction_info, page_number)
            return render(request, 'transactions/dashboard.html',
                          {'transaction_info': page_obj, 'vendor_info': vendor_info})
        except Exception as e:
            print(e)
            return render(request, 'transactions/dashboard.html', {'transactions': []}, {'vendors': []})


def format_response_data(page_number, transaction_info, vendor_info):
    """ Format Response data and return a dictionary containing the data"""
    if page_number is None:
        page_data, number_of_pages = paginate_data(transaction_info, 1)
        return {'transaction_info': list(page_data), 'vendor_info': list(vendor_info),
                'number_of_pages': number_of_pages}
    page_data, number_of_pages = paginate_data(transaction_info, int(page_number))
    return {'transaction_info': list(page_data), 'vendor_info': list(vendor_info), 'number_of_pages': number_of_pages}


def get_idvend_transactions(request):
    """ Search by idvend and return JSON response if found """
    if request.method == 'GET':
        try:
            vendor_id = request.GET.get('id')
            transaction_info = Transactions.objects.filter(idvend=vendor_id).values(
                'idvend', 'datermit', 'amtpaym', 'codecurn', 'idinvc').order_by('-datermit').all()
            vendor_info = Vendors.objects.filter(vendorid=vendor_id).values('vendorid', 'bsbno', 'accno',
                                                                            'accname').all()
            return JsonResponse(format_response_data(request.GET.get('page_number'),
                                                     transaction_info, vendor_info), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse([], safe=False)


def search_invoice_id(request):
    """ Search by idinvc in Request list and return JSON resposne if found """
    if request.method == 'POST':
        if is_ajax(request):
            try:
                # Get invoice ids from request
                invoice_ids = json.loads(request.POST.get('invoice_ids[]'))
                transaction_info = Transactions.objects.filter(idinvc__in=invoice_ids).values(
                    'idbank', 'idvend', 'datermit', 'amtpaym', 'codecurn', 'idinvc').order_by('-datermit',
                                                                                              '-idvend').all()
                vendor_info = Vendors.objects.values('vendorid', 'bsbno', 'accno', 'accname').all()
                return JsonResponse(format_response_data(request.GET.get('page_number'),
                                                         transaction_info, vendor_info), safe=False)
            except Exception as e:
                print(e)
                message = 'Error: ' + str(e)
                return JsonResponse({'message': message}, safe=False)
        else:
            return JsonResponse({'message': 'Not an ajax request'}, safe=False)
    else:
        return JsonResponse({'message': 'Not a POST request'}, safe=False)


def get_search_results(request):
    """ Get search results based on query parameters """
    if request.method == 'GET':
        try:
            # Dictionary containing field mapping parameters
            field_mapping_transactions = {
                'vendor_id': 'idvend__icontains',
                'date': 'datermit__icontains',
                'amount': 'amtpaym',
                'invoice_id': 'idinvc__icontains',
            }

            field_mapping_vendor = {
                'account_number': 'accno__icontains',
                'account_name': 'accname__icontains',
                'sort_code': 'bsbno__icontains',
                'bank_name': 'bankname__icontains',
            }

            search_params = request.GET.get('search_params')
            field_option = request.GET.get('filter_options')
            page_number = 1 if request.GET.get('page_number') is None else request.GET.get('page_number')

            if field_option in field_mapping_transactions and search_params:
                transaction_info = Transactions.objects.filter(
                    **{field_mapping_transactions[field_option]: search_params}).values(
                    'idbank', 'idvend', 'datermit', 'amtpaym', 'codecurn', 'idinvc').order_by('-datermit',
                                                                                              '-idvend').all()
                vendor_ids = [transaction['idvend'] for transaction in transaction_info]
                vendor_info = Vendors.objects.filter(vendorid__in=vendor_ids).values('vendorid', 'bsbno', 'accno',
                                                                                     'accname').all()
                return JsonResponse(format_response_data(page_number, transaction_info, vendor_info), safe=False)

            elif field_option in field_mapping_vendor and search_params:
                vendor_info = Vendors.objects.filter(**{field_mapping_vendor[field_option]: search_params}).values(
                    'vendorid', 'bsbno', 'accno', 'accname').all()
                vendor_ids = [vendor['vendorid'] for vendor in vendor_info]
                transaction_info = Transactions.objects.filter(idvend__in=vendor_ids).values(
                    'idbank', 'idvend', 'datermit', 'amtpaym', 'codecurn', 'idinvc').order_by('-datermit',
                                                                                              '-idvend').all()
                return JsonResponse(format_response_data(page_number, transaction_info, vendor_info), safe=False)
            else:
                return JsonResponse({'transaction_info': list([]), 'vendor_info': list([]),
                                     'number_of_pages': 1}, safe=False)

        except Exception as e:
            print(e)
            message = 'Error: ' + str(e)
            return JsonResponse({'message': message}, safe=False)
    else:
        return JsonResponse({'message': 'Not a GET request'}, safe=False)


def get_beneficiaries():
    """ Get beneficiaries from API endpoint """
    pass


def post_transactions(request):
    """ Post transactions to API endpoint """
    if request.method == 'POST':
        invoice_ids = json.loads(request.POST.get('invoice_ids[]'))
        transaction_type = json.loads(request.POST.get('transaction_type'))
        transaction_info = Transactions.objects.filter(idinvc__in=invoice_ids).values('idbank', 'idvend', 'amtpaym',
                                                                                      'codecurn', 'idinvc').all()
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
                     'codecurn': transaction['codecurn'], 'transaction_type': transaction_type[transaction['idinvc']]})

        # Get List of beneficiaries
        beneficiaries = get_beneficiaries()

        # Create a list of dictionaries of transactions to be sent to the api endpoint
        ft_list = [{
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
            "transferType": vendor_dict[vendor]['transaction_type'],
            "beneTransfer": False,
        } for vendor in vendor_dict]

        print(ft_list)

        # Send the list of transactions to the api endpoint
        url = 'https://api.test.com/ft'
        headers = {'Content-Type': 'application/json'}
        params = {
            "service": "CORE_BANKING_FT",
            "request": {
                "ftList": ft_list
            }
        }

        try:
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()
            return JsonResponse({'message': 'Transaction(s) Recieved and Posted'}, safe=False)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'message': 'Error: ' + str(e)}, safe=False)
