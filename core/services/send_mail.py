from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.conf import settings

class EmailService:

    @staticmethod
    def send_mail(to, subject:str, body:str = None, template_name:str = None , context:dict = None):

        email = EmailMultiAlternatives(subject = subject , body = body or "", to = to, from_email = settings.EMAIL_HOST_USER)

        if template_name:
            html_content = render_to_string(
                template_name = template_name,

                context = context or {}
            )

            email.attach_alternative(html_content,  "text/html")

        email.send()
        
