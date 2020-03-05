# Generated by Django 2.2.10 on 2020-02-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('currency', models.PositiveSmallIntegerField(choices=[(1, 'USD'), (2, 'EUR')])),
                ('buy', models.DecimalField(decimal_places=2, max_digits=4)),
                ('sale', models.DecimalField(decimal_places=2, max_digits=4)),
                ('source', models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank')])),
            ],
        ),
    ]
