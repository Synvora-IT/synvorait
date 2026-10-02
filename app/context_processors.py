from .models import ContactInfo , Industry , Solution , Service

def get_contact_info(request):
    info = ContactInfo.objects.first()

    solutions = Solution.objects.filter(is_active = True)

    services = Service.objects.all()

    industries = Industry.objects.all()

    return {"info":info , "solutions":solutions , "industries":industries , "services":services}