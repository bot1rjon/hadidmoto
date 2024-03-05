from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.control_index, name="control_index"),
    # Login ##############################################################################
    path("login/", views.control_login, name="login"), 
        path("sing_in/", views.control_sign_in, name="control_sign_in"), 
        path("log_out/", views.control_log_out, name="control_log_out"), 

    # Region and District ##############################################################################
    path("regions/", views.control_regions_all, name="control_regions_all"),
        path("region/add/", views.control_region_add, name="control_region_add"),
        path("region/create/", views.control_region_create, name="control_region_create"),
        path("region/edit/", views.control_region_edit, name="control_region_edit"),
        path("region/delete/", views.control_region_delete, name="control_region_delete"),
        path("region/<int:id>/", views.control_region_detail, name="control_region_detail"),

    path("districts/", views.control_districts_all, name="control_districts_all"),
        path("district/add/", views.control_district_add, name="control_district_add"),
        path("district/create/", views.control_district_create, name="control_district_create"),
        path("district/edit/", views.control_district_edit, name="control_district_edit"),
        path("district/delete/", views.control_district_delete, name="control_district_delete"),
        path("district/<int:id>/", views.control_district_detail, name="control_district_detail"),

    # Footer Slider ##############################################################################
    path("footsliders/", views.control_footsliders_all, name="control_footsliders_all"),
        path("footslider/add/", views.control_footslider_add, name="control_footslider_add"),
        path("footslider/create/", views.control_footslider_create, name="control_footslider_create"),
        path("footslider/edit/", views.control_footslider_edit, name="control_footslider_edit"),
        path("footslider/delete/", views.control_footslider_delete, name="control_footslider_delete"),
        path("footslider/<int:id>/", views.control_footslider_detail, name="control_footslider_detail"),

    # Master ##############################################################################
    path("masters/", views.control_masters_all, name="control_masters_all"),
        path("master/add/", views.control_master_add, name="control_master_add"),
        path("master/create/", views.control_master_create, name="control_master_create"),
        path("master/edit/", views.control_master_edit, name="control_master_edit"),
        path("master/delete/", views.control_master_delete, name="control_master_delete"),
        path("master/<int:id>/", views.control_master_detail, name="control_master_detail"),


]