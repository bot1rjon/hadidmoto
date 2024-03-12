from django.db import models
from django_resized import ResizedImageField
import string
import random
from slugify import slugify


class Region(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Master(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    sub_city = models.CharField(max_length=225, null=True, blank=True)
    number_first = models.CharField(max_length=100, null=True, blank=True)
    number_second = models.CharField(max_length=100, null=True, blank=True)
    image = ResizedImageField(size=[200, 200], quality=100, upload_to="master/", null=True, blank=True)
    region_name = models.CharField(max_length=225, null=True, blank=True)
    district_name = models.CharField(max_length=225, null=True, blank=True)
    

    def __str__(self):
        return self.title
 

class FooterSlider(models.Model):
    title = models.CharField(max_length=250)
    image = ResizedImageField(size=[400, 400], quality=100, upload_to="footer_slider/")

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=250)
    priority = models.IntegerField(default=0)
    slug = models.CharField(max_length=250, default="") 
    nav = models.BooleanField(default=False) # False bosa popular emas True bo'lsa popular
    available = models.BooleanField(default=True) # False bosa o'chgan
    is_active = models.BooleanField(default=True) # False bosa bloklangan

    def set_slug(self, title):
        characters = string.ascii_letters + string.digits
        code = "".join(random.choice(characters) for _ in range(6))
        self.slug = slugify(title) + "-" + code
        self.save()


    def str(self):
        return self.title

    class Meta: 
        ordering = ('-priority',)


class Slider(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250, default="", blank=True)
    subtitle = models.CharField(max_length=250, default="", blank=True)
    priority = models.IntegerField(default=0)
    content = models.TextField(default="", blank=True)
    image = ResizedImageField(size=[400, 400], quality=100, upload_to="slider/")

    def str(self):
        return self.category.title if self.category else "-----"

    class Meta: 
        ordering = ('-priority',)

 
class SliderCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default="", blank=True)
    subtitle = models.CharField(max_length=250, default="", blank=True)
    image = ResizedImageField(size=[200, 200], quality=100, upload_to="slider/")


    def str(self):
        return self.category.title if self.category else "-----"


class PopularCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=250, default="", blank=True)
    priority = models.IntegerField(default=0)
    image = ResizedImageField(size=[300, 300], quality=100, upload_to="popular_category/")

    def str(self):
        return self.category.title if self.category else "-----"

    class Meta: 
        ordering = ('-priority',)

 

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=225)
    subtitle = models.CharField(max_length=225, null=True, blank=True)
    slug = models.CharField(max_length=250, default="") 
    company = models.CharField(max_length=225, null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    available_price = models.BooleanField(default=True) # False bosa o'chgan
    discount = models.IntegerField(default=0, null=True, blank=True)
    old_price = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(default=0, null=True, blank=True)
    image_max = ResizedImageField(size=[400, 400], quality=100, upload_to="product/")
    image_min = ResizedImageField(size=[300, 300], quality=100, upload_to="product/")
    available = models.BooleanField(default=True) # False bosa o'chgan
    is_active = models.BooleanField(default=True) # False bosa bloklangan
    popular = models.BooleanField(default=False) # False bosa popular emas True bo'lsa popular
    date_created = models.DateTimeField(auto_now_add=True)
 
    def set_slug(self, title):
        characters = string.ascii_letters + string.digits
        code = "".join(random.choice(characters) for _ in range(6))
        self.slug = slugify(title) + "-" + code
        self.save()


    def str(self):
        return self.title

    class Meta: 
        ordering = ('-priority',)



class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_full = ResizedImageField(size=[400,400], quality=100, upload_to="products/")
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="products/")

    def str(self):
        return self.product.title if self.product else "-----"


class Order(models.Model): 
    order = models.CharField(max_length=225, null=True, blank=True)
    
    def str(self):
        return self.product.title if self.product else "-----"

# # # # # # # # # # # # # # # # # # # # #
# ! INFO WARNING ! 
# # # # # # ########################### 

class Info(models.Model): 
    start_day = models.CharField(max_length=225,null=True, blank=True)
    start_day_time = models.CharField(max_length=225,null=True, blank=True)
    finish_day = models.CharField(max_length=225,null=True, blank=True)
    finish_day_time = models.CharField(max_length=225,null=True, blank=True)
    addition_day = models.CharField(max_length=225,null=True, blank=True)
    addition_day_time = models.CharField(max_length=225,null=True, blank=True)
    address = models.CharField(max_length=225,null=True, blank=True)
    phone_first = models.CharField(max_length=255, null=True, blank=True)
    phone_second = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    instagram_link = models.URLField(null=True, blank=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    telegram_link = models.URLField(null=True, blank=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    youtube_link = models.URLField(null=True, blank=True)
    map = models.TextField()
    
    def str(self):
        return self.instagram
