# Generated by Django 5.1.3 on 2024-11-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_created_at_alter_post_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
