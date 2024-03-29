# Generated by Django 4.1.5 on 2023-01-30 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expenses', '0002_totalexpense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalexpense',
            name='user',
        ),
        migrations.AddField(
            model_name='totalexpense',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
