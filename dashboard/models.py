from django.db import models
from django.contrib.auth.models import User
from os import path, remove
from PIL import ImageDraw, Image
import qrcode, pytz, datetime
from io import BytesIO
from django.core.files import File
from django.conf import settings


class AgencyName(models.Model):
    name = models.CharField(max_length=255)
    link = models.SlugField(unique=True, max_length=255)
    unique_code = models.CharField(max_length=255)
    desc = models.TextField()
    img = models.FileField(upload_to='agency/', blank=True)

    def __str__(self):
        return self.name


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', related_query_name='user')
    phone_number = models.CharField(max_length=255)
    identity_number = models.CharField(max_length=255)
    agency = models.ForeignKey(AgencyName, on_delete=models.CASCADE, blank=True, null=True)
    is_controller = models.BooleanField(default=False)
    create_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s mobile : {self.phone_number}"


class QRCodeGenerator(models.Model):
    qr_code = models.SlugField(unique=True)
    valid_until = models.DateTimeField(blank=True)
    agency = models.ForeignKey(AgencyName, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', default=0)
    qr_img = models.FileField(blank=True, upload_to='qr/')

    def save(self, *args, **kwargs):
        code_img = qrcode.make(self.qr_code)
        canvas = Image.new('RGB', (600, 600), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(code_img)
        f_name = f"qr_generated_{self.qr_code}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_img.save(f_name, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def delete(self, using=None, *args, **kwargs):
        remove(path.join(settings.MEDIA_ROOT, self.qr_img.name))
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.qr_code


class PresenceRecap(models.Model):
    qr = models.ForeignKey(QRCodeGenerator, on_delete=models.CASCADE, related_name='qr_c', related_query_name='qr_c')
    user = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"presence at {self.time_stamp.strftime('%a %H:%M  %d/%m/%y')}"


class InvitationLink(models.Model):
    link = models.SlugField(max_length=255, unique=True)
    valid_until = models.DateTimeField(blank=True)
    agency = models.ForeignKey(AgencyName, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.link
