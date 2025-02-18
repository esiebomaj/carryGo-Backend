# Generated by Django 3.1 on 2021-08-12 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20210812_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='category',
            field=models.CharField(blank=True, choices=[('CLOTHS', 'Cloths'), ('DOCUMENTS', 'Documents'), ('GROCERY', 'Grocery'), ('OTHER', 'Other')], max_length=50, null=True, verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='package',
            name='delivery_period',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='delivery period'),
        ),
        migrations.AlterField(
            model_name='package',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='package',
            name='dest_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='delivery address'),
        ),
        migrations.AlterField(
            model_name='package',
            name='package_image',
            field=models.ImageField(blank=True, default='package_images/default.png', null=True, upload_to='package_images/', verbose_name='Package image'),
        ),
        migrations.AlterField(
            model_name='package',
            name='pick_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='pick up address'),
        ),
        migrations.AlterField(
            model_name='package',
            name='priority',
            field=models.CharField(blank=True, choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW')], max_length=50, null=True, verbose_name='Package Priority'),
        ),
        migrations.AlterField(
            model_name='package',
            name='recievers_first_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='recievers first name'),
        ),
        migrations.AlterField(
            model_name='package',
            name='recievers_last_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='recievers last name'),
        ),
        migrations.AlterField(
            model_name='package',
            name='recievers_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='recievers phone number'),
        ),
    ]
