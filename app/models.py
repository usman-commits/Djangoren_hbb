from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
import datetime
from import_export import resources 
from django.db.models import JSONField
from django.utils import timezone


DEVICE_CHOICES = (
    ('MIFI','MIFI'),
    ('Router','Router'),
    ('ODU','ODU'),
    ('5G Router','5G Router'),
)



class Broadband(models.Model):
    REGION_CHOICES = [
        ('North East', 'North East'),
        ('North West', 'North West'),
        ('South East', 'South East'),
        ('South South', 'South South'),
        ('Lagos', 'Lagos'),
        ('West', 'West'),
    ]

    STATE_CHOICES = {
        'North East': [
            ('Kano', 'Kano'),
            ('Jigawa', 'Jigawa'),
            ('Bauchi', 'Bauchi'),
            ('Yobe', 'Yobe'),
            ('Borno', 'Borno'),
            ('Adamawa', 'Adamawa'),
            ('Taraba', 'Taraba'),
            ('Gombe', 'Gombe'),
        ],
        'North West': [
            ('Kaduna', 'Kaduna'),
            ('FCT', 'FCT'),
            ('Katsina', 'Katsina'),
            ('Niger', 'Niger'),
            ('Plateau', 'Plateau'),
            ('Kebbi', 'Kebbi'),
            ('Sokoto', 'Sokoto'),
            ('Zamfara', 'Zamfara'),
            ('Kogi', 'Kogi'),
            ('Nasarawa', 'Nasarawa'),
        ],
        'South East': [
            ('Enugu', 'Enugu'),
            ('Imo', 'Imo'),
            ('Anambra', 'Anambra'),
            ('Abia', 'Abia'),
            ('Benue', 'Benue'),
            ('Ebonyi', 'Ebonyi'),
        ],
        'South South': [
            ('Bayelsa', 'Bayelsa'),
            ('Delta', 'Delta'),
            ('Rivers', 'Rivers'),
            ('Akwa Ibom', 'Akwa Ibom'),
            ('Cross River', 'Cross River'),
            ('Edo', 'Edo'),
        ],
        'Lagos': [
            ('Lagos Boundary', 'Lagos Boundary'),
            ('Lagos Island', 'Lagos Island'),
            ('Lagos Mainland', 'Lagos Mainland'),
        ],
        'West': [
            ('Ogun', 'Ogun'),
            ('Ekiti', 'Ekiti'),
            ('Ondo', 'Ondo'),
            ('Osun', 'Osun'),
            ('Kwara', 'Kwara'),
            ('Oyo', 'Oyo'),
        ],
        
    }
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    HSE_name = models.CharField(max_length=50)
    MSISDN = models.IntegerField()
    Customer_name = models.CharField(max_length=50)
    IMEI = models.IntegerField(validators=[MaxValueValidator(999999999999999 ,message='IMEI can not be greater than 15 digits'), 
    MinValueValidator(100000000000000, message='IMEI can not be less than 15 digits') ])
    Alternate = models.IntegerField()
    Device_type = models.CharField(choices=DEVICE_CHOICES, max_length=100)
    Post_date = models.DateTimeField(auto_now_add=True)
    Region = models.CharField(choices=REGION_CHOICES, max_length=100, default='North East')
    State = models.CharField(max_length=100)
    daily_sales_count = models.IntegerField(default=0)
    MIFI = models.IntegerField(default=0)
    Router = models.IntegerField(default=0)
    ODU = models.IntegerField(default=0)
    d5G_Router = models.IntegerField(default=0)
    achieved_previous_month = models.FloatField(default=0.0)

    
    @property
    def total_devices(self):
        return self.MIFI + self.Router + self.ODU + self.d5G_Router

    @property
    def total_percentage_achieved(self):
        target = 50  # Assuming the target is constant at 50 devices
        if target > 0:
            return round((self.total_devices / target) * 100, 2)
        return 0

    @property
    def growth_percentage(self):
        lmtd = self.achieved_previous_month
        if self.total_percentage_achieved > lmtd:
            return round((self.total_percentage_achieved - lmtd), 2)
        elif self.total_percentage_achieved < lmtd:
            return round((lmtd - self.total_percentage_achieved), 2)
        return 0


    def __str__(self):
        return self.HSE_name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    uploaded_photo = models.ImageField(upload_to='uploaded_photos/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class UploadPhoto(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='uploaded_photos')
    uploaded_photo = models.ImageField(upload_to='photos/')
    photo_caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Photo uploaded by {self.user_profile.user.username}'





class ReactivationReport(models.Model):
    HSE_name = models.CharField(max_length=50)
    Total_calls = models.IntegerField()
    Successful_calls = models.IntegerField()
    Unsuccessful_calls = models.IntegerField()
    Successful_bundle = models.IntegerField()
    Post_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.HSE_name


class NccOutLet(models.Model):
    HSE_name = models.CharField(max_length=50)
    Total_certified_outlet = models.IntegerField()
    Outlet_visited = models.IntegerField()
    Outlet_with_device = models.IntegerField()
    Total_devices_in_outlet = models.IntegerField()
    Total_devices_sold = models.IntegerField()
    Post_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.HSE_name



class DeviceRegistrationAnalytics(models.Model):

    DEVICE_CHOICES = (
    ('MIFI','MIFI'),
    ('Router','Router'),
    ('ODU','ODU'),
    ('5G Router','5G Router'),
)
    REGION_CHOICES = [
        ('North East', 'North East'),
        ('North West', 'North West'),
        ('South East', 'South East'),
        ('South South', 'South South'),
        ('Lagos', 'Lagos'),
        ('West', 'West'),
    ]

    
    date = models.DateField(default=timezone.now)
    device_type = models.CharField(choices=DEVICE_CHOICES, max_length=100)
    region = models.CharField(choices=REGION_CHOICES, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.region} - {self.device_type} - {self.user}"





class MainData(models.Model):
    date = models.DateField()
    value = models.CharField(max_length=100)

class ArchivedData(models.Model):
    date = models.DateField()
    value = models.CharField(max_length=100)

