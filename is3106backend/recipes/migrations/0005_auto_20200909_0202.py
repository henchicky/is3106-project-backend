# Generated by Django 3.1 on 2020-09-09 02:02

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20200908_1622'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ingredient',
            managers=[
                ('ingredient_list', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe'),
        ),
    ]
