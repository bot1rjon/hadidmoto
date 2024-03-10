from math import prod
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from control.models import *
import json
import requests
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def base_context(request):
    categories = Category.objects.filter(available=True, is_active=True)
    info = Info.objects.last()
    nav_categories = Category.objects.filter(available=True, is_active=True, nav=True)[0:2]
    footsliders = FooterSlider.objects.all()
    if Info:
        info = Info.objects.last()
    random_categories = []
    for i in range(0,4):
        random_categories.append(random.choice(categories))
    context = {"categories": categories, "nav_categories": nav_categories, "random_categories": random_categories, "footsliders":footsliders, "info": info}
    return context

def web_index(request):
    sliders = Slider.objects.all()
    slider_categories = SliderCategory.objects.filter()[0:2]
    popular_categories = PopularCategory.objects.filter()[0:6]
    discount = Product.objects.filter(available=True, is_active=True)
    discount_products = []
    for d in discount:
        if d.discount >= 1:
            discount_products.append(d)
    context = {"base": base_context(request=request),"sliders": sliders,"slider_categories": slider_categories,"popular_categories": popular_categories, "discount_products":discount_products}
    return render(request, "web/index.html", context)

def web_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True, is_active=True)
    popular_products = Product.objects.filter(available=True, is_active=True, popular=True)

    paginator = Paginator(products, 20)
    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get("page") or 1

    try: current_page = paginator.page(page)
    except: current_page = paginator.page(1)

    context = {"category": category, "products": current_page, "is_paginated": is_paginated, "paginator": paginator, "popular_products":popular_products, "base": base_context(request=request)}
    return render(request, "web/category.html", context)

def web_products(request):
    products = Product.objects.filter(available=True, is_active=True)
    popular_products = Product.objects.filter(available=True, is_active=True, popular=True)

    paginator = Paginator(products, 20)
    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get("page") or 1

    try: current_page = paginator.page(page)
    except: current_page = paginator.page(1)

    context = {
        "products": current_page,
        "popular_products": popular_products,
        "is_paginated": is_paginated,
        "paginator": paginator,
        "base": base_context(request=request)
    }

    return render(request, "web/products.html", context)

def web_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    populars = Product.objects.filter(available=True, is_active=True)
    product_image = ProductImage.objects.filter(product=product)[0:3]
    popular_products = []
    for p in populars:
        if p.popular == True:
            popular_products.append(p)
    context = {"product": product, "popular_products":popular_products, "product_image":product_image, "base": base_context(request=request)}
    return render(request, "web/product.html", context)

def web_products_discount(request):
    pro = Product.objects.filter(available=True, is_active=True)
    popular_products = Product.objects.filter(available=True, is_active=True, popular=True)
    products = []
    for p in pro:
        if p.discount >= 1:
            products.append(p)

    paginator = Paginator(products, 20)
    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get("page") or 1

    try: current_page = paginator.page(page)
    except: current_page = paginator.page(1)
    context = {"popular_products":popular_products,"products":current_page, "is_paginated": is_paginated, "paginator": paginator, "base": base_context(request=request)}
    return render(request, "web/products_discount.html", context)



def web_masters(request):
    regions = Region.objects.all()
    districts = District.objects.all()
    masters = Master.objects.all()
    products = Product.objects.filter(available=True, is_active=True)
    popular_products = []
    for p in products:
        if p.popular == True:
            popular_products.append(p)
    context = {"regions": regions, "districts": districts, "popular_products":popular_products, "masters": masters, "base": base_context(request=request)}

    return render(request, "web/master.html", context)


def page404(request, exception):
    context = {}
    return render (request, 'web/404.html', context)


def web_cart(request):
    regions = Region.objects.all()

    context = {"regions": regions, "base": base_context(request=request)}
    return render(request, "web/cart.html", context)

@csrf_exempt
def web_cart_get(request):
    data = json.loads(request.body)
    products = Product.objects.filter(available=True, is_active=True)
    answer = {"code":200, "cart_products":[]}
    get_products = data['products']
   
    matching_items = []
    for get_pro in get_products:
        for set_pro in products:
            if int(get_pro['id']) == set_pro.id:
                print(get_pro['id'])
                answer['cart_products'].append({
                    'id': set_pro.id,
                    'title': set_pro.title,
                    'subtitle': set_pro.subtitle,
                    'price': set_pro.price,
                    'old_price': set_pro.old_price,
                    'quantity': get_pro['quantity'],
                    'discount': set_pro.discount,
                    'company': set_pro.company,
                    'img': set_pro.image_min.url if set_pro.image_min else None,
                })

    return JsonResponse(answer, safe=False)

@csrf_exempt    
def web_order_send(request):
    data = json.loads(request.body)
    c = Order.objects.create(
        order = data["name"],
    )
    answer = {
        "code": 200
    }
    order_id = c.id
    orders = data["orders"]
    message = f""" Buyurtma: {order_id}
    Mijoz: {data['name']} 
    Nomer: {data["phone"]} 
    Manzil: {data["region"]} \n \n\n MAHSULOTLAR """
    for order in orders:
        message += f"""
        Mahsulot: {order["title"]}
        Narxi: {order['price']} so'm
        Umumiy Narxi:  {int(order['price'] * order["quantity"])} so'm
        Miqdori: {order["quantity"]} ta
        """

    url = f"https://api.telegram.org/bot6672406816:AAEPBP1PK5qJpt7qDJcn7lJhPQQrhWIQ1S8/sendMessage?chat_id=-4175113157&text=" + message
    r = requests.get(url) 
    return JsonResponse(answer, safe=False)