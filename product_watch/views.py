from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from helper.crons import product_details_scrap
import numpy as np
import io
import base64
from watch.models import ProductWatch

def scrap(request):
    product_details_scrap()
    return HttpResponse("Done")


def dashboard(request):

    # plot
    dates = np.linspace(0, 10, 100)
    price = np.sin(dates)
    
    watches = []
    active_product_watch = ProductWatch.objects.filter(is_active=True)
    for product_watch in active_product_watch:
        product_history = product_watch.history.all()[:10]
        dates = []
        price = []
        for history in product_history:
            dates.append(history.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            price.append(history.price)
        watches.append({
            'dates': list(dates),
            'price': list(price),
        })
    context = {
        'watches': watches
    }
    print('context: ', context)
    return render(request, 'dashboard.html', context)

def list_watches(request):
    active_product_watch = ProductWatch.objects.filter(is_active=True).values('id', 'name')
    return JsonResponse(list(active_product_watch), safe=False)


def product_history(request):
    id_ = request.GET.get('watch_id')
    context = []
    product_watch = ProductWatch.objects.filter(is_active=True, id=id_).first()
    product_history = product_watch.history.all()[:10]
    dates = []
    price = []
    for history in product_history:
        dates.append(history.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        price.append(history.price)
    context = {
        'dates': list(dates),
        'price': list(price),
    }
    return JsonResponse(context)