# Generated by Django 2.2 on 2020-07-07 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoapp', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
    ]