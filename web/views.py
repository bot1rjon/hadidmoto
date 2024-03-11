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
    masters = Master.objects.all()
    products = Product.objects.filter(available=True, is_active=True)
    popular_products = []
    regions = [
        'Toshkent.V', 'Toshkent.Sh', 'Samarqand', 'Buxoro', 'Namangan', 'Andijon', 'Farg\'ona',
        'Xorazm', 'Qashqadaryo', 'Surxondaryo', 'Navoiy', 'Jizzax', 'Sirdaryo', 'Qoraqalpog\'iston',
    ]
    districts = [
        {"title": "Bo'ka", "region": "Toshkent.V"},
        {"title": "Chinoz", "region": "Toshkent.V"},
        {"title": "Qibray", "region": "Toshkent.V"},
        {"title": "Ohangaron", "region": "Toshkent.V"},
        {"title": "Oqqo'rg'on", "region": "Toshkent.V"},
        {"title": "Parkent", "region": "Toshkent.V"},
        {"title": "Piskent", "region": "Toshkent.V"},
        {"title": "Quyi Chirchiq", "region": "Toshkent.V"},
        {"title": "O'rta Chirchiq", "region": "Toshkent.V"},
        {"title": "Yangiyo'l", "region": "Toshkent.V"},
        {"title": "Yuqori Chirchiq", "region": "Toshkent.V"},
        {"title": "Zangiota", "region": "Toshkent.V"},
        {"title": "Bektemir", "region": "Toshkent.Sh"},
        {"title": "Chilonzor", "region": "Toshkent.Sh"},
        {"title": "Yashnobod", "region": "Toshkent.Sh"},
        {"title": "Mirobod", "region": "Toshkent.Sh"},
        {"title": "Mirzo Ulug'bek", "region": "Toshkent.Sh"},
        {"title": "Sergeli", "region": "Toshkent.Sh"},
        {"title": "Shayxontohur", "region": "Toshkent.Sh"},
        {"title": "Olmazor", "region": "Toshkent.Sh"},
        {"title": "Uchtepa (Toshkent)", "region": "Toshkent.Sh"},
        {"title": "Yakkasaroy", "region": "Toshkent.Sh"},
        {"title": "Yunusobod", "region": "Toshkent.Sh"},
        {"title": "Oqoltin", "region": "Sirdaryo"},
        {"title": "Boyovut", "region": "Sirdaryo"},
        {"title": "Guliston", "region": "Sirdaryo"},
        {"title": "Xovos", "region": "Sirdaryo"},
        {"title": "Mirzaobod", "region": "Sirdaryo"},
        {"title": "Saykhunobod", "region": "Sirdaryo"},
        {"title": "Sardoba", "region": "Sirdaryo"},
        {"title": "Sirdaryo", "region": "Sirdaryo"},
        {"title": "Shirin", "region": "Sirdaryo"},
        {"title": "Yangier", "region": "Sirdaryo"},
        {"title": "Andijon (tuman)", "region": "Andijon"},
        {"title": "Andijon shahri", "region": "Andijon"},
        {"title": "Asaka", "region": "Andijon"},
        {"title": "Baliqchi", "region": "Andijon"},
        {"title": "Bo'z (tuman)", "region": "Andijon"},
        {"title": "Buloqboshi", "region": "Andijon"},
        {"title": "Buston", "region": "Andijon"},
        {"title": "Izboskan (tuman)", "region": "Andijon"},
        {"title": "Jalaquduq (tuman)", "region": "Andijon"},
        {"title": "Kho'jaobod", "region": "Andijon"},
        {"title": "Qorg'ontepa", "region": "Andijon"},
        {"title": "Marhamat", "region": "Andijon"},
        {"title": "Oltinko'l (tuman)", "region": "Andijon"},
        {"title": "Pakhtaobod", "region": "Andijon"},
        {"title": "Shahrixon (tuman)", "region": "Andijon"},
        {"title": "Khonobod shahri", "region": "Andijon"},
        {"title": "Ulug'nor (tuman)", "region": "Andijon"},   
        {"title": "Oltiariq", "region": "Farg'ona"},
        {"title": "Bag'dod", "region": "Farg'ona"},
        {"title": "Beshariq", "region": "Farg'ona"},
        {"title": "Qo'qon", "region": "Farg'ona"},
        {"title": "Quvusoy", "region": "Farg'ona"},
        {"title": "Marg'ilon", "region": "Farg'ona"},
        {"title": "Buvayda", "region": "Farg'ona"},
        {"title": "Dang'ara", "region": "Farg'ona"},
        {"title": "Farg'ona", "region": "Farg'ona"},
        {"title": "Furqat", "region": "Farg'ona"},
        {"title": "Qushtepa", "region": "Farg'ona"},
        {"title": "Quva", "region": "Farg'ona"},
        {"title": "Rishton", "region": "Farg'ona"},
        {"title": "Sokh", "region": "Farg'ona"},
        {"title": "Toshloq", "region": "Farg'ona"},
        {"title": "Uchkuprik", "region": "Farg'ona"},
        {"title": "O'zbekiston", "region": "Farg'ona"},
        {"title": "Yozovon", "region": "Farg'ona"},
        {"title": "Chortoq", "region": "Namangan"},
        {"title": "Chust", "region": "Namangan"},
        {"title": "Kosonsoy", "region": "Namangan"},
        {"title": "Mingbuloq", "region": "Namangan"},
        {"title": "Namangan", "region": "Namangan"},
        {"title": "Norin (O'zbekiston)", "region": "Namangan"},
        {"title": "Pop", "region": "Namangan"},
        {"title": "To'raqo'rg'on", "region": "Namangan"},
        {"title": "Uchqo'rg'on", "region": "Namangan"},
        {"title": "Uychi", "region": "Namangan"},
        {"title": "Yangiqo'rg'on", "region": "Namangan"},
        {"title": "Arnasoy", "region": "Jizzax"},
        {"title": "Bakhmal", "region": "Jizzax"},
        {"title": "Dostlik", "region": "Jizzax"},
        {"title": "Forish", "region": "Jizzax"},
        {"title": "G'allaorol", "region": "Jizzax"},
        {"title": "Jizzax", "region": "Jizzax"},
        {"title": "Mirzachul", "region": "Jizzax"},
        {"title": "Pakhtakor", "region": "Jizzax"},
        {"title": "Yangiobod", "region": "Jizzax"},
        {"title": "Zomin", "region": "Jizzax"},
        {"title": "Sharof Rashidov", "region": "Jizzax"},
        {"title": "Zafarobod", "region": "Jizzax"},
        {"title": "Zarbdor", "region": "Jizzax"},
        {"title": "Angor", "region": "Surxondaryo"},
        {"title": "Bandixon", "region": "Surxondaryo"},
        {"title": "Boysun", "region": "Surxondaryo"},
        {"title": "Denov", "region": "Surxondaryo"},
        {"title": "Zarqo'rg'on", "region": "Surxondaryo"},
        {"title": "Qiziriq", "region": "Surxondaryo"},
        {"title": "Qumqo'rg'on", "region": "Surxondaryo"},
        {"title": "Muzrabot", "region": "Surxondaryo"},
        {"title": "Oltinsoy", "region": "Surxondaryo"},
        {"title": "Sariosiyo", "region": "Surxondaryo"},
        {"title": "Sherobod", "region": "Surxondaryo"},
        {"title": "Shurchi", "region": "Surxondaryo"},
        {"title": "Termiz", "region": "Surxondaryo"},
        {"title": "Uzun", "region": "Surxondaryo"},
        {"title": "Chiroqchi", "region": "Qashqadaryo"},
        {"title": "Dehqonobod", "region": "Qashqadaryo"},
        {"title": "Guzor", "region": "Qashqadaryo"},
        {"title": "Qamashi", "region": "Qashqadaryo"},
        {"title": "Qarshi", "region": "Qashqadaryo"},
        {"title": "Koson", "region": "Qashqadaryo"},
        {"title": "Kasbi", "region": "Qashqadaryo"},
        {"title": "Kitob", "region": "Qashqadaryo"},
        {"title": "Mirishkor", "region": "Qashqadaryo"},
        {"title": "Muborak", "region": "Qashqadaryo"},
        {"title": "Nishon", "region": "Qashqadaryo"},
        {"title": "Shahrisabz", "region": "Qashqadaryo"},
        {"title": "Yakkabog", "region": "Qashqadaryo"}, 
        {"title": "Bulungur", "region": "Samarqand"},
        {"title": "Ishtikhon", "region": "Samarqand"},
        {"title": "Jomboy", "region": "Samarqand"},
        {"title": "Kattaqo'rg'on", "region": "Samarqand"},
        {"title": "Qo'shrabot", "region": "Samarqand"},
        {"title": "Narpay", "region": "Samarqand"},
        {"title": "Nurobod", "region": "Samarqand"},
        {"title": "Oqdaroy", "region": "Samarqand"},
        {"title": "Pakhtachi", "region": "Samarqand"},
        {"title": "Payariq", "region": "Samarqand"},
        {"title": "Pastdarg'om", "region": "Samarqand"},
        {"title": "Samarqand", "region": "Samarqand"},
        {"title": "Toyloq", "region": "Samarqand"},
        {"title": "Urgut", "region": "Samarqand"},
        {"title": "Olot", "region": "Buxoro"},
        {"title": "Buxoro", "region": "Buxoro"},
        {"title": "G'ijduvon", "region": "Buxoro"},
        {"title": "Jondor", "region": "Buxoro"},
        {"title": "Kogon", "region": "Buxoro"},
        {"title": "Qorako'l", "region": "Buxoro"},
        {"title": "Qorovulbozor", "region": "Buxoro"},
        {"title": "Peshku", "region": "Buxoro"},
        {"title": "Romitan", "region": "Buxoro"},
        {"title": "Shofirkon", "region": "Buxoro"},
        {"title": "Vobkent", "region": "Buxoro"},
        {"title": "Navoiy", "region": "Navoiy"},
        {"title": "Zarafshon", "region": "Navoiy"},
        {"title": "Konimex", "region": "Navoiy"},
        {"title": "Karmana", "region": "Navoiy"},
        {"title": "Qiziltepa (Navoiy)", "region": "Navoiy"},
        {"title": "Xatirchi", "region": "Navoiy"},
        {"title": "Navbahor", "region": "Navoiy"},
        {"title": "Nurota", "region": "Navoiy"},
        {"title": "Tomdi", "region": "Navoiy"},
        {"title": "Uchkuduk", "region": "Navoiy"},
        {"title": "Bog'ot", "region": "Xorazm"},
        {"title": "Gurlan", "region": "Xorazm"},
        {"title": "Xonqa", "region": "Xorazm"},
        {"title": "Hazorasp", "region": "Xorazm"},
        {"title": "Xiva", "region": "Xorazm"},
        {"title": "Qo'shkupir", "region": "Xorazm"},
        {"title": "Shovot", "region": "Xorazm"},
        {"title": "Urganch", "region": "Xorazm"},
        {"title": "Yangiariq", "region": "Xorazm"},
        {"title": "Yangibozor", "region": "Xorazm"},
        {"title": "Amudaryo", "region": "Qoraqalpog'iston"},
        {"title": "Beruniy", "region": "Qoraqalpog'iston"},
        {"title": "Chimboy", "region": "Qoraqalpog'iston"},
        {"title": "Ellikqal'a", "region": "Qoraqalpog'iston"},
        {"title": "Kegayli", "region": "Qoraqalpog'iston"},
        {"title": "Mo'ynoq", "region": "Qoraqalpog'iston"},
        {"title": "Nukus", "region": "Qoraqalpog'iston"},
        {"title": "Qanliko'l", "region": "Qoraqalpog'iston"},
        {"title": "Qon'g'irat", "region": "Qoraqalpog'iston"},
        {"title": "Qoraqo'zak", "region": "Qoraqalpog'iston"},
        {"title": "Shumanay", "region": "Qoraqalpog'iston"},
        {"title": "Taxtako'pir", "region": "Qoraqalpog'iston"},
        {"title": "Tortko'l", "region": "Qoraqalpog'iston"},
        {"title": "Xo'jayli", "region": "Qoraqalpog'iston"},
    ]    
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
                answer['cart_products'].append({
                    'id': set_pro.id,
                    'title': set_pro.title,
                    'subtitle': set_pro.subtitle,
                    'available_price': set_pro.available_price,
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
    total_price = 0
    message = f""" Buyurtma: {order_id}
    Mijoz: {data['name']} 
    No'mer: {data["phone"]} 
    Manzil: {data["region"]} \n \n\n MAHSULOTLAR """
    for order in orders:
        total_price += int(order['price'] * order["quantity"])
        message += f"""
        Mahsulot: {order["title"]}
        Narxi: {order['price']} so'm
        Miqdori: {order["quantity"]} ta
        Umumiy Narxi:  {int(order['price'] * order["quantity"])} so'm
        """
    message += f"""\n\n Umumiy Narx: {total_price} so'm """
    url = f"https://api.telegram.org/bot6373586338:AAG2J0VbKRT99sUgBvTqLL3kP4Lf25tXG2U/sendMessage?chat_id=-4156342549&text=" + message
    r = requests.get(url) 
    return JsonResponse(answer, safe=False)