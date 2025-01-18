from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    items = Product.objects.all()
    return render(request, 'index.html', {'items': items})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image.url,
    })
