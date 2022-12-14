# Generated by Django 3.2 on 2022-09-15 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='description',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='image',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='name',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='price',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='rating',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='products',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='username',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
