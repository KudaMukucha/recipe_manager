# Generated by Django 4.2.7 on 2024-10-16 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_recipe_recipe_of_the_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_of_the_day',
        ),
    ]
