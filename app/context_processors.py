from .models import ContactInfo , Industry , Service

def get_contact_info(request):
    info = ContactInfo.objects.first()

    services = Service.objects.all()

    industries = Industry.objects.all()

    return {"info":info , "industries":industries , "services":services}