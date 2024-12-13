from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from stdimage import StdImageField, JPEGField
from stdimage.validators import MinSizeValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Le Nom")

    BENEFICIEAIRE, USER_QONTO = 'B', 'UQ'
    TYPE = [
        (BENEFICIEAIRE, 'Bénéficiaire'),
        (USER_QONTO, 'Utilisateur Qonto')
    ]
    type = models.CharField(
        max_length=3,
        choices=TYPE,
        default=USER_QONTO,
        verbose_name="Type d'utilisateur"
                            )
    compta_admin = models.BooleanField(default=False)


# creating provisional contact model for stimualtion:
class ContactProvisional(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, unique=True, verbose_name='Nom')

    class Meta:
        verbose_name = _('Contact provisoir')

    def __str__(self):
        return self.name

