from django.contrib.auth import get_user_model

from django.dispatch import receiver

from django.db.models.signals import post_save

from threading import Thread

from core.services.send_mail import EmailService

from .models import ActivationCode

User = get_user_model()


@receiver(signal = post_save , sender = User)
def create_activation_key(sender , instance , created , *args , **kwargs):
    if created:
        activation_key = ActivationCode.objects.create(user = instance)
        return

@receiver(signal=post_save, sender=ActivationCode)
def send_email_signal(sender, instance, created, *args, **kwargs):

    if created:

        activation_url = f"localhost:8000/session/activate-account/{instance.id}/{instance.code}/"

        email_thread = Thread(
            target=EmailService.send_mail,
            args=(
                [instance.user.email,],
                "Activate your account",
                "",
                "email/activation.html"
            ),
            kwargs={
                "context": {
                    "full_name": instance.user.get_full_name(),
                    "activation_url": activation_url,
                }
            }
        )

        email_thread.start()
