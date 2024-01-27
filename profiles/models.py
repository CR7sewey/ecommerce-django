from django.db import models
from django.contrib.auth.models import User
from utils.cc_validator import valida_cc
from django.forms import ValidationError
import re
# Create your models here.


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birth_date = models.DateField()
    cc = models.CharField(max_length=11)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=30)
    local = models.CharField(max_length=30)
    nif = models.CharField(max_length=8)
    city = models.CharField(max_length=30)
    district = models.CharField(
        default='',
        max_length=2,
        choices=(('AV', 'Aveiro'),
                 ('BJ', 'Beja'),
                 ('BR', 'Braga'),
                 ('BG', 'Bragança'),
                 ('CA', 'Castelo Branco'),
                 ('CB', 'Coimbra'),
                 ('EV', 'Évora'),
                 ('FA', 'Faro'),
                 ('PO', 'Portalegre'),
                 ('SA', 'Santarém'),
                 ('SE', 'Setúbal'),
                 ('VR', 'Vila Real'),
                 ('VI', 'Viseu'),
                 )
    )

    # para levantar exceccao na validacao
    # antes de fazer save faz este clean
    def clean(self) -> None:
        error_messages = {}
        val = valida_cc(self.cc)
        if not val:
            error_messages['cc'] = 'Invalid cc!'

        if re.search(r'[^0-9]', self.nif) or len(self.nif) != 8:
            error_messages['nif'] = 'Invalid nif, put 8 numbers!'

        if error_messages:
            raise ValidationError(error_messages)

        return super().clean()

    def __str__(self) -> str:
        if self.user.first_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return f'{self.user}'
