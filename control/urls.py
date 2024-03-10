from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.control_index, name="control_index"),
    # Login ##############################################################################
    path("login/", views.control_login, name="login"), 
        path("sing_in/", views.control_sign_in, name="control_sign_in"), 
        path("log_out/", views.control_log_out, name="control_log_out"), 

   # Store ##############################################################################
    path("info/", views.control_info, name="control_info"),
        path("info/edit/", views.control_info_edit, name="control_info_edit"),

    # Categories ##############################################################################
    path("categories/", views.control_categories_all, name="control_categories_all"),
    path("category/add/", views.control_category_add, name="control_category_add"),
        path("category/create/", views.control_category_create, name="control_category_create"),
        path("category/edit/", views.control_category_edit, name="control_category_edit"),
        path("category/delete/", views.control_category_delete, name="control_category_delete"),
    path("category/<int:id>/", views.control_category_detail, name="control_category_detail"),


    # Slider ##############################################################################
    path("sliders/", views.control_sliders_all, name="control_sliders_all"),
        path("slider/add/", views.control_slider_add, name="control_slider_add"),
        path("slider/create/", views.control_slider_create, name="control_slider_create"),
        path("slider/edit/", views.control_slider_edit, name="control_slider_edit"),
        path("slider/delete/", views.control_slider_delete, name="control_slider_delete"),
        path("slider/<int:id>/", views.control_slider_detail, name="control_slider_detail"),

   # Slider Categories ##############################################################################
    path("slidercategories/", views.control_slidercategories_all, name="control_slidercategories_all"),
    path("slidercategory/add/", views.control_slidercategory_add, name="control_slidercategory_add"),
        path("slidercategory/create/", views.control_slidercategory_create, name="control_slidercategory_create"),
        path("slidercategory/edit/", views.control_slidercategory_edit, name="control_slidercategory_edit"),
        path("slidercategory/delete/", views.control_slidercategory_delete, name="control_slidercategory_delete"),
    path("slidercategory/<int:id>/", views.control_slidercategory_detail, name="control_slidercategory_detail"),

   # Popular Categories ##############################################################################
    path("popularcategories/", views.control_popularcategories_all, name="control_popularcategories_all"),
    path("popularcategory/add/", views.control_popularcategory_add, name="control_popularcategory_add"),
        path("popularcategory/create/", views.control_popularcategory_create, name="control_popularcategory_create"),
        path("popularcategory/edit/", views.control_popularcategory_edit, name="control_popularcategory_edit"),
        path("popularcategory/delete/", views.control_popularcategory_delete, name="control_popularcategory_delete"),
    path("popularcategory/<int:id>/", views.control_popularcategory_detail, name="control_popularcategory_detail"),


    # Products ##############################################################################
    path("products/", views.control_products_all, name="control_products_all"),
    path("product/add/", views.control_product_add, name="control_product_add"),
        path("product/create/", views.control_product_create, name="control_product_create"),
        path("product/edit/", views.control_product_edit, name="control_product_edit"),
        path("product/delete/", views.control_product_delete, name="control_product_delete"),
    path("product/<int:id>/", views.control_product_detail, name="control_product_detail"),

    # Product Image##############################################################################
    path("product/product_image/create/", views.control_product_image_create, name="control_product_image_create"),
    path("product/product_image/remove/<int:product_id>_<int:id>", views.control_product_image_remove, name="control_product_image_remove"),

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


    # Master ##############################################################################
    path("masters/", views.control_masters_all, name="control_masters_all"),
        path("master/add/", views.control_master_add, name="control_master_add"),
        path("master/create/", views.control_master_create, name="control_master_create"),
        path("master/edit/", views.control_master_edit, name="control_master_edit"),
        path("master/delete/", views.control_master_delete, name="control_master_delete"),
        path("master/<int:id>/", views.control_master_detail, name="control_master_detail"),

    # Footer Slider ##############################################################################
    path("footsliders/", views.control_footsliders_all, name="control_footsliders_all"),
        path("footslider/add/", views.control_footslider_add, name="control_footslider_add"),
        path("footslider/create/", views.control_footslider_create, name="control_footslider_create"),
        path("footslider/edit/", views.control_footslider_edit, name="control_footslider_edit"),
        path("footslider/delete/", views.control_footslider_delete, name="control_footslider_delete"),
        path("footslider/<int:id>/", views.control_footslider_detail, name="control_footslider_detail"),

]