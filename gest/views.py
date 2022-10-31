import json
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as dj_login, authenticate, logout
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q, F
from django.forms import inlineformset_factory
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.core import serializers
import csv, xlsxwriter
#from .printer import printw
from .forms import *
from .models import *
from io import BytesIO
from django.conf import settings
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.utils import ImageReader
from django.core.mail import EmailMessage
import textwrap, os

today = timezone.now().day
month = timezone.now().month
year = timezone.now().year



def backupfile(request):
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
        
    worksheet = workbook.add_worksheet(name="PAIMENTS")
    worksheet.set_column(0, 2, 40)
    
    
    
    worksheet.write(1, 0, "DATE", stylehead)
    worksheet.write(1, 1, "COMMANDE ID", stylehead)
    worksheet.write(1, 2, "MONTANT", stylehead)

    data_paiment = Paiment.objects.all()
    line = 2
    for i in data_paiment:
        if i.date == None:
            i.date = "-"
        if i.commande_id == None:
            i.commande_id = "-"
        if i.montant == None:
            i.montant = "-"


        worksheet.write(line, 0, "{}".format(i.date), styleText)
        worksheet.write(line, 1, "{}".format(i.commande_id), styleText)
        worksheet.write(line, 2, "{}".format(i.montant), styleText)

        line = line + 1
        
        #'kantouch.mohammed@gmail.com',
        
    workbook.close()
    mail = EmailMessage('BACKUP DU {}-{}-{}'.format(today, month, year), 'VOICI LE BACKUP DE LA BASE DE DONNEE AU {}-{}-{}'.format(today, month, year), settings.EMAIL_HOST_USER, ['redabenhamid@yahoo.com', 'kantouch.mohammed@gmail.com',])
    cwd = os.getcwd()
    app = os.path.join(cwd, 'BACKUP|{}-{}-{}.xlsx'.format(today, month, year))
    mail.attach_file(app)
    mail.send()

def draw_wrapped_line(canvas, text, length, x_pos, y_pos, y_offset):
    """
    :param canvas: reportlab canvas
    :param text: the raw text to wrap
    :param length: the max number of characters per line
    :param x_pos: starting x position
    :param y_pos: starting y position
    :param y_offset: the amount of space to leave between wrapped lines
    """
    if len(text) > length:
        wraps = textwrap.wrap(text, length)
        for x in range(len(wraps)):
            canvas.drawString(x_pos, y_pos, wraps[x])
            y_pos -= y_offset
        y_pos += y_offset  # add back offset after last wrapped line
    else:
        canvas.drawString(x_pos, y_pos, text)
    return y_pos


def counter_p():
    counter_panier = Panier.objects.count()
    if counter_panier == None:
        counter_panier = 0
    else:
        pass

    return counter_panier


def login(request):

    #pyautogui.press('F11')
    #backupfile()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
                dj_login(request, user)
                return redirect('/dashboard')
        else:
            messages.warning(request, 'IDENTIFIANT INCORRECT !')
            return redirect('/')


    return render(request, 'login.html', {})


def prodliste(request):

    panier = Product.objects.all()
    serialized_qs = serializers.serialize('json', panier)

    return JsonResponse(serialized_qs, safe=False)

@login_required
def dashboard(request):

    # #pyautogui.press('F11')
    # # Give the location of the file
    # loc = ("C:\\Users\\yoga\\Desktop\\para\\gest\\data.xlsx")
    
    # wb = xlrd.open_workbook(loc)
    # sheet = wb.sheet_by_index(0)
 
    # for i in range(sheet.nrows):
    #     if i == 0:
    #         continue
    #     article = sheet.cell_value(i, 1)
    #     prix_achat = sheet.cell_value(i, 3)
    #     prix_vente = sheet.cell_value(i, 4)
    #     print("ygkj iuyg {} {} {}".format(article, prix_achat, prix_vente))
    #     if article == None:
    #         article = "-"
    #     if prix_achat == None or prix_achat == ' ' or prix_achat == '':
    #         prix_achat = 0
    #     if prix_vente == None or prix_vente == ' ' or prix_vente == '':
    #         prix_vente = 0
    #     Product.objects.create(name=article, p_achat=float(prix_achat), prix=float(prix_vente))

    panier = counter_p()

    if request.method == 'POST':
        forms = dette_form(request.POST or None)
        if forms.is_valid():
            forms.save()
            forms = dette_form()
            redirect('/dashboard')
    else:
        forms = dette_form()
    forms = dette_form()

    data_vente = Ventes.objects.filter(date__month=month, date__year=year).aggregate(Sum('p_remise'))
    data_vente_year = Ventes.objects.filter(date__year=year).aggregate(Sum('p_remise')).get('p_remise__sum')
    data_dettes = Dette.objects.all().aggregate(Sum('montant')).get('montant__sum')
    data_fac = Facture.objects.filter(date__month=month, date__year=year, statut="Impayee").aggregate(Sum('toutTaxe')).get('toutTaxe__sum')
    data_vente_month = Ventes.objects.filter(date__month=month, date__year=year).aggregate(Sum('quantite')).get('quantite__sum')
    data_produit = Product.objects.all().count()
    data_prod_ven = Ventes.objects.all().aggregate(Sum('quantite'))
    exp_month = Product.objects.filter(date_expire__month=month, date_expire__year=year)
    exp_month_dettes = Dette.objects.filter(date__month=month, date__year=year).filter(raison='Impayer')
    rupture = Product.objects.filter(quantity__lte=2)

    data = []

    mois = []

    for k in range(1, 32):

        kl = Ventes.objects.filter(date__day=k, date__month=month, date__year=year).aggregate(Sum('p_remise'))
        kl = kl.get('p_remise__sum')

        if kl == None:
            kl = 0

        mois.append(kl)
        pass
        

    for p in range(1, 13):
        l = Ventes.objects.filter(date__month=p, date__year=year).aggregate(Sum('p_remise'))
        l = l.get('p_remise__sum')
        if l == None:
            l = 0
        data.append(l)
        pass

    context = {
        'nbar': 'ACCEUIL',
        'dd': today,
        'mm': month,
        'yy': year,
        'panier': panier,
        'montant': data_vente.get('p_remise__sum'),
        'total_prod': data_produit,
        'total_prod_ven': data_prod_ven.get('quantite__sum'),
        'year': data,
        'rupture': rupture,
        'data_fac': data_fac,
        'mois': mois,
        'expire': exp_month,
        'data_dettes': data_dettes,
        'dettes': exp_month_dettes,
        'total_year': data_vente_year,
        'forms': forms,
        'total_vente_mois': data_vente_month

    }

    return render(request, 'main.html', context)




@login_required
def produits(request):
    if request.method == 'POST':
        formProd = stockFrom(request.POST or None)
        if formProd.is_valid():
            formProd.save()
    else:
        formProd = stockFrom()
    prod = Product.objects.all()
    search_post = request.GET.get('search')
    paginator = Paginator(prod, 200)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if search_post:
        page_obj = Product.objects.filter(Q(name__icontains=search_post) | Q(codeBarre__icontains=search_post))


    panier = counter_p()
    data = []
    for k in prod:
        data.append(k.name)
        
    dic = 9

    context = {
        'nbar': 'PRODUITS',
        'prodListe': page_obj,

        'data':data,
        'panier': panier,
        'form': formProd
    }

    return render(request, 'product.html', context)

@login_required
def add_produits(request):
    panier = counter_p()

    if request.method == 'POST':
        formProd = prodForm(request.POST or None)
        if formProd.is_valid():
            formProd.save()
    else:
        formProd = prodForm()


    context = {
        'nbar': 'PRODUITS',
        'form': formProd,
        'panier': panier
    }
    return render(request, 'addprod.html', context)


@login_required
def category(request):

    cater = Categories.objects.all()
    panier = counter_p()

    if request.method == 'POST':
        form = cat_form(request.POST)
        if form.is_valid():
            form.save() 
    else:
        form = cat_form()

    context = {
        'nbar': 'CATEGORY',
        'form': form,
        'data': cater,
        'panier': panier
    }

    return render(request, 'category.html', context)

@login_required
def ventes(request):

    data = Ventes.objects.all().order_by('-id')
    panier = counter_p()

    context = {
        'nbar': 'VENTES',
        'data': data,
        'panier': panier      
    }

    return render(request, 'ventes.html', context)

@login_required
def add_ventes(request):
    panier = counter_p()

    if request.method == 'POST':
        form = ven_form_model(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ven_form_model()

    context = {
        'nbar': 'VENTES',
        'form': ven_form_model,
        'panier': panier
    }

    return render(request, 'ven_form.html', context)

@login_required
def delete_category(request, pk):
    rec = get_object_or_404(Categories, pk=pk)      
    rec.delete()        

    return redirect('/category')

@login_required
def delete_vente(request, pk):

    delp = get_object_or_404(Ventes, pk=pk)
    t = Product.objects.filter(name=delp.produit)[0]
    Product.objects.filter(name=t.name).update(quantity=F('quantity') + delp.quantite)
    saver = Annuler(date=delp.date, produit=delp.produit, remise=delp.remise, prix=delp.prix, quantite=delp.quantite)
    saver.save()
    delp.delete()

    return redirect('/ventes')

@login_required
def ajouter_panier(request, pk, remise, qte, pph):

    pan = get_object_or_404(Product, pk=pk)
    pl =  float(pph) * float(remise) / 100
    pl = float(pph) - pl
    qt = int(qte)
    plt = pl * qt
    saver = Panier(nom=pan.name, remise=float(remise), prix=float(pph), quantite=qt, p_remise=pl, p_total=plt)
    saver.save()

    return redirect('/produits')

@login_required
def deleteProduct(request, pk):
    Product.objects.get(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def clients(request):

    client = Client.objects.all()
    if request.method == 'POST':
        form = client_form(request.POST or None)
        if form.is_valid():
            form.save()
            form = client_form()
            redirect('/clients')
    else:
        form = client_form()

    context = {
        'nbar': 'Clients',
        'client': client,
        'form': form
    }

    return render(request, 'clients.html', context)

@login_required
def clt_profil(request, pk):

    nom = Client.objects.get(pk=pk)
    vente = Facture.objects.filter(client=nom)
    paiment = Paiment.objects.filter(commande_id__client=nom.pk)
    paiment_total = Paiment.objects.filter(commande_id__client=nom.pk).aggregate(Sum('montant')).get('montant__sum')
    paiment_imp_total = Paiment.objects.filter(commande_id__client=nom.pk, commande_id__statut="Impayee").aggregate(Sum('montant')).get('montant__sum')
    total_impayer_facture = Facture.objects.filter(client=nom.pk, statut="Impayee").aggregate(Sum('toutTaxe')).get('toutTaxe__sum')
    total_dette_vente = Ventes.objects.filter(client=nom.pk, pay="DETTE").aggregate(Sum('p_remise')).get('p_remise__sum')
    dette = Ventes.objects.filter(client=nom.pk)
    
    if total_impayer_facture == None:
        total_impayer_facture = 0
        
    if paiment_imp_total == None:
        paiment_imp_total = 0
        
    if paiment_total == None:
        paiment_total = 0
        
    if total_dette_vente == None:
        total_dette_vente = 0
        
    totaldyaltotal = (total_dette_vente + total_impayer_facture) - paiment_total
        
    total_impayer_facture = total_impayer_facture - paiment_imp_total
        
    

    context = {
        'nbar': nom.nom,
        'dette':dette,
        'nom': nom,
        'vente': vente,
        'imp_fac': total_impayer_facture,
        'imp_vente': total_dette_vente,
        'paiment_total': paiment_total,
        'data': paiment,
        'totaldyaltotal': totaldyaltotal
    }

    return render(request, 'profil.html', context)

@login_required
def clt_profilfiltred(request, pk):

    nom = Client.objects.get(pk=pk)
    vente = Facture.objects.filter(client=nom, statut='Impayee')
    dette = Ventes.objects.filter(pay="DETTE")

    context = {
        'nbar': nom.nom,
        'dette':dette,
        'nom': nom,
        'vente': vente
    }

    return render(request, 'profil.html', context)

@login_required
def frs(request):

    client = Fournisseur.objects.all()
    if request.method == 'POST':
        form = frs_form(request.POST or None)
        if form.is_valid():
            form.save()
            form = frs_form()
            redirect('/frs')
    else:
        form = frs_form()
    


    context = {
        'nbar': 'Fournisseur',
        'client': client,
        'form': form,
        'former': forms
    }

    return render(request, 'frs.html', context)

@login_required
def frs_profil(request, pk):

    nom = Fournisseur.objects.get(pk=pk)
    vente = Dette.objects.filter(fournisseur=nom)
    dettes = Dette.objects.filter(fournisseur=nom).filter(raison='Impayer').aggregate(Sum('montant')).get('montant__sum')

    context = {
        'nbar': nom.nom,
        'nom': nom,
        'vente': vente,
        'dette': dettes
    }

    return render(request, 'frsprofil.html', context)

@login_required
def payer(request, pk):
    Dette.objects.filter(pk=pk).update(raison='Payer')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def impayer(request, pk):
    Dette.objects.filter(pk=pk).update(raison='Impayer')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def frs_supp(request, pk):
    Fournisseur.objects.filter(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER')) 

@login_required
def facsupp(request, pk):
    Facture.objects.filter(pk=pk).delete()
    return redirect('/facture')
    
@login_required
def devsupp(request, pk):
    Devis.objects.filter(pk=pk).delete()
    return redirect('/devis')

@login_required
def panier(request):
    data = Panier.objects.all()
    panier = counter_p()
    client = Client.objects.all()
    tot = Panier.objects.all().aggregate(Sum('p_total'))


    context = {
        'panier': panier,
        'data': data,
        'nbar': 'PANIER',
        'client':client,
        'total_paye': tot.get('p_total__sum')
    }

    return render(request, 'panier.html', context)

@login_required
def annul(request):
    data = Annuler.objects.all().order_by('-id')
    paginator = Paginator(data, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'annul.html', {'data': page_obj, 'nbar': 'ANNULATION'})

@login_required
def validation(request, client, mode):
    clientp = client.replace("%20", " ")
    clt = Client.objects.filter(nom=clientp)[0]
    tot = Panier.objects.all()
    for t in tot:
        prodID = Product.objects.get(name=t.nom)
        # stockInfo = Stock.objects.filter(nom=prodID.pk)[0]
        # if stockInfo.quantite <= 0:
        #     Stock.objects.filter(pk=stockInfo.pk).update(quantite=stockInfo.quantite - int(t.quantite))
        Product.objects.filter(pk=prodID.pk).update(quantity=F('quantity') - int(t.quantite))
        Ventes.objects.create(date=timezone.now(), client=clt, produit=t.nom, quantite=t.quantite, remise=t.remise, p_remise=t.p_total, prix=t.prix, pay=mode)
        # else:
        #     Stock.objects.filter(pk=stockInfo.pk).update(quantite=stockInfo.quantite - int(t.quantite))
        #     Ventes.objects.create(date=timezone.now(), client=clt, produit=t.nom, quantite=t.quantite, remise=t.remise, p_remise=t.p_total, prix=t.prix, pay=mode)
            
        #Product.objects.filter(name=t.nom).update(quantity=F('quantity') - int(t.quantite))
    fide = Ventes.objects.filter(client=clt.pk).aggregate(Sum('prix')).get('p_total__sum')
    if fide == None:
        fide = 0
    if fide > 200:
        tps = fide // 200
        tps = int(tps)
        Client.objects.filter(pk=clt.pk).update(point=tps)
    Panier.objects.all().delete()

    #printw(tot)
    return redirect('/panier')


@login_required
def rester(request, pk):
    vp = Client.objects.filter(pk=pk)[0]
    Client.objects.filter(pk=pk).update(point=0)
    Ventes.objects.filter(client=vp).delete()

    return redirect(request.META.get('HTTP_REFERER'))
@login_required
def supp_clt(request, pk):
    Client.objects.filter(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def panier_an(request, pk):
    delt = get_object_or_404(Panier, pk=pk)
    delt.delete()
    return redirect('/panier')

@login_required
def productEditor(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    stock = Stock.objects.filter(nom=pk)
    editProd = productEdit(request.POST or None, instance=prod)
    if editProd.is_valid():
        editProd.save()
        redirect('/produits')

    context = {
        'form':editProd,
        'stock': stock,
        'nbar': 'MODIFICATION',
        'stock':stock
    }


    return render(request, 'editor.html', context)

@login_required
def clientEditor(request, pk):
    prod = get_object_or_404(Client, pk=pk)
    editProd = clientEdit(request.POST or None, instance=prod)
    if editProd.is_valid():
        editProd.save()
        redirect('/clients')

    context = {
        'form':editProd,
        'nbar': 'MODIFICATION'
    }


    return render(request, 'editorClients.html', context)

@login_required
def panier_vider(self):
    Panier.objects.all().delete()
    return redirect('/panier')
    

@login_required
def delete_paiments(request, pk):
    rec = get_object_or_404(Paiment, pk=pk)      
    rec.delete()        

    return redirect('/paiments')
    
@login_required
def paiments(request):

    data = Paiment.objects.all().order_by('-id')
    if request.method == 'POST':
        form_paiment = paimentForm(request.POST)
        if form_paiment.is_valid():
            form_paiment.save()
            return redirect('/paiments')
            
    else:
        form_paiment = paimentForm()

    context = {
        'nbar': 'PAIMENTS',
        'form': form_paiment,
        'data': data
    }

    return render(request, 'paiments.html', context)



@login_required
def facture(request):
    data = Facture.objects.all().order_by('-id')
    if request.method == 'POST':
        form_fact = factureForm(request.POST)
        if form_fact.is_valid():
            form_fact.save()
            return redirect('/facture')
            
    else:
        form_fact = factureForm()

    context = {
        'nbar': 'FACTURE',
        'data': data,
        'form': form_fact
    }

    return render(request, 'fac.html', context)

@login_required
def factureAdmin(request):

    data = Facture.objects.all().order_by('-id')
    if request.method == 'POST':
        form_fact = factureForm(request.POST)
        if form_fact.is_valid():
            fs= form_fact.save(commit=False)
            fs.commercant= request.user.username
            fs.save()
            
    else:
        form_fact = factureForm()

    context = {
        'nbar': 'FACTURE',
        'data': data,
        'form': form_fact
    }

    return render(request, 'facAdmin.html', context)

@login_required
def factureOrderAdd(request, pk):
    dats = Product.objects.all()
    data = {}
    for t in dats:
        remise = t.tva
        if t.tva == None:
            remise = 0
        data['{}'.format(t)] = remise

    fact = get_object_or_404(Facture, pk=pk)
    order = inlineformset_factory(Facture, Order,fields=('nom', 'quantite', 'remise', 'prix'), extra=1)
    if request.method == 'POST':
        form = order(request.POST or None, instance=fact)
        if form.is_valid():
            form.save()
        if Order.objects.filter(facture=fact.pk).aggregate(Sum('p_total')).get('p_total__sum') == None:
            sumHorsTaxe = 0
        else:
            sumHorsTaxe = Order.objects.filter(facture=fact.pk).aggregate(Sum('p_total')).get('p_total__sum')
        editorfact = Facture.objects.get(pk=pk)
        if Order.objects.filter(facture=editorfact.pk).aggregate(Sum('tva_order')).get('tva_order__sum') == None:
            tvatotal = 0
        else:
            tvatotal = Order.objects.filter(facture=editorfact.pk).aggregate(Sum('tva_order')).get('tva_order__sum')
        editorfact = Facture.objects.filter(pk=pk)
        editorfact.update(horsTaxe=float(sumHorsTaxe-tvatotal))
        editorfact.update(tva=tvatotal)
        editorfact.update(toutTaxe=float(sumHorsTaxe))
        return redirect('/facture')
        
    else:
        form = order(instance=fact)

    context = {
        'nbar': 'FACTURE',
        'form': form,
        'data': data
    }
    return render(request, 'facture.html', context)
    
@login_required
def devis(request):
    data = Devis.objects.all().order_by('-id')
    if request.method == 'POST':
        form_fact = devisForm(request.POST)
        if form_fact.is_valid():
            form_fact.save()
            
    else:
        form_fact = devisForm()

    context = {
        'nbar': 'Devis',
        'data': data,
        'form': form_fact
    }

    return render(request, 'devis.html', context)
    
@login_required
def devisProdAdd(request, pk):
    dats = Product.objects.all()
    data = {}
    for t in dats:
        remise = t.tva
        if t.tva == None:
            remise = 0
        data['{}'.format(t)] = remise

    fact = get_object_or_404(Devis, pk=pk)
    order = inlineformset_factory(Devis, Prod,fields=('nom', 'quantite', 'remise', 'prix'), extra=1)
    if request.method == 'POST':
        form = order(request.POST or None, instance=fact)
        if form.is_valid():
            form.save()
        if Prod.objects.filter(facture=fact.pk).aggregate(Sum('p_total')).get('p_total__sum') == None:
            sumHorsTaxe = 0
        else:
            sumHorsTaxe = Prod.objects.filter(facture=fact.pk).aggregate(Sum('p_total')).get('p_total__sum')
        editorfact = Devis.objects.get(pk=pk)
        if Prod.objects.filter(facture=editorfact.pk).aggregate(Sum('tva_order')).get('tva_order__sum') == None:
            tvatotal = 0
        else:
            tvatotal = Prod.objects.filter(facture=editorfact.pk).aggregate(Sum('tva_order')).get('tva_order__sum')
        editorfact = Devis.objects.filter(pk=pk)
        editorfact.update(horsTaxe=float(sumHorsTaxe-tvatotal))
        editorfact.update(tva=tvatotal)
        editorfact.update(toutTaxe=float(sumHorsTaxe))
        return redirect('/devis')
        
    else:
        form = order(instance=fact)

    context = {
        'nbar': 'DEVIS',
        'form': form,
        'data': data
    }
    return render(request, 'dev.html', context)

@login_required
def journal(request, dateone, datetwo):


    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['date', 'produits', 'remise', 'prix', 'quantite'])

    for v in Ventes.objects.filter(date__range=[dateone, datetwo]).values_list('date', 'produit', 'remise', 'prix', 'quantite'):
        writer.writerow(v)
    
    response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.csv"'.format(today, month, year)

    return response

@login_required
def pdfFacture(request, idFacture):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="FACTURE-{}-{}-{}|{}.pdf"'.format(today, month, year, idFacture)
    factureInfo = Facture.objects.get(pk=idFacture)
    if factureInfo.is_Facture != True:
        Facture.objects.filter(pk=idFacture).update(is_Facture=True)
        counterFacture = Numerateur.objects.get(pk=1).total_facture
        if counterFacture == None:
            counterFacture = 0
        Facture.objects.filter(pk=idFacture).update(num_facture=int(counterFacture+1))
        Numerateur.objects.filter(pk=1).update(total_facture=int(counterFacture+1))
    factureInfo = Facture.objects.get(pk=idFacture)
    client = factureInfo.client
    order = Order.objects.filter(facture=idFacture)
    total = Order.objects.filter(facture=idFacture).aggregate(Sum('p_total'))
    total_art = total.get('p_total__sum')
    if Order.objects.filter(facture=idFacture).aggregate(Sum('tva_order')).get('tva_order__sum') == None:
        tvatotal = 0
    else:
        tvatotal = Order.objects.filter(facture=idFacture).aggregate(Sum('tva_order')).get('tva_order__sum')
    if total_art == None:
        total_art = 0
    tva_total = tvatotal
    ttc = total_art
    desc = factureInfo.description
    piedPage = factureInfo.piedPage
    client = client
    a = 2490
    b = a - 30
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 35)
    p.setFillColor('#3f4041')
    logo = ImageReader('http://para.sid.co.ma/static/facturebiomedic.png')
    pg = Paginator(order, 14)
    l = pg.num_pages + 1
    for i in range(1, l):
        p.setFont('Helvetica', 35)
        p.setFillColor('#3f4041')
        p.setPageSize((2480, 3508))
        p.drawImage(logo, 0, 0, 2480, 3508, mask='auto')
        p.setFont('Helvetica-Bold', 39)
        p.setFillColor("#CBCBCB")
        p.drawRightString(210, 3000, "#{}".format(str(factureInfo.pk).zfill(8)))
        p.drawCentredString(140, 2950, "c-{}".format(factureInfo.type_facture))
        p.setFont('Helvetica', 35)
        p.setFillColor('#3f4041')
        p.drawRightString(2300, 2899, '{}'.format(str(factureInfo.num_facture).zfill(8)))
        p.drawRightString(2300, 2836, '{} / {} / {}'.format(today, month, year))
        if desc == None:
            pass
        else:
            p.setFillColor('#0870a5')
            p.setFont('Helvetica-Bold', 44)
            p.drawCentredString(1240, 2800, '{}'.format(factureInfo.description))
            p.setFillColor('#3f4041')   
        p.setFont('Helvetica-Bold', 72)
        p.drawString(210, 2896, '{}'.format(client))
        p.setFont('Helvetica', 44)
        p.drawString(295, 2818, '{}'.format(client.ice))
        for r in pg.page(i).object_list:
            if r.nom == None:
                continue
            info = get_object_or_404(Product, name=r.nom.name)
            if info.refer == None:
                p.drawCentredString(280, a, '-')
            else:    
                p.drawCentredString(280, a, '{}'.format(info.refer))
            #draw_wrapped_line(p, '{}'.format(info.name), 100, 760, a, 80)
            p.drawCentredString(990, a, '{}'.format(info.name))

            p.drawCentredString(1600, a, '{}'.format(r.quantite))
            if r.remise == 0 or r.remise == None:
                p.drawCentredString(1745, a, '-')
            else:
                p.drawCentredString(1745, a, '{}%'.format(r.remise))
            p.drawAlignedString(1960, a, '{}'.format(round(r.prix, 2)))
            p.drawAlignedString(2270, a, '{}'.format(round(r.p_total, 2)))
            p.line(150, b, 2390, b)
            a = a - 70
            b = b - 70
        if factureInfo.montant == None:
            pass
        else:
            draw_wrapped_line(p, factureInfo.montant, 60, 180, 1380, 80)
        if piedPage == None:
            pass
        else:
            draw_wrapped_line(p, piedPage, 60, 180, 980, 80)
        p.setFont('Helvetica', 44)
        p.drawString(2040, 1428, '{} DH'.format(round(total_art - tva_total, 2)))
        p.drawString(2040, 1300, '{} DH'.format(round(tva_total, 2)))
        p.setFont('Helvetica-Bold', 44)
        p.setFillColor('#ffffff')
        p.drawString(2040, 1168, '{} DH'.format(round(total_art, 2)))
        a = 2500
        b = a - 30
        p.setFont('Helvetica-Bold', 49)

        if i == pg.num_pages:
            break
        p.showPage()

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


@login_required
def pdfBon(request, idFacture):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="BON-{}-{}-{}|{}.pdf"'.format(today, month, year, idFacture)
    factureInfo = Facture.objects.get(pk=idFacture)
    if factureInfo.is_Bl != True:
        Facture.objects.filter(pk=idFacture).update(is_Bl=True)
        counterFacture = Numerateur.objects.get(pk=1).total_bl
        Facture.objects.filter(pk=idFacture).update(num_bl=int(counterFacture+1))
        if counterFacture == None:
            counterFacture = 0
        Numerateur.objects.filter(pk=1).update(total_bl=int(counterFacture+1))
    factureInfo = Facture.objects.get(pk=idFacture)
    client = factureInfo.client
    order = Order.objects.filter(facture=idFacture)
    total = Order.objects.filter(facture=idFacture).aggregate(Sum('p_total'))
    total_art = total.get('p_total__sum')
    if total_art == None:
        total_art = 0
    tva_total = total_art * 20 / 100
    ttc = total_art + tva_total
    desc = None
    client = client
    a = 2375
    b = a - 30
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 35)
    p.setFillColor('#3f4041')
    logo = ImageReader('http://para.sid.co.ma/static/bldnd.png')
    pg = Paginator(order, 21)
    l = pg.num_pages + 1
    for i in range(1, l):
        p.setPageSize((2480, 3508))
        p.drawImage(logo, 0, 0, 2480, 3508, mask='auto')
        p.setFont('Helvetica-Bold', 39)
        p.setFillColor("#CBCBCB")
        p.drawRightString(210, 3000, "#{}".format(str(factureInfo.pk).zfill(8)))
        p.drawCentredString(140, 2950, "c-{}".format(factureInfo.type_facture))
        p.setFont('Helvetica', 35)
        p.setFillColor('#3f4041')
        p.drawRightString(2300, 2840, '{}'.format(str(factureInfo.num_bl).zfill(8)))
        p.drawRightString(2300, 2770, '{} / {} / {}'.format(today, month, year))
        if desc == None:
            pass
        else:
            p.setFillColor('#0870a5')
            p.setFont('Helvetica-Bold', 44)
            p.drawCentredString(1240, 2800, '{}'.format(factureInfo.description))
            p.setFillColor('#3f4041')   
        p.setFont('Helvetica-Bold', 72)
        p.drawString(210, 2896, '{}'.format(client))
        p.setFont('Helvetica', 44)
        for r in pg.page(i).object_list:
            if r.nom == None:
                continue
            info = get_object_or_404(Product, name=r.nom.name)
            if info.refer == None:
                p.drawCentredString(280, a, '-')
            else:    
                p.drawCentredString(280, a, '{}'.format(info.refer))
            #draw_wrapped_line(p, '{}'.format(info.name), 10, 500, a, 120)
            p.drawCentredString(990, a, '{}'.format(info.name))
      
            p.drawCentredString(1550, a, '{}'.format(r.quantite))
            if r.remise == 0 or r.remise == None:
                p.drawCentredString(1720, a, '-')
            
            else:
                
                p.drawCentredString(1710, a, '{}%'.format(r.remise))
            p.drawRightString(2060, a, '{}'.format(round(float(r.prix), 2)))
            p.drawRightString(2360, a, '{}'.format(round(r.p_total, 2)))
            p.line(164, b, 2375, b)
            a = a - 70
            b = b - 70
        p.setFont('Helvetica-Bold', 64)
        p.setFillColor('#000000')
        p.drawString(180, 568, 'Total TTC : {} DH'.format(round(total_art, 2)))
        a = 2500
        b = a - 30
        p.setFont('Helvetica-Bold', 49)

        if i == pg.num_pages:
            break
        p.showPage()

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

@login_required
def pdfDevis(request, idFacture):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="DEVIS-{}-{}-{}|{}.pdf"'.format(today, month, year, idFacture)
    factureInfo = Devis.objects.get(pk=idFacture)
    client = factureInfo.client
    order = Prod.objects.filter(facture=idFacture)
    total = Prod.objects.filter(facture=idFacture).aggregate(Sum('p_total'))
    total_art = total.get('p_total__sum')
    if Prod.objects.filter(facture=idFacture).aggregate(Sum('tva_order')).get('tva_order__sum') == None:
        tvatotal = 0
    else:
        tvatotal = Prod.objects.filter(facture=idFacture).aggregate(Sum('tva_order')).get('tva_order__sum')
    if total_art == None:
        total_art = 0
    tva_total = tvatotal
    ttc = total_art
    desc = factureInfo.description
    piedPage = factureInfo.piedPage
    client = client
    a = 2490
    b = a - 30
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Helvetica', 35)
    p.setFillColor('#3f4041')
    logo = ImageReader('http://para.sid.co.ma/static/devis.png')
    pg = Paginator(order, 14)
    l = pg.num_pages + 1
    for i in range(1, l):
        p.setFont('Helvetica', 35)
        p.setFillColor('#3f4041')
        p.setPageSize((2480, 3508))
        p.drawImage(logo, 0, 0, 2480, 3508, mask='auto')
        p.setFont('Helvetica-Bold', 39)
        p.setFillColor("#CBCBCB")
        p.drawRightString(210, 3000, "#{}".format(str(factureInfo.pk).zfill(8)))
        
        p.setFont('Helvetica', 35)
        p.setFillColor('#3f4041')
        p.drawRightString(2300, 2899, '{}'.format(str(factureInfo.pk).zfill(8)))
        p.drawRightString(2300, 2836, '{} / {} / {}'.format(today, month, year))
        if desc == None:
            pass
        else:
            p.setFillColor('#0870a5')
            p.setFont('Helvetica-Bold', 44)
            p.drawCentredString(1240, 2800, '{}'.format(factureInfo.description))
            p.setFillColor('#3f4041')   
        p.setFont('Helvetica-Bold', 72)
        p.drawString(210, 2896, '{}'.format(client))
        p.setFont('Helvetica', 44)
        p.drawString(295, 2818, '{}'.format(client.ice))
        for r in pg.page(i).object_list:
            if r.nom == None:
                continue
            info = get_object_or_404(Product, name=r.nom.name)
            if info.refer == None:
                p.drawCentredString(280, a, '-')
            else:    
                p.drawCentredString(280, a, '{}'.format(info.refer))
            #draw_wrapped_line(p, '{}'.format(info.name), 100, 760, a, 80)
            p.drawCentredString(990, a, '{}'.format(info.name))

            p.drawCentredString(1600, a, '{}'.format(r.quantite))
            if r.remise == 0 or r.remise == None:
                p.drawCentredString(1745, a, '-')
            else:
                p.drawCentredString(1745, a, '{}%'.format(r.remise))
            p.drawAlignedString(1960, a, '{}'.format(round(r.prix, 2)))
            p.drawAlignedString(2270, a, '{}'.format(round(r.p_total, 2)))
            p.line(150, b, 2390, b)
            a = a - 70
            b = b - 70
        if factureInfo.montant == None:
            pass
        else:
            draw_wrapped_line(p, factureInfo.montant, 60, 180, 1380, 80)
        if piedPage == None:
            pass
        else:
            draw_wrapped_line(p, piedPage, 60, 180, 980, 80)
        p.setFont('Helvetica', 44)
        p.drawString(2040, 1428, '{} DH'.format(round(total_art - tva_total, 2)))
        p.drawString(2040, 1300, '{} DH'.format(round(tva_total, 2)))
        p.setFont('Helvetica-Bold', 44)
        p.setFillColor('#ffffff')
        p.drawString(2040, 1168, '{} DH'.format(round(total_art, 2)))
        a = 2500
        b = a - 30
        p.setFont('Helvetica-Bold', 49)

        if i == pg.num_pages:
            break
        p.showPage()

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


@login_required
def factureUpdate(request, pk):
    instance = get_object_or_404(Facture, pk=pk)
    facture_edits = editFacture(request.POST or None, instance=instance)
    if facture_edits.is_valid():
        facture_edits.save()
        redirect('/facture')
    else:
        facture_edits = editFacture(request.POST or None, instance=instance)

    context = {
        'form': facture_edits
    }

    return render(request, 'facedit.html', context)
    
@login_required
def devisUpdate(request, pk):
    instance = get_object_or_404(Devis, pk=pk)
    facture_edits = editDevis(request.POST or None, instance=instance)
    if facture_edits.is_valid():
        facture_edits.save()
        redirect('/facture')
    else:
        facture_edits = editDevis(request.POST or None, instance=instance)

    context = {
        'form': facture_edits
    }

    return render(request, 'devisedit.html', context)

@login_required
def choicespdfbl(request, idFacture):
    factureInfo = Facture.objects.get(pk=idFacture)
    if factureInfo.is_Bl == True:
        t = redirect('/bl/{}'.format(factureInfo.pk))
    else:
        t = redirect('/pdf/{}'.format(factureInfo.pk))

    return t


@login_required
def pa(request, pk):
    Facture.objects.filter(id=pk).update(statut='Payer')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def im(request, pk):

    Facture.objects.filter(id=pk).update(statut='Impayee')

    return redirect(request.META.get('HTTP_REFERER'))  

@login_required
def pavente(request, pk):
    Ventes.objects.filter(id=pk).update(pay='ESPECE')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def imvente(request, pk):

    Ventes.objects.filter(id=pk).update(pay='DETTE')

    return redirect(request.META.get('HTTP_REFERER'))    

@login_required
def remiseData(request, name):
    na = str(name)
    na = na.split("-")
    vt = str(na[0])
    vt = vt.replace('%20', ' ')
    data = Product.objects.filter(name__contains=vt).first()
    dict = {'name':data.remise_grossite, 'prix': data.prix}
    return HttpResponse(json.dumps(dict), content_type='application/json')


def logoutPage(request):

    logout(request)
    return redirect('/')

"""
    with open('C:\\Users\\REDA\\Desktop\\para\\gest\\gest_product.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            prix = row[2]
            pri = prix
            print(pri)
            created = Product.objects.create(name=row[1], prix=pri,codeBarre=row[6])
"""