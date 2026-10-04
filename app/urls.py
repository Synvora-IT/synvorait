from app.views import index , get_services , get_solutions , solution_detail , service_detail , contact_us , get_industries , blogs , blog_detail , create_blog , project_detail , case_studies , our_team

from django.urls import path

urlpatterns = [
    path("" , index , name = "index"),

    path("solutions/" , get_solutions , name = "solutions"),

    path("services/" , get_services , name = "services"),

    path("solution/<str:slug>/" , solution_detail , name = "solution-detail"),

    path("industries/" , get_industries , name = "industries"),

    path("case-studies/" , case_studies , name = "case-studies"),

    path("our-team/" , our_team , name = "our-team"),

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