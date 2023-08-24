from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages # On créer les messages dans le fichier base.html
from django.db import transaction

import pdfkit

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.template.loader import get_template

from django.http import HttpResponse

from .utils import pagination,get_invoice




# Create your views here.

class HomeView(View):
    """ Main view On va afficher les invoice dans le fichier index.html  """ 

    templates_name ='index.html'
    # objects.select_related('customer', 'save_by') permet de recupere les valeur d'autre entite
    # C'est parce que nous avons une relation ManyToMany
    #-invoice_date_time represente la date d'ajout de la facture verifie ds le modele on veut lire les facture en fonction de la ddate
    invoices =  Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')

   
    context = {
        'invoices': invoices # elle represente l'ensembles des factures 
    }
    # Cette fonction permet de recuperer les données pour les mettre dans le tableau

    def get(self, request, *args, **kwags):
        items = pagination(request, self.invoices) # la fonction pagination se trouve ds le fichier utils.py

        self.context['invoices'] = items

        return render(request, self.templates_name, self.context)
    

    # Cette fonction sert à envoyer des données
    
    def post(self, request, *args, **kwags):


          # modify an invoice
          # On teste si valeur existe request.POST.get('id_modified')

        if request.POST.get('id_modified'):

            paid = request.POST.get('modified') # paid prend la valeur du name= modified

            try: 

                 # obj recupere l'id_modified
                obj = Invoice.objects.get(id=request.POST.get('id_modified'))
                # si l'utilisateur choisit paid = true alors obj.paid= True

                if paid == 'True':

                    obj.paid = True

                else:
                     # si l'utilisateur choisit paid = false alors obj.paid= false

                    obj.paid = False 
                # On sauvegarde l'objet
                obj.save() 

                messages.success(request,("Change made successfully.")) 

            except Exception as e:   

                messages.error(request, f"Sorry, the following error has occured {e}.")   
            

             # deleting an invoice   ou on veut supprimer la facture
             # on va teste si l'id 

        if request.POST.get('id_supprimer'):

            try:

                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))

                obj.delete()

                messages.success(request,("The deletion was successful."))   

            except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")     


        # Elle nous permet de rafraichir notre table donc le met après les fonction get, post
        items = pagination(request, self.invoices)

        self.context['invoices'] = items

        return render(request, self.templates_name, self.context)
    




# On veut ajouter une nouveau client donc on crée une nouvelle classe
# cette classe elle est utile au fichier add_customer.html

class AddCustomerView(View):

    """ Main view """
    templates_name ='add_customer.html'

    def get(self, request, *args, **kwags):

        return render(request, self.templates_name)
    
    # Cette fonction sert à envoyer des données
    
    def post(self, request, *args, **kwags):
        # On peut tester l'envoie du formulaire avec cette methode print(request.POST)
        #print(request.POST)
        data = {
            'name': request.POST.get('name'), # elle represent id du forumlaire
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user # Elle presente le user qui celui qui a enregister la facture ou invoice en anglais
        }
        try:
            created = Customer.objects.create(**data)
            if created:
                # import message et l'affiche ensuite
                messages.success(request, "Customer registered successfully.")
            else:
                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:
               
         messages.error(request, f"Sorry our system is detecting the following issues {e}.")

        return render(request, self.templates_name)   


# cette Classe permet d'ajouter une nouvelle  facture

class AddInvoiceView(View):

    """ new invoice view """
    templates_name ='add_invoice.html'
    # On veut recupere l'ensemble de client et l'utilisateur qui la enregister quand on veut recupere d'autre valeur d'une table on met select_related
    customers =  Customer.objects.select_related('save_by').all()

    context = {
        'customers': customers # elle represente l'ensembles des factures 
    }

    def get(self, request, *args, **kwags):

        return render(request, self.templates_name,self.context)
    
    # Elle permet d'empêcher d'envoyer les données au cas ou il y a probleme
    @transaction.atomic()
    
    def post(self, request, *args, **kwags):

        #print(request.POST)
        items = [] # items represente la liste des articles

        try: 
            # Elle vient du fichier js  request.POST.get('customer')
            # getlist permet d'avoir une liste d'article et chaque article à ça qty, unit et total-a
            customer = request.POST.get('customer') 

            type = request.POST.get('invoice_type')

            articles = request.POST.getlist('article')

            qties = request.POST.getlist('qty')

            units = request.POST.getlist('unit')

            total_a = request.POST.getlist('total-a')

            total = request.POST.get('total')

            comment = request.POST.get('commment')
            #On créer l'objet sachant  une facture aura toujours un customer_id,save_by,total,invoice_type et comment
            # Par contre qty, unit, total-a va depend des de la quantite que le client veut donc on ne met pas l'objet invoice_objet
            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,# Elle represente l'utilisateur connecté
                'total': total,# elle ne represente pas le total à payer de la facture
                'invoice_type': type,
                'comments': comment
            }
            invoice = Invoice.objects.create(**invoice_object)
            # Sachant que une facture peut avoir plusieurs article

            for index, article in enumerate(articles): # Enumerate sert à lister l'index et l'élément ou la variable

                data = Article(
                    invoice_id = invoice.id,
                    name = article,
                    quantity=qties[index],
                    unit_price = units[index],
                    total = total_a[index],
                )

                items.append(data) # On a ajoute le data dans la liste items[] déclare en haut
            # bulk_create crée liste d'element d'objet
            created = Article.objects.bulk_create(items)   
            if created:
                # Si l'article
                messages.success(request, "Data saved successfully.") 
            else:
                messages.error(request, "Sorry, please try again the sent data is corrupt.")    

        except Exception as e:
               messages.error(request, f"Sorry the following error has occured {e}.")   
        return render(request, self.templates_name,self.context)


# cette classe Elle permet de visualiser la facture du client
class InvoiceVisualizationView(View):
    """ This view helps to visualize the invoice """

    templates_name = 'invoice.html'

    # Elle sert à passer plusieurs argument dams une fonction
    # Elle permet de mettre *args permet de mettre d'argument à l'infinit par contre **kwargs permet de mettre un dictionnaire d'argument à l'infinit

    def get(self, request, *args, **kwargs):
        # on recupere l'id d'invoice donc pk est une clé primaire obj recupere l'objet invoice par la clé primaire pk


        # ON VEUT AVOIR TOUT LES ARTICLES RELIER A L'OBJET INVOICE exemple on veut recupere qui est le client qui à payer tout les article
        pk = kwargs.get('pk')
        # get_invoice est une fonction du utils.py
        # c'est ce get_invoice qui permet  de recuperer les valeurs de cette fonction
        context = get_invoice(pk)

        return render(request, self.templates_name, context)

        


    # cette fonction permet de generer une facture pdf
    #@superuser_required
    def get_invoice_pdf(request, *args, **kwargs):
        """ generate pdf file from html file """
        # On va chercher à recuperer l'id de la facture
        pk = kwargs.get('pk')
        # get_invoice est une fonction du utils.py
        # c'est ce get_invoice qui permet  de recuperer les valeurs de cette fonction
        context = get_invoice(pk) 

        context['date'] = datetime.datetime.today()

        # get html file
        template = get_template('invoice-pdf.html')

        # render html with context variables

        html = template.render(context)

        # options of pdf format 

        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            "enable-local-file-access": ""
        }

        # generate pdf 

        pdf = pdfkit.from_string(html, False, options)

        response = HttpResponse(pdf, content_type='application/pdf')

        response['Content-Disposition'] = "attachement"

        return response



