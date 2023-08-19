from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages # On créer les messages dans le fichier base.html



# Create your views here.

class HomeView(View):
    """ Main view """

    templates_name ='index.html'
    # objects.select_related('customer', 'save_by') permet de recupere les valeur d'autre entite
    # C'est parce que nous avons une relation ManyToMany
    invoices =  Invoice.objects.select_related('customer', 'save_by').all()

   
    context = {
        'invoices': invoices # elle represente l'ensembles des factures 
    }
    # Cette fonction permet de recuperer les données pour les mettre dans le tableau

    def get(self, request, *args, **kwags):

        return render(request, self.templates_name, self.context)
    
    # Cette fonction sert à envoyer des données
    
    def post(self, request, *args, **kwags):

        return render(request, self.templates_name, self.context)
    

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


