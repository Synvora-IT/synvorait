"""
URL configuration for synvora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('session/', include("session.urls")),
    path('summernote/', include("django_summernote.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

from app.views import index , get_services , get_solutions , solution_detail , service_detail , contact_us , get_industries , blogs , blog_detail , create_blog , project_detail , case_studies

urlpatterns += [
    path("" , index , name = "index"),

    path("solutions/" , get_solutions , name = "solutions"),

    path("services/" , get_services , name = "services"),

    path("solution/<str:slug>/" , solution_detail , name = "solution-detail"),

    path("industries/" , get_industries , name = "industries"),

    path("case-studies/" , case_studies , name = "case-studies"),

    path("project/<str:slug>/" , project_detail , name = "project-detail"),

    path("service/<str:slug>/" , service_detail , name = "service-detail"),

    path("blogs/" , blogs , name = "blogs"),

    path("create-blog/" , create_blog , name = "create-blog"),

    path("blog-detail/<str:slug>/" , blog_detail , name = "blog-detail"),

    path("contact-us/" , contact_us , name = "contact-us"),

]


# User specific
from app.views import my_projects , add_project

urlpatterns += [
    path("my-projects/" , my_projects , name = "my-projects"),

    path("add-project/" , add_project , name = "add-project"),
]