# Generated by Django 5.1.3 on 2024-11-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlShortener', '0003_alter_urlshortener_custom_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlshortener',
            name='ttl_seconds',
            field=models.IntegerField(default=120, null=True),
        ),
    ]
