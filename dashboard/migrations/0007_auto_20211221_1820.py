# Generated by Django 3.2.8 on 2021-12-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20211205_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationlink',
            name='valid_until',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='qrcodegenerator',
            name='qr_code',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='qrcodegenerator',
            name='valid_until',
            field=models.DateTimeField(blank=True),
        ),
    ]