# Generated by Django 5.0.4 on 2024-04-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts_images/', verbose_name='Изображение'),
        ),
    ]
