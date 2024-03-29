# Generated by Django 4.1.7 on 2023-08-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_stockstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='composition',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(choices=[('26', '26'), ('28', '28'), ('30', '30'), ('32', '32'), ('34 (XS)', '34 (XS)'), ('36 (XS)', '36 (XS)'), ('38 (M)', '38 (M)'), ('40 (M)', '40 (M)'), ('42 (L)', '42 (L)'), ('44 (L)', '44 (L)'), ('46 (XL)', '46 (XL)'), ('48 (XL)', '48 (XL)')], max_length=200),
        ),
    ]
