# Generated by Django 4.1.7 on 2023-05-24 20:43

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_url', models.TextField(blank=True, max_length=2000, validators=[django.core.validators.URLValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_body', models.TextField(blank=True, max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_poster_url', models.TextField(blank=True, max_length=2000, validators=[django.core.validators.URLValidator()])),
                ('video_url', models.TextField(blank=True, max_length=2000, validators=[django.core.validators.URLValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_id', models.CharField(default='v3032400', max_length=10, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('price_per_head', models.CharField(max_length=5)),
                ('description', models.TextField(blank=True)),
                ('features', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=3000), blank=True, default=list, size=None)),
                ('city', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Restaurent', 'Restaurent'), ('Marquee', 'Marquee'), ('Auditorium', 'Auditorium')], max_length=10)),
                ('logo_url', models.TextField(blank=True, max_length=2000, validators=[django.core.validators.URLValidator()])),
                ('virtual_tour_url', models.TextField(blank=True, max_length=2000, validators=[django.core.validators.URLValidator()])),
                ('phone_number', models.CharField(max_length=20)),
                ('whatsapp_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('capacity', models.CharField(blank=True, max_length=10)),
                ('terms_conditions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), blank=True, default=list, size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_gallery', models.ManyToManyField(blank=True, to='venues.imagegallery')),
                ('video_gallery', models.ManyToManyField(blank=True, to='venues.videogallery')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('unlikes', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_like', to='venues.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venue_review', to='venues.venue'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rating', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venue_rating', to='venues.venue')),
            ],
        ),
    ]
