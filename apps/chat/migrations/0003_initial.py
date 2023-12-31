# Generated by Django 5.0 on 2023-12-08 14:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0002_initial'),
        ('freelancer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='freelmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freel_messages', to='freelancer.freelancer'),
        ),
        migrations.AddField(
            model_name='room',
            name='current_cust',
            field=models.ManyToManyField(blank=True, related_name='cust_current_rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='room',
            name='current_freel',
            field=models.ManyToManyField(blank=True, related_name='freel_current_rooms', to='freelancer.freelancer'),
        ),
        migrations.AddField(
            model_name='room',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='freelmessage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freel_messages', to='chat.room'),
        ),
        migrations.AddField(
            model_name='custmessage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cust_messages', to='chat.room'),
        ),
    ]
