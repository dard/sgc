from django.contrib.auth.models import AbstractUser
from django.db import models
from SGC.settings import MEDIA_URL, STATIC_URL
from django.conf import settings

# Create your models here.


class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE, related_name='user_creation', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE, related_name='user_update', null=True, blank=True)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class User (AbstractUser):
    imagen = models.ImageField(upload_to='cheque/%Y/%m/%d', null=True, blank=True)

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(STATIC_URL, 'img/empty.png')
