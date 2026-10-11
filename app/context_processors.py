from .models import ContactInfo , Industry , Service , SocialLink

def get_contact_info(request):
    info = ContactInfo.objects.first()

    nav_services = Service.objects.all()[:6]

    nav_industries = Industry.objects.all()[:6]

    socials = SocialLink.objects.all()

    return {"info":info , "nav_industries":nav_industries , "nav_services":nav_services , "socials":socials}