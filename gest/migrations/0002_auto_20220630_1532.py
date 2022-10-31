# Generated by Django 3.1.7 on 2022-06-30 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annuler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('produit', models.CharField(max_length=9000)),
                ('remise', models.IntegerField(blank=True, null=True)),
                ('prix', models.FloatField(blank=True, null=True)),
                ('quantite', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=9000)),
                ('telephone', models.CharField(blank=True, max_length=9000, null=True)),
                ('email', models.CharField(blank=True, max_length=9000, null=True)),
                ('ice', models.CharField(max_length=800, null=True)),
                ('abreviation', models.CharField(blank=True, max_length=250, null=True)),
                ('adresse', models.CharField(blank=True, max_length=650, null=True)),
                ('ville', models.CharField(blank=True, max_length=250, null=True)),
                ('point', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Devis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, max_length=9000, null=True)),
                ('description', models.TextField(blank=True, max_length=9000, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('commercant', models.CharField(blank=True, max_length=100, null=True)),
                ('montant', models.CharField(blank=True, max_length=9000, null=True)),
                ('piedPage', models.TextField(blank=True, max_length=9999, null=True)),
                ('horsTaxe', models.FloatField(blank=True, default=1, null=True)),
                ('tva', models.FloatField(blank=True, default=1, null=True)),
                ('toutTaxe', models.FloatField(blank=True, default=1, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gest.client')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, max_length=9000, null=True)),
                ('type_facture', models.CharField(choices=[('AVOIR', 'AVOIR'), ('DUE', 'DUE')], default='DUE', max_length=90)),
                ('description', models.TextField(blank=True, max_length=9000, null=True)),
                ('commercant', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('montant', models.CharField(blank=True, max_length=9000, null=True)),
                ('mode_paiment', models.CharField(blank=True, choices=[('ESPECE', 'ESPECE'), ('CREANCE', 'CREANCE')], default='Impayee', max_length=9000, null=True)),
                ('piedPage', models.TextField(blank=True, max_length=9999, null=True)),
                ('statut', models.CharField(blank=True, choices=[('Impayee', 'Impayee'), ('Payee', 'Payee')], default='Impayee', max_length=9000, null=True)),
                ('horsTaxe', models.FloatField(blank=True, default=1, null=True)),
                ('is_Facture', models.BooleanField(default=False)),
                ('num_facture', models.IntegerField(blank=True, null=True)),
                ('is_Bl', models.BooleanField(default=False)),
                ('num_bl', models.IntegerField(blank=True, null=True)),
                ('tva', models.FloatField(blank=True, default=1, null=True)),
                ('toutTaxe', models.FloatField(blank=True, default=1, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gest.client')),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=9000)),
                ('telephone', models.CharField(blank=True, max_length=9000, null=True)),
                ('email', models.CharField(blank=True, max_length=9000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ventes',
            name='ref',
        ),
        migrations.AddField(
            model_name='panier',
            name='p_remise',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='panier',
            name='p_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='panier',
            name='prix',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='p_achat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='refer',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='remise_consomateur',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='remise_grossite',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='tva',
            field=models.IntegerField(blank=True, choices=[(0, 0), (7, 7), (10, 10), (14, 14), (20, 20)], null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='unite',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AddField(
            model_name='ventes',
            name='p_remise',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ventes',
            name='pay',
            field=models.CharField(blank=True, choices=[('ESPECE', 'ESPECE'), ('DETTE', 'DETTE')], max_length=9000, null=True),
        ),
        migrations.AddField(
            model_name='ventes',
            name='remise',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='panier',
            name='nom',
            field=models.CharField(default=None, max_length=9000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='categorie',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='gest.categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_expire',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ventes',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='ventes',
            name='produit',
            field=models.CharField(max_length=9000),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produit', models.CharField(max_length=9000)),
                ('date', models.DateField(blank=True, null=True)),
                ('prix_achat', models.FloatField(blank=True, null=True)),
                ('prix_vente', models.FloatField(blank=True, null=True)),
                ('quantite', models.IntegerField(blank=True, null=True)),
                ('nom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest.product')),
            ],
        ),
        migrations.CreateModel(
            name='Prod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('article', models.CharField(blank=True, max_length=9000, null=True)),
                ('article_quantite', models.IntegerField(blank=True, null=True)),
                ('article_prix', models.FloatField(blank=True, null=True)),
                ('article_remise', models.FloatField(blank=True, default=1, null=True)),
                ('article_total', models.FloatField(blank=True, null=True)),
                ('devis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gest.devis')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('remise', models.IntegerField(blank=True, default=1, null=True)),
                ('prix', models.FloatField(blank=True, null=True)),
                ('p_remise', models.FloatField(blank=True, null=True)),
                ('quantite', models.IntegerField(blank=True, default=1, null=True)),
                ('p_total', models.FloatField(blank=True, null=True)),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gest.facture')),
                ('nom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='one', to='gest.product')),
            ],
        ),
        migrations.CreateModel(
            name='Dette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField()),
                ('numero_facture', models.CharField(blank=True, max_length=9000, null=True)),
                ('date', models.DateField()),
                ('montant', models.FloatField(blank=True, null=True)),
                ('raison', models.CharField(blank=True, default='Impayer', max_length=9000, null=True)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='Creance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField()),
                ('date', models.DateField()),
                ('montant', models.FloatField(blank=True, null=True)),
                ('raison', models.CharField(blank=True, max_length=9000, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest.client')),
            ],
        ),
        migrations.AddField(
            model_name='ventes',
            name='client',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='gest.client'),
            preserve_default=False,
        ),
    ]
