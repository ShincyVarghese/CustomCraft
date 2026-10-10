from django.shortcuts import render

# Create your views here.

def shop(request):

    return render(
        request,
        'product/shop.html'
    )


def custom_order(request):
    return render(request,'products/custom_order.html')