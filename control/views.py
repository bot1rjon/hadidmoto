from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.contrib import auth

# Create your views here.

SECURE_PATH_ADMIN = '/sklad/'

def base_context(request):
    try: 
        code = request.build_absolute_uri().split('?')[1]
    except: 
        code = None
    context = {
        "code": code
    }
    return context


def control_login(request):
    context = {
        "base": base_context(request=request),
    }
    return render(request, "control/login.html", context)


def control_sign_in(request):
    if request.method =='POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(SECURE_PATH_ADMIN + '')
        return redirect(SECURE_PATH_ADMIN + 'login/?error')

def control_log_out(request):
    auth.logout(request)
    return redirect(SECURE_PATH_ADMIN + 'login/')


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Index  

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_index(request):
    total_categories = Category.objects.filter(available=True, is_active=True).count()
    total_products = Product.objects.filter(available=True, is_active=True).count()
    total_masters = Master.objects.all().count()
    total_slidercategories = SliderCategory.objects.all().count()
    total_populars = Product.objects.filter(available=True, is_active=True, popular=True).count()
    total_sliders = Slider.objects.all().count()
    total_popularcategories = PopularCategory.objects.all().count()  
    context = {
        "total_categories": total_categories,
        "total_products": total_products,
        "total_masters": total_masters,
        "total_slidercategories": total_slidercategories,
        "total_popularcategories": total_popularcategories,
        "total_sliders": total_sliders,
        "total_populars": total_populars,
        "base": base_context(request=request),
    }
    return render(request, 'control/index.html', context)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Store  

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_info(request):
    info = Info.objects.last()
    context = {
        "base": base_context(request=request),
        "info": info,
    }
    return render(request, 'control/about.html', context)
   

@login_required(login_url='login')
def control_info_edit(request):
    if request.method == "POST":
        if Info.objects.last():
            info = Info.objects.last()
            info.start_day = request.POST['start_day']
            info.start_day_time = request.POST['start_day_time']
            info.finish_day = request.POST['finish_day']
            info.finish_day_time = request.POST['finish_day_time']
            info.addition_day = request.POST['addition_day']
            info.addition_day_time = request.POST['addition_day_time']
            info.address = request.POST['address']
            info.phone_first = request.POST['phone_first']
            info.phone_second = request.POST['phone_second']
            info.telegram = request.POST['telegram']
            info.telegram_link = request.POST['telegram_link']
            info.instagram = request.POST['instagram']
            info.instagram_link = request.POST['instagram_link']
            info.youtube = request.POST['youtube']
            info.youtube_link = request.POST['youtube_link']
            info.map = request.POST['map']
            info.save()
        else:
            Info.objects.create(
            start_day = request.POST['start_day'],
            start_day_time = request.POST['start_day_time'],
            finish_day = request.POST['finish_day'],
            finish_day_time = request.POST['finish_day_time'],
            addition_day = request.POST['addition_day'],
            addition_day_time = request.POST['addition_day_time'],
            address = request.POST['address'],
            phone_first = request.POST['phone_first'],
            phone_second = request.POST['phone_second'],
            telegram = request.POST['telegram'],
            telegram_link = request.POST['telegram_link'],
            instagram = request.POST['instagram'],
            instagram_link = request.POST['instagram_link'],
            youtube = request.POST['youtube'],
            youtube_link = request.POST['youtube_link'],
            map = request.POST['map']
            )
        return redirect(SECURE_PATH_ADMIN + "info/?edit")


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Categories

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_categories_all(request):
    categories = Category.objects.filter(available=True)
    nav_categories = Category.objects.filter(available=True, is_active=True)
    navactive = 0
    for i in categories:
        if i.nav == True:
            navactive += 1
    context = {
        "base": base_context(request=request),
        "categories":categories,
        "navactive":navactive
    }
    return render(request, "control/categories/all.html", context)


@login_required(login_url='login')
def control_category_add(request):
    categories = Category.objects.filter(available=True, is_active=True)
    navactive = 0
    for i in categories:
        if i.nav == True:
            navactive += 1
    context = {
        "base": base_context(request=request),
        "navactive": navactive
    }
    return render(request, "control/categories/add.html", context)


@login_required(login_url='login')
def control_category_create(request):    
    if request.method == "POST": 
        title = request.POST["title"]
        priority = request.POST["priority"]
        try:
            if request.POST["nav"]:
                nav = True
            else: 
                nav = False 
        except:
            nav = False
        category = Category.objects.create(title=title, nav=nav, priority=priority)
        category.set_slug(title=title)
        return redirect(SECURE_PATH_ADMIN+"categories/?created")
    else: answer = {"code": 404,"error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_category_detail(request, id):
    category= get_object_or_404(Category, id=id)
    categories = Category.objects.filter(available=True, is_active=True)
    navactive = 0
    for i in categories:
        if i.nav == True:
            navactive += 1
    context = {
        "base": base_context(request=request),
        "category": category,
        "navactive": navactive
    }
    
    return render(request, "control/categories/detail.html", context)


@login_required(login_url='login')
def control_category_edit(request):
    if request.method == "POST":
        category = get_object_or_404(Category, id=request.POST["id"])
        category.priority = request.POST["priority"]
        category.title = request.POST["title"]
        category.set_slug(title=category.title)
        try:
            if request.POST["is_active"]:
                category.is_active = True
                category.nav = True
            else: 
                category.is_active = False 
                category.nav = False 
        except:
            category.is_active = False
            category.nav = False 
        try:
            if request.POST["nav"] and request.POST["is_active"]:
                category.nav = True
            else: 
                category.nav = False 
        except:
            category.nav = False
        category.save()
        return redirect(SECURE_PATH_ADMIN + f"categories/?edited")
    else: answer = {"code": 404,"error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_category_delete(request):
    if request.method == "POST": 
        category = get_object_or_404(Category, id=request.POST["id"])
        category.available = False
        category.delete()
        return redirect(SECURE_PATH_ADMIN + "categories/?deleted")
    else: answer = {"code": 404,"error": "Page Not Found"}; return JsonResponse(answer, safe=False)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Slider

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_sliders_all(request):
    sliders = Slider.objects.all()
    categories = Category.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "sliders":sliders
    }
    return render(request, "control/sliders/all.html", context)
    

@login_required(login_url='login')
def control_slider_add(request):
    categories = Category.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "categories": categories
    }
    return render(request, "control/sliders/add.html", context)


@login_required(login_url='login')
def control_slider_create(request):    
    if request.method == "POST" and request.FILES["file"]: 
        slider = Slider.objects.create(title=request.POST["title"], subtitle=request.POST["subtitle"],content=request.POST["content"],priority=request.POST["priority"],image=request.FILES["file"])
        slider.save()
        return redirect(SECURE_PATH_ADMIN+"sliders/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_slider_detail(request, id):
    slider = get_object_or_404(Slider, id=id)
    categories = Category.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "slider": slider
    }
    return render(request, "control/sliders/detail.html", context)


@login_required(login_url='login')
def control_slider_edit(request):    
    if request.method == "POST" or request.FILES["file"]:  
        slider = get_object_or_404(Slider, id=request.POST["slider_id"])
        slider.title = request.POST["title"]
        slider.subtitle = request.POST["subtitle"]
        slider.content = request.POST["content"]
        slider.priority = request.POST["priority"]
        try: 
            slider.image = request.FILES["file"]
        except:
            pass
        slider.save()
        return redirect(SECURE_PATH_ADMIN+f"sliders/?edited")


@login_required(login_url='login')
def control_slider_delete(request):
    if request.method == "POST":
        slider = get_object_or_404(Slider, id=request.POST["slider_id"])
        slider.delete()
        return redirect(SECURE_PATH_ADMIN + "sliders/?deleted")



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Slider Categories

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_slidercategories_all(request):
    slidercategories = SliderCategory.objects.all()
    total_slidercategories = SliderCategory.objects.all().count()
    categories = Category.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "slidercategories":slidercategories,
        "total_slidercategories":total_slidercategories
    }
    return render(request, "control/slidercategories/all.html", context)
    

@login_required(login_url='login')
def control_slidercategory_add(request):
    categories = Category.objects.filter(available=True, is_active=True)
    total_slidercategories = SliderCategory.objects.all().count()
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "total_slidercategories":total_slidercategories
    }
    return render(request, "control/slidercategories/add.html", context)


@login_required(login_url='login')
def control_slidercategory_create(request):    
    if request.method == "POST" and request.FILES["file"]: 
        category = get_object_or_404(Category, id=request.POST["category_id"])
        slidercategory = SliderCategory.objects.create(category=category, title=request.POST["title"], subtitle=request.POST["subtitle"],image=request.FILES["file"])
        slidercategory.save()
        return redirect(SECURE_PATH_ADMIN+"slidercategories/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_slidercategory_detail(request, id):
    slidercategory = get_object_or_404(SliderCategory, id=id)
    categories = Category.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "slidercategory": slidercategory
    }
    return render(request, "control/slidercategories/detail.html", context)


@login_required(login_url='login')
def control_slidercategory_edit(request):    
    if request.method == "POST" or request.FILES["file"]:  
        slidercategory = get_object_or_404(SliderCategory, id=request.POST["slidercategory_id"])
        category = get_object_or_404(Category, id=request.POST["category_id"])
        slidercategory.category = category
        slidercategory.subtitle = request.POST["subtitle"]
        slidercategory.title = request.POST["title"]
        try: 
            slidercategory.image = request.FILES["file"]
        except:
            pass
        slidercategory.save()
        return redirect(SECURE_PATH_ADMIN+f"slidercategories/?edited")


@login_required(login_url='login')
def control_slidercategory_delete(request):
    if request.method == "POST":
        slidercategory = get_object_or_404(SliderCategory, id=request.POST["slidercategory_id"])
        slidercategory.delete()
        return redirect(SECURE_PATH_ADMIN + "slidercategories/?deleted")


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Popular Categories

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_popularcategories_all(request):
    popularcategories = PopularCategory.objects.all()
    categories = Category.objects.filter(available=True, is_active=True)
    total_popularcategories = PopularCategory.objects.all().count() 
    context = {
        "base": base_context(request=request),
        "popularcategories":popularcategories,
        "total_popularcategories":total_popularcategories
    }
    return render(request, "control/popularcategories/all.html", context)
    

@login_required(login_url='login')
def control_popularcategory_add(request):
    categories = Category.objects.filter(available=True, is_active=True)
    total_popularcategories = PopularCategory.objects.all().count()  
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "total_popularcategories":total_popularcategories
    }
    return render(request, "control/popularcategories/add.html", context)


@login_required(login_url='login')
def control_popularcategory_create(request):    
    if request.method == "POST" and request.FILES["file"]: 
        category = get_object_or_404(Category, id=request.POST["category_id"])
        popularcategory = PopularCategory.objects.create(category=category, title=request.POST["title"], priority=request.POST["priority"], image=request.FILES["file"])
        popularcategory.save()
        return redirect(SECURE_PATH_ADMIN+"popularcategories/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_popularcategory_detail(request, id):
    popularcategory = get_object_or_404(PopularCategory, id=id)
    categories = Category.objects.filter(available=True, is_active=True)
    total_popularcategories = PopularCategory.objects.all().count() 
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "popularcategory": popularcategory,
        "total_popularcategories":total_popularcategories
    }
    return render(request, "control/popularcategories/detail.html", context)


@login_required(login_url='login')
def control_popularcategory_edit(request):    
    if request.method == "POST" or request.FILES["file"]:  
        popularcategory = get_object_or_404(PopularCategory, id=request.POST["popularcategory_id"])
        category = get_object_or_404(Category, id=request.POST["category_id"])
        popularcategory.category = category
        popularcategory.priority = request.POST["priority"]
        popularcategory.title = request.POST["title"]
        try: 
            popularcategory.image = request.FILES["file"]
        except:
            pass
        popularcategory.save()
        return redirect(SECURE_PATH_ADMIN+f"popularcategories/?edited")


@login_required(login_url='login')
def control_popularcategory_delete(request):
    if request.method == "POST":
        popularcategory = get_object_or_404(PopularCategory, id=request.POST["popularcategory_id"])
        popularcategory.delete()
        return redirect(SECURE_PATH_ADMIN + "popularcategories/?deleted")



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Products

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_products_all(request):
    products = Product.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "products": products
    }
    return render(request, "control/products/all.html", context)

@login_required(login_url='login')
def control_product_add(request):
    categories = Category.objects.filter(available=True, is_active=True)
    context = {
        "base": base_context(request=request),
        "categories": categories,
    }
    return render(request, "control/products/add.html", context)


@login_required(login_url='login')
def control_product_create(request):
    if request.method == "POST" and request.FILES["file"]:
        category = get_object_or_404(Category, id=request.POST["category_id"])    
        title = request.POST["title"]
        subtitle = request.POST["subtitle"]
        company = request.POST["company"]
        description = request.POST["description"]
        priority = request.POST["priority"]
        price = request.POST["price"]
        image_min = request.FILES["file"]
        image_max = request.FILES["file"]
        if request.POST["old_price"] != "" and request.POST["old_price"] != "None":old_price = request.POST["old_price"]
        else: old_price = 0       
        if request.POST["discount"] != "" and request.POST["discount"] != "None":discount = request.POST["discount"]
        else: discount = 0           
        try:
            if request.POST["popular"]:
                popular = True
            else: 
                popular = False 
        except:
            popular = False
        try:
            if request.POST["available_price"]:
                available_price = True
            else: 
                available_price = False 
        except:
            available_price = False
        product = Product.objects.create(category=category, title=title, subtitle=subtitle, company=company, priority=priority, description=description, image_min=image_min, image_max=image_max, price=price, old_price=old_price, discount=discount, popular=popular, available_price=available_price)
        product.set_slug(title=title)
        return redirect(SECURE_PATH_ADMIN + 'products/?created')

    else:  answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_product_detail(request, id):
    categories = Category.objects.filter(available=True, is_active=True)
    product_img = ProductImage.objects.all()
    product =  get_object_or_404(Product, id=id)
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "product_img": product_img,
        "product": product,
    }
    return render(request, 'control/products/detail.html', context)
    

@login_required(login_url='login')
def control_product_edit(request):
    if request.method == 'POST' or request.FILES["file"]:
        product = get_object_or_404(Product, id=request.POST["id"])
        product.category = get_object_or_404(Category, id=request.POST["category_id"])
        product.description = request.POST["description"]
        product.priority = request.POST["priority"]
        product.title = request.POST["title"]
        product.subtitle = request.POST["subtitle"]
        product.company = request.POST["company"]
        product.price = request.POST["price"]
        if request.POST["old_price"] != "" and request.POST["old_price"] != "None":product.old_price = request.POST["old_price"]
        else: product.old_price = 0       
        if request.POST["discount"] != "" and request.POST["discount"] != "None":product.discount = request.POST["discount"]
        else: product.discount = 0     
        product.set_slug(title=product.title)
        try:
            if request.POST["is_active"]:
                product.is_active = True
            else: 
                product.is_active = False 
        except:
            product.is_active = False
        try:
            if request.POST["popular"]:
                product.popular = True
            else: 
                product.popular = False 
        except:
            product.popular = False
        try:
            if request.POST["available_price"]:
                 product.available_price = True
            else: 
                 product.available_price = False 
        except:
             product.available_price = False
        try: 
            product.image_max = request.FILES["file"]
            product.image_min = request.FILES["file"]
        except:
            pass
        product.save()
    return redirect(SECURE_PATH_ADMIN + f"product/{product.id}/?edited")


@login_required(login_url='login')
def control_product_delete(request):
    if request.method == "POST":
        product = get_object_or_404(Product, id=request.POST["id"])
        product.available = True
        product.save()
        return redirect(SECURE_PATH_ADMIN + "products/?deleted")


@login_required(login_url='login')
def control_product_image_create(request):
    if request.method == "POST" and request.FILES["file"]:
        product = Product.objects.get(id=request.POST["product_id"])
        ProductImage.objects.create(
            product = product, 
            img_min = request.FILES["file"],
            img_full = request.FILES["file"],
        )
        return redirect(SECURE_PATH_ADMIN + f"product/{product.id}/?p_image_add")


@login_required(login_url='login')
def control_product_image_remove(request, product_id, id):
        product = Product.objects.get(id=product_id)
        product_image = ProductImage.objects.get(product=product, id=id)
        product_image.delete()
        return redirect(SECURE_PATH_ADMIN + f"product/{product.id}/?p_image_remove")


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Regions

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_regions_all(request):
    regions = Region.objects.all()
    context = {"base": base_context(request=request),"regions":regions}
    return render(request, "control/regions/all.html", context)

@login_required(login_url='login')
def control_region_add(request):
    regions = [
        'Toshkent.V', 'Toshkent.Sh', 'Samarqand', 'Buxoro', 'Namangan', 'Andijon', 'Farg\'ona',
        'Xorazm', 'Qashqadaryo', 'Surxondaryo', 'Navoiy', 'Jizzax', 'Sirdaryo', 'Qoraqalpog\'iston',
    ]
    context = {"regions": regions, "base": base_context(request=request)}
    return render(request, "control/regions/add.html", context)

@login_required(login_url='login')
def control_region_create(request):    
    if request.method == "POST": 
        title = request.POST["title"]
        region = Region.objects.create(title = title)
        region.save()
        return redirect(SECURE_PATH_ADMIN+"regions/?created")
    else: answer = {"code": 404,"error": "Page Not Found"}; return JsonResponse(answer, safe=False)

@login_required(login_url='login')
def control_region_detail(request, id):
    regions = [
        'Toshkent.V', 'Toshkent.Sh', 'Samarqand', 'Buxoro', 'Namangan', 'Andijon', 'Farg\'ona',
        'Xorazm', 'Qashqadaryo', 'Surxondaryo', 'Navoiy', 'Jizzax', 'Sirdaryo', 'Qoraqalpog\'iston',
    ]
    region = get_object_or_404(Region, id=id)
    context = {
        "base": base_context(request=request),
        "region": region,
        "regions": regions
    }
    
    return render(request, "control/regions/detail.html", context)

@login_required(login_url='login')
def control_region_edit(request):
    if request.method == "POST":
        region = get_object_or_404(Region, id=request.POST["id"])
        region.title = request.POST['title']
        region.save()
        return redirect(SECURE_PATH_ADMIN + f"regions/?edited")
    else: answer = {"code": 404,"error": "Page Not Found"}; return JsonResponse(answer, safe=False)

@login_required(login_url='login')
def control_region_delete(request):
    if request.method == "POST": 
        region = get_object_or_404(Region, id=request.POST["id"])
        region.delete()
        return redirect(SECURE_PATH_ADMIN + "regions/?deleted")
    else: answer = {"code": 404,"error": "Page Not Found"}; return JsonResponse(answer, safe=False)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Districts

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_districts_all(request):
    districts = District.objects.all()
    context = {
        "base": base_context(request=request),
        "districts":districts
    }
    return render(request, "control/districts/all.html", context)
    

@login_required(login_url='login')  
def control_district_add(request):
    regions = Region.objects.all()
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
    context = {
        "base": base_context(request=request),
        "regions":regions,
        "districts": districts
    }
    return render(request, "control/districts/add.html", context)


@login_required(login_url='login')
def control_district_create(request):    
    if request.method == "POST": 
        title = request.POST["title"]
        region = get_object_or_404(Region, id=request.POST["region_id"])
        district = District.objects.create(region=region, title=title)
        district.save()
        return redirect(SECURE_PATH_ADMIN+"districts/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_district_detail(request, id):
    regions = Region.objects.all()
    district = get_object_or_404(District, id=id)
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
    context = {
        "base": base_context(request=request),
        "regions": regions, 
        "district": district,
        "districts": districts
    }
    return render(request, "control/districts/detail.html", context)

@login_required(login_url='login')
def control_district_edit(request):
    if request.method == "POST":
        region = get_object_or_404(Region, id=request.POST["region_id"])
        district = get_object_or_404(District, id=request.POST["id"])
        title = request.POST["title"]
        district.region = region
        district.title = title
        district.save()
        return redirect(SECURE_PATH_ADMIN + f"districts/?edited") 
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)

@login_required(login_url='login')
def control_district_delete(request):
    if request.method == "POST": 
        district = get_object_or_404(District, id=request.POST["id"])
        district.delete()
        return redirect(SECURE_PATH_ADMIN + "districts/?deleted")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Footer Slider

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_footsliders_all(request):
    footsliders = FooterSlider.objects.all()
    context = {
        "base": base_context(request=request),
        "footsliders":footsliders
    }
    return render(request, "control/footsliders/all.html", context)
    

@login_required(login_url='login')
def control_footslider_add(request):
    context = {
        "base": base_context(request=request)
    }
    return render(request, "control/footsliders/add.html", context)


@login_required(login_url='login')
def control_footslider_create(request):    
    if request.method == "POST" and request.FILES["file"]:  
        footslider = FooterSlider.objects.create(title=request.POST["title"],image=request.FILES["file"])
        footslider.save()
        return redirect(SECURE_PATH_ADMIN+"footsliders/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_footslider_detail(request, id):
    footslider = get_object_or_404(FooterSlider, id=id)
    context = {
        "base": base_context(request=request),
        "footslider": footslider
    }
    return render(request, "control/footsliders/detail.html", context)


@login_required(login_url='login')
def control_footslider_edit(request):    
    if request.method == "POST" or request.FILES["file"]:  
        footslider = get_object_or_404(FooterSlider, id=request.POST["footslider_id"])
        footslider.title = request.POST["title"]
        try: 
            footslider.image = request.FILES["file"]
        except:
            pass
        footslider.save()
        return redirect(SECURE_PATH_ADMIN+f"footsliders/?edited")


@login_required(login_url='login')
def control_footslider_delete(request):
    if request.method == "POST":
        footslider = get_object_or_404(FooterSlider, id=request.POST["footslider_id"])
        footslider.delete()
        return redirect(SECURE_PATH_ADMIN + "footsliders/?deleted")



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Master

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='login')
def control_masters_all(request):
    masters = Master.objects.all()
    regions = Region.objects.all()
    districts = District.objects.all()
    context = {
        "base": base_context(request=request),
        "masters":masters,
        "districts":districts,
        "regions":regions,
    }
    return render(request, "control/masters/all.html", context)
    

@login_required(login_url='login')
def control_master_add(request):
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
    context = {
        "base": base_context(request=request),
        "districts":districts,
        "regions":regions,
    }
    return render(request, "control/masters/add.html", context)


@login_required(login_url='login')
def control_master_create(request):    
    if request.method == "POST" and request.FILES["file"]:  
        title = request.POST["title"]
        subtitle = request.POST["subtitle"]
        number_first = request.POST["number_first"]
        sub_city = request.POST["sub_city"]
        region = request.POST["region"]
        district = request.POST["district"]
        number_second = request.POST["number_second"]
        master = Master.objects.create(region_name=region, district_name=district, sub_city=sub_city, title=title, subtitle=subtitle, number_first=number_first, number_second=number_second,image=request.FILES["file"])
        master.save()
        return redirect(SECURE_PATH_ADMIN+"masters/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_master_detail(request, id):
    master = get_object_or_404(Master, id=id)
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
    context = {
        "base": base_context(request=request),
        "master": master,
        "districts":districts,
        "regions":regions,

    }
    return render(request, "control/masters/detail.html", context)


@login_required(login_url='login')
def control_master_edit(request):    
    if request.method == "POST" or request.FILES["file"]:  
        master = get_object_or_404(Master, id=request.POST["master_id"])
        master.sub_city = request.POST["sub_city"]
        master.region_name = request.POST["region"]
        master.district_name = request.POST["district"]
        master.title = request.POST["title"]
        master.subtitle = request.POST["subtitle"]
        master.number_first = request.POST["number_first"]
        master.number_second = request.POST["number_second"]
        try: 
            master.image = request.FILES["file"]
        except:
            pass
        master.save()
        return redirect(SECURE_PATH_ADMIN+f"masters/?edited")


@login_required(login_url='login')
def control_master_delete(request):
    if request.method == "POST":
        master = get_object_or_404(Master, id=request.POST["master_id"])
        master.delete()
        return redirect(SECURE_PATH_ADMIN + "masters/?deleted")
