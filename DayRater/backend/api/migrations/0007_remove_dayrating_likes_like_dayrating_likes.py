# Generated by Django 4.1.4 on 2023-01-11 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_remove_userprofile_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dayrating',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dayrating',
            name='likes',
            field=models.ManyToManyField(related_name='rating', to='api.like'),
        ),
    ]