from django.db.models.signals import post_save

from django.dispatch import receiver

from .models import Message

from core.services.send_mail import EmailService

from threading import Thread

@receiver(post_save , sender = Message)
def send_email(sender, instance , created , **kwargs):

    if created:

        subject = "Thanks for reaching out to us"

        body = f"Hey, {instance.name}\nWe got your message. We will message you via email and cell phone"

        to = [instance.email,]

        email_thread = Thread(target = EmailService.send_mail , args = [to,subject,body])

        email_thread.start()