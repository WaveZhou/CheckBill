# Generated by Django 3.2.8 on 2021-10-20 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrive',
            name='end_date',
            field=models.DateField(null=True, verbose_name='结束日期'),
        ),
        migrations.AlterField(
            model_name='arrive',
            name='start_date',
            field=models.DateField(null=True, verbose_name='开始日期'),
        ),
        migrations.AlterField(
            model_name='arrive',
            name='status',
            field=models.IntegerField(null=True, verbose_name='有效标志'),
        ),
    ]
