# Generated by Django 4.1.7 on 2023-06-03 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='number',
        ),
        migrations.AddField(
            model_name='user',
            name='number',
            field=models.CharField(default=3056496364, max_length=15),
            preserve_default=False,
        ),
    ]
