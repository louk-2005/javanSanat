from django.db import models

#django files
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#packages
from PIL import Image

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\d{11}$',
        message="Phone number must be exactly 11 digits."
    )

    ROLE_CHOICES = [
        ('USER', 'کاربر'),
        ('STAFF', 'کارمند'),
    ]
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_regex])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and self.image.name != 'default.png':
            img_path = self.image.path

            img = Image.open(img_path)

            img.thumbnail((300, 300))

            img.save(img_path, optimize=True, quality=85)

    def __str__(self):
        return self.username










class ContactInfo(models.Model):
    NAME_CHOICES = [
        ('Head Office', 'شعبه اصلی'),
        ('Other Branches', 'سایر شعبه ها'),
    ]
    name = models.CharField(choices=NAME_CHOICES, max_length=55, default='FACTORY')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.TextField(verbose_name="communicate with us", blank=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            orig = ContactInfo.objects.filter(pk=self.pk).first()
            orig_image = orig.logo if orig else None
        else:
            orig_image = None

        super().save(*args, **kwargs)

        if self.logo and self.logo != orig_image:
            image_path = self.logo.path
            with Image.open(image_path) as img:
                max_size = (300, 300)
                img.thumbnail(max_size)
                img.save(image_path, quality=85)

    def __str__(self):
        return "Contact information"


class SocialLink(models.Model):
    contact = models.ForeignKey(ContactInfo, related_name='social_links', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="field name")
    url = models.URLField(verbose_name="link url")

    def __str__(self):
        return f"{self.name} - {self.url}"













