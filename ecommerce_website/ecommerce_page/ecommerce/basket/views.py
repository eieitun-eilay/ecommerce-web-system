from http.client import HTTPResponse
from itertools import product
from urllib import response
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)
        baskettotal = basket.get_total_price()
        response = JsonResponse({'subtotal': baskettotal})
        return response
    else:
        return HttpResponseBadRequest('Invalid request')

# def basket_update(request):
#     basket = Basket(request)
#     if request.method == 'POST' and request.POST.get('action') == 'update':
#         product_id = int(request.POST.get('productid'))
#         product_qty = int(request.POST.get('productqty'))
#         basket.update(product=product_id, qty=product_qty)
        
#         response = JsonResponse({'Success' :True})
#         return response
#     else:
#         return HttpResponseBadRequest('Invalid request')

def basket_update(request):
    basket = Basket(request)
    if request.method == 'POST' and request.POST.get('action') == 'update':
        product_id = request.POST.get('productid')
        product_qty = int(request.POST.get('productqty'))
        
        if product_id is not None:
            product_id = int(product_id)
            basket.update(product=product_id, qty=product_qty)
            basketqty = basket.__len__()
            baskettotal = basket.get_total_price()
            response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        else:
            response = HttpResponseBadRequest('Invalid product ID')
        
        return response
    else:
        return HttpResponseBadRequest('Invalid request')
