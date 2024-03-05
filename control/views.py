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

SECURE_PATH_ADMIN = '/control/'

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
    context = {
        "base": base_context(request=request),
    }
    return render(request, 'control/index.html', context)


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
    context = {"base": base_context(request=request)}
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
    region = get_object_or_404(Region, id=id)
    context = {
        "base": base_context(request=request),
        "region": region
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
    context = {
        "base": base_context(request=request),
        "regions":regions
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
    context = {
        "base": base_context(request=request),
        "regions": regions, 
        "district": district
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

# Footer Slider

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
    regions = Region.objects.all()
    districts = District.objects.all()
    context = {
        "base": base_context(request=request),
        "districts":districts,
        "regions":regions,
    }
    return render(request, "control/masters/add.html", context)


@login_required(login_url='login')
def control_master_create(request):    
    if request.method == "POST" and request.FILES["file"]:  
        region = get_object_or_404(Region, id=request.POST["region_id"])
        district = get_object_or_404(District, id=request.POST["district_id"])
        title = request.POST["title"]
        subtitle = request.POST["subtitle"]
        number_first = request.POST["number_first"]
        number_second = request.POST["number_second"]
        master = Master.objects.create(region=region, district=district, title=title, subtitle=subtitle, number_first=number_first, number_second=number_second,image=request.FILES["file"])
        master.save()
        return redirect(SECURE_PATH_ADMIN+"masters/?created")
    else: answer = {"code": 404, "error": "Page Not Found"}; return JsonResponse(answer, safe=False)


@login_required(login_url='login')
def control_master_detail(request, id):
    master = get_object_or_404(Master, id=id)
    regions = Region.objects.all()
    districts = District.objects.all()
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
        master.region = get_object_or_404(Region, id=request.POST["region_id"])
        master.district = get_object_or_404(District, id=request.POST["district_id"])
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
