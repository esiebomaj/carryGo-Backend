# Generated by Django 3.1 on 2020-09-29 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_transaction_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_credit',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
