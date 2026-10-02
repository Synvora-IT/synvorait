from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings

from core.services import rand_code, expiry_date

import uuid

class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    image = models.ImageField(upload_to = "user_images" , blank = True , null = True)

    class UserRoles(models.TextChoices):
        TEAMMATE = "teammate" , "Team Mate"
        CLIENT = "client" , "Client"

    user_type = models.CharField(max_length = 20 , choices = UserRoles.choices , default = UserRoles.CLIENT)



_expiry_date = expiry_date.generate_expiry_date(minutes = 20)

class ActivationCode(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    code = models.CharField(default = rand_code.generate_random_code, max_length = 6)

    created_at = models.DateTimeField(auto_now_add = True)

    expiry_date = models.DateTimeField(default = _expiry_date)

    def __str__(self):
        return f"Code for {self.user}"
    