# Generated by Django 3.1.7 on 2022-06-30 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest', '0002_auto_20220630_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='point',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='horsTaxe',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='toutTaxe',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='devis',
            name='tva',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='horsTaxe',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='toutTaxe',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='facture',
            name='tva',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='remise',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='prod',
            name='article_remise',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='remise_consomateur',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='remise_grossite',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ventes',
            name='remise',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
