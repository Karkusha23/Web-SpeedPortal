# Generated by Django 4.2.6 on 2023-11-05 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_game_banner_alter_game_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='banner',
            field=models.ImageField(default='default_game_banner.jpg', upload_to='games_banners'),
        ),
    ]