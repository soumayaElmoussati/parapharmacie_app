from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import *

class cat_form(ModelForm):
    
    class Meta:
        model = Categories
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'aria-label':'Default', 'aria-describedby': 'inputGroup-sizing-default'})
        }

class prodForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'categorie': forms.Select(attrs={ 'class':'selectpicker form-control', 'data-style':'py-0'}),
            'date_expire': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'autocomplete':'off'}),
        }

class stockFrom(ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        exclude = ('produit',)
        widgets = {
            
            'date': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'autocomplete':'off'}),
        }

class ven_form_model(ModelForm):

    class Meta:
        model = Ventes
        fields = '__all__'

        widgets = {
            'produit': forms.Select(attrs={ 'class':'selectpicker form-control', 'data-style':'py-0'})
        }

class productEdit(ModelForm):

    class Meta:

        model = Product

        fields = '__all__'

        widgets = {
            'date_expire': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'autocomplete':'off'}),
        }

class clientEdit(ModelForm):
    class Meta:

        model = Client

        fields = '__all__'

class panier_form(ModelForm):

    class Meta:

        model = Panier
        fields = '__all__'

        widgets = {
            'nom': forms.Select(attrs={ 'class':'selectpicker form-control', 'data-style':'py-0'})
        }

class journalVente(ModelForm):

    class Meta:

        model = Ventes
        fields = '__all__'

class client_form(ModelForm):

    class Meta:

        model = Client
        fields = '__all__'
        exclude = ['point']

class frs_form(ModelForm):

    class Meta:

        model = Fournisseur
        fields = '__all__'

class creance_form(ModelForm):

    class Meta:

        model = Creance
        fields = '__all__'

class dette_form(ModelForm):

    class Meta:

        model = Dette
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'autocomplete':'off'}),
            'date_creation': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'autocomplete':'off'}),
        }


class factureForm(forms.ModelForm):

    class Meta:
        model = Facture
        fields = '__all__'
        exclude = ('ref', 'horsTaxe', 'tva', 'toutTaxe', 'montant', 'piedPage', 'statut', 'commercant', 'is_Facture', 'num_facture', 'is_Bl', 'num_bl',)


class editFacture(forms.ModelForm):

    class Meta:
        model = Facture
        fields = '__all__'
        exclude =  ('ref', 'horsTaxe', 'tva', 'commercant', 'is_Facture', 'num_facture', 'is_Bl', 'num_bl',)

        widgets = {
            'toutTaxe': forms.TextInput(attrs={'disabled': 'disabled'}),
            'montant': forms.TextInput(attrs={'value': 'Arrêter La Présente Facture A La Somme De : '})
        }

class editDevis(forms.ModelForm):

    class Meta:
        model = Devis
        fields = '__all__'
        exclude =  ('ref', 'horsTaxe', 'tva', 'commercant',)

        widgets = {
            'toutTaxe': forms.TextInput(attrs={'disabled': 'disabled'}),
            'montant': forms.TextInput(attrs={'value': 'Arrêter Le Présent Devis A La Somme De : '})
        }


class devisForm(forms.ModelForm):

    class Meta:
        model = Devis
        fields = '__all__'
        exclude = ('ref', 'horsTaxe', 'tva', 'toutTaxe', 'montant', 'piedPage', 'commercant',)



class paimentForm(forms.ModelForm):

    class Meta:

        model = Paiment
        fields = '__all__'
        exclude =  ('client',)
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'autocomplete':'off'}),
        }
