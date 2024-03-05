from django.db import models
from django_resized import ResizedImageField


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
    number_first = models.CharField(max_length=100, null=True, blank=True)
    number_second = models.CharField(max_length=100, null=True, blank=True)
    image = ResizedImageField(size=[200, 200], quality=100, upload_to="master/", null=True, blank=True)

    def __str__(self):
        return self.title
 

class FooterSlider(models.Model):
    title = models.CharField(max_length=250)
    image = ResizedImageField(size=[400, 400], quality=100, upload_to="footer_slider/")

    def __str__(self):
        return self.title
