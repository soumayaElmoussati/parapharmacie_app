from statistics import mode
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models import F
import datetime

today = datetime.datetime.now().day
month = datetime.datetime.now().month
year = datetime.datetime.now().year
# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=800)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    TVA = (
        (0, 0),
        (7, 7),
        (10, 10),
        (14, 14),
        (20, 20),

    )
    refer = models.CharField(max_length=900, blank=True, null=True)
    name = models.CharField(max_length=9000)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, default=2)
    prix = models.FloatField(blank=True, null=True)
    p_achat = models.FloatField(blank=True, null=True)
    date_expire = models.DateField(null=True, blank=True)
    tva = models.IntegerField(null=True, blank=True, choices=TVA)
    remise_consomateur = models.FloatField(blank=True, null=True, default=0)
    remise_grossite = models.FloatField(blank=True, null=True, default=0)
    unite = models.CharField(max_length=900, null=True, blank=True)
    quantity = models.IntegerField(blank=True, null=True)
    codeBarre = models.CharField(max_length=9000, blank=True, null=True)

    def __str__(self):
        return str(self.name)+"-"+str(self.codeBarre)

class Ventes(models.Model):
    PFA = (
        ('ESPECE', 'ESPECE'),
        ('DETTE', 'DETTE'),
    )
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    produit = models.CharField(max_length=9000)
    pay = models.CharField(max_length=9000, null=True, blank=True, choices=PFA)
    remise = models.IntegerField(blank=True, null=True, default=0)
    prix = models.FloatField(blank=True, null=True)
    p_remise = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)

    
class Panier(models.Model):

    nom = models.CharField(max_length=9000)
    remise = models.IntegerField(blank=True, null=True, default=0)
    prix = models.FloatField(blank=True, null=True)
    p_remise = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True, default=1)
    p_total = models.FloatField(blank=True, null=True)


class Annuler(models.Model):

    date = models.DateTimeField(auto_now=True, blank=True)
    produit = models.CharField(max_length=9000)
    remise = models.IntegerField(blank=True, null=True)
    prix = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)


class Fournisseur(models.Model):

    nom = models.CharField(max_length=9000)
    telephone = models.CharField(max_length=9000, blank=True, null=True)
    email = models.CharField(max_length=9000, blank=True, null=True)
    def __str__(self):
        return self.nom

class Client(models.Model):

    nom = models.CharField(max_length=9000)
    telephone = models.CharField(max_length=9000, blank=True, null=True)
    email = models.CharField(max_length=9000, blank=True, null=True)
    ice = models.CharField(max_length=800, blank=False, null=True)
    abreviation = models.CharField(max_length=250, blank=True, null=True)
    adresse = models.CharField(max_length=650, blank=True, null=True)
    ville = models.CharField(max_length=250, blank=True, null=True)
    point = models.IntegerField(blank=True, null=True, default=0)
    def __str__(self):
        return self.nom

class Dette(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date_creation = models.DateField()
    numero_facture = models.CharField(max_length=9000, blank=True, null=True)
    date = models.DateField()
    montant = models.FloatField(blank=True, null=True)
    raison = models.CharField(max_length=9000, blank=True, null=True, default='Impayer')

class Creance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_creation = models.DateField()
    date = models.DateField()
    montant = models.FloatField(blank=True, null=True)
    raison = models.CharField(max_length=9000, blank=True, null=True)


class Stock(models.Model):

    nom = models.ForeignKey(Product, on_delete=models.CASCADE)
    produit = models.CharField(max_length=9000)
    date = models.DateField(blank=True, null=True)
    prix_achat = models.FloatField(blank=True, null=True)
    prix_vente = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.produit = ""
        self.produit = str(self.date)+" "+str(self.produit)
        return super(Stock, self).save(*args, **kwargs)

class Order(models.Model):
    facture = models.ForeignKey('Facture', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    nom = models.ForeignKey(Product, related_name="one", on_delete=models.SET_NULL, null=True, blank=True)
    remise = models.IntegerField(blank=True, null=True, default=0)
    prix = models.FloatField(blank=True, null=True)
    tva_order = models.FloatField(blank=True, null=True)
    p_remise = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True, default=1)
    p_total = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.facture.type_facture == "AVOIR":
            producta = Product.objects.get(name=self.nom.name)
            Product.objects.filter(pk=producta.pk).update(quantity=F('quantity') + int(self.quantite))
        else:
            producta = Product.objects.get(name=self.nom.name)
            Product.objects.filter(pk=producta.pk).update(quantity=F('quantity') - int(self.quantite))
 
        if self.quantite == None:
            self.quantite = 0
        try:
            prx = Product.objects.get(name=self.nom.name)
            faprix = prx.prix
            if prx.tva == None:
                tvaprod = 20
            else:
                tvaprod = int(prx.tva)
            
            self.prix = faprix
        except Product.DoesNotExist:
            self.prix = 0
        self.p_remise = prx.remise_grossite
        remised = (self.prix * self.remise)/100
        plm = (self.prix - remised) * self.quantite
        self.tva_order = float((plm*tvaprod)/100)
        self.p_total = plm
        fac = Facture.objects.filter(ref=self.facture)
        super(Order, self).save(*args, **kwargs)

class Prod(models.Model):
    devis = models.ForeignKey('Devis', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    article = models.CharField(max_length=9000,null=True, blank=True)
    article_quantite = models.IntegerField(blank=True, null=True)
    article_prix = models.FloatField(blank=True, null=True)
    article_remise = models.FloatField(blank=True, null=True, default=0)
    article_total = models.FloatField(blank=True, null=True)
    def save(self, *args, **kwargs):

        self.article_total = self.article_prix * self.article_quantite

        super(Prod, self).save(*args, **kwargs)

class Facture(models.Model):
    CHOICES = (
        ('ESPECE', 'ESPECE'),
        ('CREANCE', 'CREANCE'),
    )
    TYPE = (
        ('AVOIR', 'AVOIR'),
        ('DUE', 'DUE'),

    )
    CHOICES_STATUTS = (
    ('Impayee', 'Impayee'),
    ('Payee', 'Payee'),
    )
    ref = models.CharField(max_length=9000, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    type_facture = models.CharField(max_length=90, choices=TYPE, default="DUE")
    description = models.TextField(max_length=9000, blank=True, null=True)
    commercant = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    montant = models.CharField(max_length=9000, blank=True, null=True)
    mode_paiment = models.CharField(max_length=9000, blank=True, null=True, choices=CHOICES, default="Impayee")
    piedPage = models.TextField(max_length=9999, blank=True, null=True)
    statut = models.CharField(max_length=9000, blank=True, null=True, choices=CHOICES_STATUTS, default="Impayee")  
    horsTaxe = models.FloatField(blank=True, null=True, default=0)
    is_Facture = models.BooleanField(default=False)
    num_facture = models.IntegerField(blank=True, null=True)
    is_Bl = models.BooleanField(default=False)
    num_bl = models.IntegerField(blank=True, null=True)
    tva = models.FloatField(null=True, blank=True, default=0)
    toutTaxe = models.FloatField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        fgh = Facture.objects.all().last()
        
        if fgh == None:
            fa = 0
        else:
            fa = int(fgh.id)
        self.ref = str("#{}".format(str(fa+1).zfill(8)))
        if Order.objects.filter(facture=self.pk).aggregate(Sum('p_total')).get('p_total__sum') == None:
            sumHorsTaxe = 0
        else:
            sumHorsTaxe = Order.objects.filter(facture=self.pk).aggregate(Sum('p_total')).get('p_total__sum')
        if Order.objects.filter(facture=self.pk).aggregate(Sum('tva_order')).get('tva_order__sum') == None:
            tvatotal = 0
        else:
            tvatotal = Order.objects.filter(facture=self.pk).aggregate(Sum('tva_order')).get('tva_order__sum')

        refe = Facture.objects.filter(ref=self.ref)
        if refe.exists():
            pass
        else:
            
            self.horsTaxe = sumHorsTaxe
            if self.horsTaxe == None:
                pass
            else:
                self.tva = tvatotal
                self.toutTaxe = sumHorsTaxe
            
        super(Facture, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.ref)

class Devis(models.Model):

    ref = models.CharField(max_length=9000, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=9000, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    commercant = models.CharField(max_length=100, null=True, blank=True)
    montant = models.CharField(max_length=9000, blank=True, null=True)
    piedPage = models.TextField(max_length=9999, blank=True, null=True)
    
    horsTaxe = models.FloatField(blank=True, null=True, default=0)
    tva = models.FloatField(null=True, blank=True, default=0)
    toutTaxe = models.FloatField(null=True, blank=True, default=0)


    def save(self, *args, **kwargs):
        self.ref = str("D{}/".format(today)) + str("{}/".format(self.client.nom)) + str("{}".format(year))
        sumHorsTaxe = Prod.objects.filter(devis=self.pk).aggregate(Sum('article_total')).get('article_total__sum')
        self.horsTaxe = sumHorsTaxe
        if self.horsTaxe == None:
            pass
        else:
            self.tva = self.horsTaxe * 20 / 100
            self.toutTaxe = self.horsTaxe + self.tva
                    
        super(Devis, self).save(*args, **kwargs)

