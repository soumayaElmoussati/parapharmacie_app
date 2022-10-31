from django.core.mail import EmailMessage
from datetime import datetime
import os, xlsxwriter
from django.conf import settings
from gest.models import *

settings.configure(
    DATABASE_ENGINE = 'mysql',
    DATABASE_NAME = 'redareda_mirapara',
    DATABASE_USER = 'redareda_mira',
    DATABASE_PASSWORD = 'nJm&.Imj+}=e',
    DATABASE_HOST = 'localhost',
    DATABASE_PORT = '3306',
    TIME_ZONE = 'America/New_York',
)

today = datetime.now().day
month = datetime.now().month
year = datetime.now().year

def backupfile():
    workbook = xlsxwriter.Workbook('BACKUP|{}-{}-{}.xlsx'.format(today, month, year))
    style = workbook.add_format({'bold': 4, 'border': 5, 'align': 'center', 'valign': 'vcenter','fg_color': 'A6BCF1', 'font_size': '20' , 'font':'underline'})
    style.set_underline()
    styleHeader = workbook.add_format({'bold': 2, 'border': 5, 'align': 'center', 'valign': 'center'})
    stylebottom = workbook.add_format({'bold': 1, 'border': 5, 'align': 'center', 'fg_color': 'E09F5A', 'valign': 'center'})
    stylehead = workbook.add_format({'bold': 1, 'align': 'center', 'border': 5, 'valign': 'center' ,'fg_color': 'F1CCA6'})
    styleText = workbook.add_format({'align': 'center', 'valign': 'center'})
    worksheet = workbook.add_worksheet(name="PRODUITS")
    worksheet.set_column(0, 11, 40)

    worksheet.write(1, 0, "REFER", stylehead)
    worksheet.write(1, 1, "NOM", stylehead)
    worksheet.write(1, 2, "CATEGORIE", stylehead)
    worksheet.write(1, 3, "PRIX", stylehead)
    worksheet.write(1, 4, "PRIX ACHAT", stylehead)
    worksheet.write(1, 5, "DATE EXPIRATION", stylehead)
    worksheet.write(1, 6, "TVA", stylehead)
    worksheet.write(1, 7, "REMISE CONSO", stylehead)
    worksheet.write(1, 8, "REMISE GROSSISTE", stylehead)
    worksheet.write(1, 9, "UNITE", stylehead)
    worksheet.write(1, 10, "QTE", stylehead)
    worksheet.write(1, 11, "CODE BARRE", stylehead)
    data_prod = Product.objects.all()
    line = 2
    step = 0
    for i in data_prod:
        if i.refer == None:
            i.refer = "-"
        if i.name == None:
            i.name = "-"
        if i.categorie == None:
            i.categorie = "-"
        if i.prix == None:
            i.prix = "-"
        if i.p_achat == None:
            i.p_achat = "-"
        if i.date_expire == None:
            i.date_expire = "-"
        if i.tva == None:
            i.tva = "-"
        if i.remise_consomateur == None:
            i.remise_consomateur = "-"
        if i.remise_grossite == None:
            i.remise_grossite = "-"
        if i.unite == None:
            i.unite = "-"
        if i.quantity == None:
            i.quantity = "-"
        if i.codeBarre == None:
            i.codeBarre = "-"
        
        worksheet.write(line, 0, "{}".format(i.refer), styleText)
        worksheet.write(line, 1, "{}".format(i.name), styleText)
        worksheet.write(line, 2, "{}".format(i.categorie), styleText)
        worksheet.write(line, 3, "{}".format(i.prix), styleText)
        worksheet.write(line, 4, "{}".format(i.p_achat), styleText)
        worksheet.write(line, 5, "{}".format(i.date_expire), styleText)
        worksheet.write(line, 6, "{}".format(i.tva), styleText)
        worksheet.write(line, 7, "{}".format(i.remise_consomateur), styleText)
        worksheet.write(line, 8, "{}".format(i.remise_grossite), styleText)
        worksheet.write(line, 9, "{}".format(i.unite), styleText)
        worksheet.write(line, 10, "{}".format(i.quantity), styleText)
        worksheet.write(line, 11, "{}".format(i.codeBarre), styleText)
        line = line + 1

    worksheet = workbook.add_worksheet(name="VENTES")
    worksheet.set_column(0, 7, 40)
    

    worksheet.write(1, 0, "DATE", stylehead)
    worksheet.write(1, 1, "CLIENT", stylehead)
    worksheet.write(1, 2, "PRODUITS", stylehead)
    worksheet.write(1, 3, "PAY", stylehead)
    worksheet.write(1, 4, "REMISE", stylehead)
    worksheet.write(1, 5, "PRIX", stylehead)
    worksheet.write(1, 6, "PRIX REMISE", stylehead)
    worksheet.write(1, 7, "QTE", stylehead)
    data_vente = Ventes.objects.all()
    line = 2
    for i in data_vente:
        if i.date == None:
            i.date = "-"
        if i.client == None:
            i.client = "-"
        if i.produit == None:
            i.produit = "-"
        if i.pay == None:
            i.pay = "-"
        if i.remise == None:
            i.remise = "-"
        if i.prix == None:
            i.prix = "-"
        if i.p_remise == None:
            i.p_remise = "-"
        if i.quantite == None:
            i.quantite = "-"

        worksheet.write(line, 0, "{}".format(i.date), styleText)
        worksheet.write(line, 1, "{}".format(i.client), styleText)
        worksheet.write(line, 2, "{}".format(i.produit), styleText)
        worksheet.write(line, 3, "{}".format(i.pay), styleText)
        worksheet.write(line, 4, "{}".format(i.remise), styleText)
        worksheet.write(line, 5, "{}".format(i.prix), styleText)
        worksheet.write(line, 6, "{}".format(i.p_remise), styleText)
        worksheet.write(line, 7, "{}".format(i.quantite), styleText)
        line = line + 1

    worksheet = workbook.add_worksheet(name="ANNULER")
    worksheet.set_column(0, 4, 40)
    
    
    worksheet.write(1, 0, "DATE", stylehead)
    worksheet.write(1, 1, "PRODUITS", stylehead)
    worksheet.write(1, 2, "REMISE", stylehead)
    worksheet.write(1, 3, "PRIX", stylehead)
    worksheet.write(1, 4, "QTE", stylehead)
    data_annuler = Annuler.objects.all()
    line = 2
    for i in data_annuler:
        if i.date == None:
            i.date = "-"
        if i.produit == None:
            i.produit = "-"
        if i.remise == None:
            i.remise = "-"
        if i.prix == None:
            i.prix = "-"
        if i.quantite == None:
            i.quantite = "-"

        worksheet.write(line, 0, "{}".format(i.date), styleText)
        worksheet.write(line, 1, "{}".format(i.produit), styleText)
        worksheet.write(line, 2, "{}".format(i.remise), styleText)
        worksheet.write(line, 3, "{}".format(i.prix), styleText)
        worksheet.write(line, 4, "{}".format(i.quantite), styleText)
        line = line + 1
        
    worksheet = workbook.add_worksheet(name="FOURNISSEUR")
    worksheet.set_column(0, 2, 40)
    
    
    worksheet.write(1, 0, "NOM", stylehead)
    worksheet.write(1, 1, "TELEPHONE", stylehead)
    worksheet.write(1, 2, "EMAIL", stylehead)
    data_frs = Fournisseur.objects.all()
    line = 2
    for i in data_frs:
        if i.nom == None:
            i.nom = "-"
        if i.telephone == None:
            i.telephone = "-"
        if i.email == None:
            i.email = "-"

        worksheet.write(line, 0, "{}".format(i.nom), styleText)
        worksheet.write(line, 1, "{}".format(i.telephone), styleText)
        worksheet.write(line, 2, "{}".format(i.email), styleText)
        line = line + 1

    worksheet = workbook.add_worksheet(name="CLIENTS")
    worksheet.set_column(0, 6, 40)
    
    
    
    worksheet.write(1, 0, "NOM", stylehead)
    worksheet.write(1, 1, "TELEPHONE", stylehead)
    worksheet.write(1, 2, "EMAIL", stylehead)
    worksheet.write(1, 3, "ICE", stylehead)
    worksheet.write(1, 4, "ABREVIATION", stylehead)
    worksheet.write(1, 5, "ADRESSE", stylehead)
    worksheet.write(1, 6, "VILLE", stylehead)
    data_client = Client.objects.all()
    line = 2
    for i in data_client:
        if i.nom == None:
            i.nom = "-"
        if i.telephone == None:
            i.telephone = "-"
        if i.email == None:
            i.email = "-"
        if i.ice == None:
            i.ice = "-"
        if i.abreviation == None:
            i.abreviation = "-"
        if i.adresse == None:
            i.adresse = "-"
        if i.ville == None:
            i.ville = "-"

        worksheet.write(line, 0, "{}".format(i.nom), styleText)
        worksheet.write(line, 1, "{}".format(i.telephone), styleText)
        worksheet.write(line, 2, "{}".format(i.email), styleText)
        worksheet.write(line, 3, "{}".format(i.ice), styleText)
        worksheet.write(line, 4, "{}".format(i.abreviation), styleText)
        worksheet.write(line, 5, "{}".format(i.adresse), styleText)
        worksheet.write(line, 6, "{}".format(i.ville), styleText)
        line = line + 1
        
    worksheet = workbook.add_worksheet(name="DETTES")
    worksheet.set_column(0, 5, 40)
    
    
    
    worksheet.write(1, 0, "FOURNISSEUR", stylehead)
    worksheet.write(1, 1, "DATE CREATION", stylehead)
    worksheet.write(1, 2, "NUMERO FACTURE", stylehead)
    worksheet.write(1, 3, "DATE", stylehead)
    worksheet.write(1, 4, "MONTANT", stylehead)
    worksheet.write(1, 5, "RAISON", stylehead)
    data_dette = Dette.objects.all()
    line = 2
    for i in data_dette:
        if i.fournisseur == None:
            i.fournisseur = "-"
        if i.date_creation == None:
            i.date_creation = "-"
        if i.numero_facture == None:
            i.numero_facture = "-"
        if i.date == None:
            i.date = "-"
        if i.montant == None:
            i.montant = "-"
        if i.raison == None:
            i.raison = "-"

        worksheet.write(line, 0, "{}".format(i.fournisseur), styleText)
        worksheet.write(line, 1, "{}".format(i.date_creation), styleText)
        worksheet.write(line, 2, "{}".format(i.numero_facture), styleText)
        worksheet.write(line, 3, "{}".format(i.date), styleText)
        worksheet.write(line, 4, "{}".format(i.montant), styleText)
        worksheet.write(line, 5, "{}".format(i.raison), styleText)
        line = line + 1
        
        
    worksheet = workbook.add_worksheet(name="FACTURE")
    worksheet.set_column(0, 15, 40)
    
    


    worksheet.write(1, 0, "REF", stylehead)
    worksheet.write(1, 1, "CLIENT", stylehead)
    worksheet.write(1, 2, "TYPE FAC", stylehead)
    worksheet.write(1, 3, "DESCRIPTION", stylehead)
    worksheet.write(1, 4, "DATE", stylehead)
    worksheet.write(1, 5, "MONTANT", stylehead)
    worksheet.write(1, 6, "MODE", stylehead)
    worksheet.write(1, 7, "PIED PAGE", stylehead)
    worksheet.write(1, 8, "STATUT", stylehead)
    worksheet.write(1, 9, "MONTANT HT", stylehead)
    worksheet.write(1, 10, "IS FACT", stylehead)
    worksheet.write(1, 11, "NUM FACTURE", stylehead)
    worksheet.write(1, 12, "IS BL", stylehead)
    worksheet.write(1, 13, "NUM BL", stylehead)
    worksheet.write(1, 14, "TVA", stylehead)
    worksheet.write(1, 15, "MONTANT TTC", stylehead)

    data_fac = Facture.objects.all()
    line = 2
    for i in data_fac:
        if i.ref == None:
            i.ref = "-"
        if i.client == None:
            i.client = "-"
        if i.type_facture == None:
            i.type_facture = "-"
        if i.description == None:
            i.description = "-"
        if i.date == None:
            i.date = "-"
        if i.montant == None:
            i.montant = "-"
        if i.mode_paiment == None:
            i.mode_paiment = "-"
        if i.piedPage == None:
            i.piedPage = "-"
        if i.statut == None:
            i.statut = "-"
        if i.horsTaxe == None:
            i.horsTaxe = "-"
        if i.is_Facture == None:
            i.is_Facture = "-"
        if i.num_facture == None:
            i.num_facture = "-"
        if i.is_Bl == None:
            i.is_Bl = "-"
        if i.num_bl == None:
            i.num_bl = "-"
        if i.tva == None:
            i.tva = "-"
        if i.toutTaxe == None:
            i.toutTaxe = "-"

        worksheet.write(line, 0, "{}".format(i.ref), styleText)
        worksheet.write(line, 1, "{}".format(i.client), styleText)
        worksheet.write(line, 2, "{}".format(i.type_facture), styleText)
        worksheet.write(line, 3, "{}".format(i.description), styleText)
        worksheet.write(line, 4, "{}".format(i.date), styleText)
        worksheet.write(line, 5, "{}".format(i.montant), styleText)
        worksheet.write(line, 6, "{}".format(i.mode_paiment), styleText)
        worksheet.write(line, 7, "{}".format(i.piedPage), styleText)
        worksheet.write(line, 8, "{}".format(i.statut), styleText)
        worksheet.write(line, 9, "{}".format(i.horsTaxe), styleText)
        worksheet.write(line, 10, "{}".format(i.is_Facture), styleText)
        worksheet.write(line, 11, "{}".format(i.num_facture), styleText)
        worksheet.write(line, 12, "{}".format(i.is_Bl), styleText)
        worksheet.write(line, 13, "{}".format(i.num_bl), styleText)
        worksheet.write(line, 14, "{}".format(i.tva), styleText)
        worksheet.write(line, 15, "{}".format(i.toutTaxe), styleText)
        line = line + 1

    worksheet = workbook.add_worksheet(name="ORDERS")
    worksheet.set_column(0, 8, 40)
    
    
    
    worksheet.write(1, 0, "FACTURE", stylehead)
    worksheet.write(1, 1, "DATE", stylehead)
    worksheet.write(1, 2, "NOM", stylehead)
    worksheet.write(1, 3, "REMISE", stylehead)
    worksheet.write(1, 4, "MONTANT", stylehead)
    worksheet.write(1, 5, "TVA", stylehead)
    worksheet.write(1, 6, "PRIX REMISE", stylehead)
    worksheet.write(1, 7, "QTE", stylehead)
    worksheet.write(1, 8, "TOTAL", stylehead)

    data_order = Order.objects.all()
    line = 2
    for i in data_order:
        if i.facture == None:
            i.facture = "-"
        if i.date == None:
            i.date = "-"
        if i.nom == None:
            i.nom = "-"
        if i.remise == None:
            i.remise = "-"
        if i.prix == None:
            i.prix = "-"
        if i.tva_order == None:
            i.tva_order = "-"
        if i.p_remise == None:
            i.p_remise = "-"
        if i.quantite == None:
            i.quantite = "-"
        if i.p_total == None:
            i.p_total = "-"

        worksheet.write(line, 0, "{}".format(i.facture), styleText)
        worksheet.write(line, 1, "{}".format(i.date), styleText)
        worksheet.write(line, 2, "{}".format(i.nom), styleText)
        worksheet.write(line, 3, "{}".format(i.remise), styleText)
        worksheet.write(line, 4, "{}".format(i.prix), styleText)
        worksheet.write(line, 5, "{}".format(i.tva_order), styleText)
        worksheet.write(line, 6, "{}".format(i.p_remise), styleText)
        worksheet.write(line, 7, "{}".format(i.quantite), styleText)
        worksheet.write(line, 8, "{}".format(i.p_total), styleText)
        line = line + 1
        
        #'kantouch.mohammed@gmail.com',
        
    workbook.close()
    mail = EmailMessage('BACKUP DU {}-{}-{}'.format(today, month, year), 'VOICI LE BACK DU LA BASE DE DONNEE AU {}-{}-{}'.format(today, month, year), settings.EMAIL_HOST_USER, ['redabenhamid@yahoo.com', ])
    cwd = os.getcwd()
    app = os.path.join(cwd, 'BACKUP|{}-{}-{}.xlsx'.format(today, month, year))
    mail.attach_file(app)
    mail.send()
    print("send it")
    
backupfile()
