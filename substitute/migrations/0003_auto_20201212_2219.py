# Generated by Django 3.1.4 on 2020-12-12 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0002_product_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='user_favorite', to='substitute.User'),
        ),
    ]