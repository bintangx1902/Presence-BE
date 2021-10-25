from django.db import models
from django.contrib.auth.models import User


class AgencyName(models.Model):
    name = models.CharField(max_length=255)
    link = models.SlugField(unique=True, max_length=255)
    unique_code = models.CharField(max_length=255)
    desc = models.TextField()

    def __str__(self):
        return self.name


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    identity_number = models.CharField(max_length=255)
    agency = models.ForeignKey(AgencyName, on_delete=models.CASCADE)
    is_controller = models.BooleanField(default=False)
    create_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s mobile : {self.phone_number}"


class QRCodeGenerator(models.Model):
    qr_code = models.TextField()
    valid_until = models.DateTimeField()
    agency = models.ForeignKey(AgencyName, on_delete=models.CASCADE)
    for_date = models.DateField(auto_now_add=True)
    presence = models.ManyToManyField(User, blank=True, related_name='presence')
    is_restrict = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', default=0)

    def __str__(self):
        return f"{self.presence.count()} presence for {self.for_date}"
