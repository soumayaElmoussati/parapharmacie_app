# Generated by Django 3.1.7 on 2022-09-12 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gest', '0006_auto_20220806_1342'),
    ]

    operations = [

        migrations.CreateModel(
            name='Paiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('montant', models.FloatField(blank=True, null=True)),
                ('commande_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest.facture')),
            ],
        ),
    ]
