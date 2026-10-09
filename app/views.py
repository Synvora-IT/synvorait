from django.shortcuts import render , get_object_or_404 , redirect

from .models import Technology , Industry , Review , Service , Project , Blog

from django.views.decorators.http import require_GET

from django.core.paginator import Paginator

from .forms import BlogForm , ProjectForm , MessageForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required

from session.models import TeamMember

from django.contrib import messages

from django.db.models import Avg

@require_GET
def index(request):
    technologies = Technology.objects.all()

    reviews = Review.objects.filter(is_active = True)

    context = {
        "technologies":technologies,

        "reviews":reviews,

    }

    return render(request , "index.html" , context)


@require_GET
def get_industries(request):
    industries = Industry.objects.all()
    context = {"industries":industries}
    return render(request , "industries.html" , context)

@require_GET
def get_services(request):
    services = Service.objects.all()

    total_member = TeamMember.objects.filter(is_active = True).count()

    total_project = Project.objects.all().count()
    
    context = {"services":services , "total_member":total_member , "total_project":total_project}

    return render(request , "services.html" , context)

@require_GET
def service_detail(request , slug):
    service = get_object_or_404(Service , slug = slug)
    return render(request , "service-detail.html" , {"service":service})

@require_GET
def case_studies(request):

    projects = (
        Project.objects
        .select_related("service")
        .prefetch_related("technologies")
    )

    cases = []

    for project in projects:

        cases.append({
            "id": project.id,
            "slug": project.slug,

            "client": project.client,

            "title": project.title,

            "summary": project.short_description,

            "description": project.description,

            # Service / Category
            "cat": (
                project.service.title
                if project.service
                else None
            ),

            # Single project image
            "image": (
                project.image.url
                if project.image
                else None
            ),

            # Technologies
            "stack": list(
                project.technologies.values_list(
                    "name",
                    flat=True
                )
            ),

            "start_date": (
                project.start_date.isoformat()
                if project.start_date
                else None
            ),

            "end_date": (
                project.end_date.isoformat()
                if project.end_date
                else None
            ),
        })

    context = {
        "cases": cases
    }

    return render(
        request,
        "case_study.html",
        context
    )


@require_GET
def project_detail(request , slug):
    project = get_object_or_404(Project , slug = slug)
    return render(request , "project-detail.html" , {"project":project})

@require_GET
def our_team(request):
    members = list(TeamMember.objects.filter(is_active = True).values("user__first_name" , "user__last_name" , "user__image","designation__name"))
    return render(request , "our-team.html" , {"members":members})

def contact_us(request):

    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request , "We've sent you a email")
            return redirect("contact-us")

        else:
            messages.warning(request , "Invalid form")

    return render(request , "contact-us.html" , {"form":form})

def about_us(request):

    total_member = TeamMember.objects.filter(is_active = True).count()

    total_project = Project.objects.all().count()

    context = {"total_member":total_member , "total_project":total_project}

    return render(request , "about-us.html" , context)

def reviews(request):
    page = request.GET.get("page" , 1)

    user_reviews = Review.objects.filter(is_active = True).order_by("-created_at")

    avg_rating = user_reviews.aggregate(avg_rating = Avg("rating"))

    paginator = Paginator(user_reviews , 20)

    user_reviews = paginator.get_page(page)

    return render(request , "reviews.html" , {"reviews":user_reviews , "avg_rating":avg_rating})

@login_required(login_url = "login")
def my_projects(request):

    if request.user.user_type != 'teammate':
        return redirect('index')

    page = request.GET.get("page" , 1)

    try:page = int(page)
    except(ValueError , TypeError):page = 1

    projects  = Project.objects.filter(user = request.user)

    search = request.GET.get("search" , None)

    if search:
        projects = projects.filter(title__icontains = search)

    paginator = Paginator(projects , 10)

    projects = paginator.get_page(page)

    context = {"projects":projects}

    return render(request , "my-projects.html" , context)


@login_required(login_url = "login")
def add_project(request):
    if request.user.user_type != 'teammate':
        return redirect('index')
    
    form = ProjectForm()
    
    if request.method == "POST":
        form = ProjectForm(data = request.POST , files = request.FILES)

        if form.is_valid():
            technologies = form.cleaned_data.pop("technologies")

            project = form.save(commit = False)

            project.user = request.user

            project.save()

            project.technologies.set(technologies)

            return redirect("project-detail" , project.slug)

    return render(request , "add-project.html" , {"form":form})            


@require_GET
def blogs(request):
    search = request.GET.get("search" , None)

    page = request.GET.get("page" , 1)

    try:page = int(page)

    except(ValueError , TypeError):page = 1

    blogs = Blog.objects.all()

    if search:
        blogs = blogs.filter(Q(title__icontains = search) | Q(tags__title__icontains = search))

    paginator = Paginator(blogs , 20)

    blogs = paginator.get_page(page)

    context = {"blogs":blogs}

    return render(request , "blogs.html" , context)

@require_GET
def blog_detail(request , slug):
    blog = get_object_or_404(Blog , slug = slug)

    context = {"blog":blog}

    return render(request , "blog-detail.html" , context)

@login_required(login_url = "login")
def create_blog(request):

    form = BlogForm()

    if request.method == "POST":
        form = BlogForm(data = request.POST , files = request.FILES)

        if form.is_valid():
            blog = form.save(commit = False)
            blog.user = request.user
            blog.save()

    return render(request , "create-blog.html" , {"form":form})