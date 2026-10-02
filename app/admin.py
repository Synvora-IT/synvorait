from django.contrib import admin
from .models import *

admin.site.site_header = "Synvora IT"
admin.site.site_title = "Synvora IT Admin"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title" , "start_date" , "end_date"]

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ["title"]

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ["title" , "is_active"]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title" , "is_active"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["name" , "email" , "is_active" , "created_at"]

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["title" , "url"]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name" , "email" , "phone" , "subject" , "is_read" , "created_at"]


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["phone" , "email" , "location"]

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name" , "code"]

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ["title"]

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["user" , "title" , "created_at"]