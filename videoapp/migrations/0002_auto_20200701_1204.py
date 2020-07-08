# Generated by Django 2.2 on 2020-07-01 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='author',
            field=models.CharField(default='admin', max_length=50),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('entertainment', 'entertainment'), ('tech', 'tech'), ('educational', 'educational'), ('random', 'random'), ('news', 'news')], default='random', max_length=30),
        ),
    ]
