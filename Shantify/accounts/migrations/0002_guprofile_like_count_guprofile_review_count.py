# Generated by Django 4.0.4 on 2022-04-26 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guprofile',
            name='like_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='guprofile',
            name='review_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
