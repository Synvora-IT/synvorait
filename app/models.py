from django.db import models

from django_summernote.fields import SummernoteTextField

from django.utils.text import slugify

from django.core.exceptions import ValidationError

from django_summernote.fields import SummernoteTextField

from django.core.validators import MinValueValidator , MaxValueValidator

from django.conf import settings


class Industry(models.Model):
    title = models.CharField(max_length = 50)

    banner = models.ImageField(upload_to = "solution_banners/" , blank = True , null = True)

    short_description = models.CharField(max_length = 100 , blank = True , null = True)

    description = SummernoteTextField(blank = True , null = True)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.title

class Technology(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Technologies"


class Service(models.Model):
    slug = models.SlugField(blank = True , null = True)

    title = models.CharField(max_length = 100)

    banner = models.ImageField(upload_to = "service_images/")

    technologies = models.ManyToManyField(Technology , related_name = "services")

    short_description = models.TextField()

    description = SummernoteTextField(blank = True , null = True)

    is_active = models.BooleanField(default = True)


    def __str__(self):
        return self.title

    def save(self, *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args , **kwargs)

class Project(models.Model):
    slug = models.SlugField(blank = True , null = True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.SET_NULL , blank = True , null = True, related_name = "dev_proejcts")

    user_client = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.SET_NULL , blank = True , null = True , related_name = "client_proejcts")

    client = models.CharField(max_length = 100 , blank = True , null = True)

    title = models.CharField(max_length = 120)

    image = models.ImageField(upload_to = "project_images/" , blank = True , null = True)

    short_description = models.CharField(max_length = 100)
    
    description = SummernoteTextField(blank = True , null = True)

    service = models.ForeignKey(Service , related_name = "projects" , on_delete = models.SET_NULL , blank = True , null = True)

    technologies = models.ManyToManyField(Technology , related_name = "projects")

    start_date = models.DateField(blank = True , null = True)

    end_date = models.DateField(blank = True , null = True)

    def __str__(self):
        return self.title

    def save(self, *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args , **kwargs)

class Review(models.Model):
    name = models.CharField(max_length = 60)

    image = models.ImageField(upload_to = "reviewer_image/" , blank = True , null = True)

    email = models.EmailField()

    detail = models.TextField()

    rating = models.PositiveIntegerField(validators = [MinValueValidator(1) , MaxValueValidator(5)] , blank = True , null = True)

    occupation = models.CharField(max_length = 30 , blank = True , null = True)

    created_at = models.DateTimeField(auto_now_add = True)

    is_active = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} : {self.created_at.date}"
    
class ContactInfo(models.Model):
    phone = models.CharField(max_length = 13 , unique = True)

    email = models.EmailField(unique = True)

    location = models.CharField(max_length = 200 , blank = True , null = True)

    class Meta:
        verbose_name_plural = "Contact Infoes"

class SocialLink(models.Model):
    title = models.CharField(max_length = 20)

    url = models.URLField(unique = True)

    def __str__(self):
        return self.title


class Country(models.Model):
    name = models.CharField(max_length = 50)

    code = models.CharField(max_length = 3 , unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class GenderTextChoices(models.TextChoices):
    MALE = "male" , "Male"

    FEMALE = "female" , "Female"

class Message(models.Model):
    name = models.CharField(max_length = 50)

    email = models.EmailField()

    country = models.ForeignKey(Country , on_delete = models.CASCADE , blank = True , null = True)

    gender = models.CharField(max_length = 6 , choices = GenderTextChoices.choices)

    phone = models.CharField(max_length = 20)

    service = models.ForeignKey(Service , on_delete = models.CASCADE , blank = True , null = True)

    subject = models.CharField(max_length = 100)

    body = models.TextField()

    is_read = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now_add = True)


    class Meta:
        ordering = ["-created_at"]


class BlogTag(models.Model):
    title = models.CharField(max_length = 30)

    def __str__(self):
        return self.title

    def clean(self , *args , **kwargs):
        qs = self.objects.filter(title__iexact = self.title)

        if self.pk:
            qs = qs.exclude(pk = self.pk)

        if qs:
            raise ValidationError("Tag with this title is already exists")

        super().save(*args , **kwargs)

class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.SET_NULL , null = True , related_name = "blogs")

    slug = models.SlugField(blank = True , null = True)

    title = models.CharField(max_length = 100)

    banner = models.ImageField(upload_to = "blog_image/" , blank = True)

    tags = models.ManyToManyField(BlogTag , blank = True , related_name = "blogs")

    short_description = models.TextField(max_length = 200)

    description = SummernoteTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args , **kwargs)

    class Meta:
        ordering = ["-created_at"]