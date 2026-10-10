from .models import ContactInfo , Industry , Service , SocialLink

def get_contact_info(request):
    info = ContactInfo.objects.first()

    services = Service.objects.all()[:6]

    industries = Industry.objects.all()[:6]

    socials = SocialLink.objects.all()

    return {"info":info , "industries":industries , "services":services , "socials":socials}