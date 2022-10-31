from escpos.printer import Usb
from datetime import date
from django.db.models import Sum
from .models import *

p = Usb(idVendor=0x0619, idProduct=0x0127, timeout=0 ,in_ep=0x81, out_ep=0x01)


day = date.today().day
month = date.today().month
year = date.today().year

def printw(*args):


    p.set(align='CENTER', width=3, height=3)
    p.text("Flana Para\n")
    p.set(align='CENTER', width=1, height=1)
    p.text("------------------------------\n")
    p.text('Parapharmacie')
    p.text("\n")
    p.text("\n")
    p.text("Date : {}/{}/{}, Telephone : 06.67.01.84.91".format(day, month, year))
    p.text("\n")
    p.text("\n")
    p.text("Produits--------------------------------Prix\n")
    p.text("\n")
    p.set(align='RIGHT', width=1, height=1)
    ap = Panier.objects.all()
    tote = Panier.objects.all().aggregate(Sum('p_total')).get('p_total__sum')
    for i in ap:
        lent = str(i.nom)
        lentp = len(lent)
        lep = 30
        lep = lep - lentp
        spacer =  lep * " "
        p.text("{}  {}{}{:0.2f} DH\n".format(i.quantite, i.nom, spacer, i.p_total))
        #p.text("{}             {} DH\n".format(i.nom, i.prix))
    p.set(align='CENTER', width=2, height=2)
    p.text("\n")
    p.text("\n")
    p.text('Total  :   {} DH'.format(tote))
    p.text("\n")
    p.text("\n")
    p.cut()