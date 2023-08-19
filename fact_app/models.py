from django.db import models
from django.contrib.auth.models import User

# On va mettre ses modele dans le fichier admin.py 

class Customer(models.Model):
    """
    Name: Customer model definition
    """
    SEX_TYPES = (
        ('M', ('Male')),
        ('F',('Feminine')),
    )
    name = models.CharField(max_length=132)

    email = models.EmailField()

    phone = models.CharField(max_length=132)

    address = models.CharField(max_length=64)

    sex = models.CharField(max_length=1, choices=SEX_TYPES)

    age = models.CharField(max_length=12)

    city = models.CharField(max_length=32)

    zip_code = models.CharField(max_length=16)

    created_date = models.DateTimeField(auto_now_add=True)
    # On veut savoir quel utilisateur a enregister le client donc on fait save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    # On va importe l'utilisateur en faisant from django.contrib.auth.models import User
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta: 
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name     
    

class Invoice(models.Model): 
    """
    Name: Invoice model definition
    Description: 
    author:besseberenger@gmail.com
    """
    INVOICE_TYPE = (
        ('R', ('RECEIPT')),
        ('P', ('PROFORMA INVOICE')),
        ('I',('INVOICE'))
    )

    # ForeignKey(Customer, on_delete=models.PROTECT) est utile comme le clé
    # On sait une facture a appartient à un client donc pour avoir accès aux données du client
    # On veut recuperer le nom et la date de quand le client a été inscrit
    # et un client peut avoir plusieurs factures
    """
    Model Meta is basically the inner class of your model class. 
    Model Meta is basically used to change the behavior of your model fields like changing order options,verbose_name, and a lot of other options. 
    It’s completely optional to add a Meta class to your model. 
    In order to use model meta you have to add class Meta in your model as shown below as follows: 

    """
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT) # On veut recuperer le nom et dats les valeur de customer donc on defi

    save_by = models.ForeignKey(User, on_delete=models.PROTECT) # Et utilisateur peut enregister pluseiur facture

    invoice_date_time = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(max_digits=10000, decimal_places=2) # decimal_places=2 deux chiffre apres la virgule

    last_updated_date = models.DateTimeField(null=True, blank=True)# La date de la mise à jour

    paid  = models.BooleanField(default=False) # paid est un boolean et represente une status parce qu'il n est pas encore donc il est false

    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)

    comments = models.TextField(null=True, max_length=1000, blank=True)

    
    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
           return f"{self.customer.name}_{self.invoice_date_time}"
    
    
    @property
    def get_total(self):
        articles = self.article_set.all() # article_set.all() permet de recuperer tout les articles d'une relation onetoMany parce que une facture a plusieurs articles 
        # on fait la somme de chaque article apres on fait la somme total des prix des prix à payer get_total est la fonction de la classe article    
        total = sum(article.get_total for article in articles) 
        return total
 
 
class Article(models.Model):
    """
    Name: Article model definiton
    Descripiton: 
    Author: besseberenger@gmail.com
    """
    #  on_delete=models.CASCADE son utilité est lorsqu'on supprime une facture facture tout les article st aussi supprimer 

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)# Un article doit être relié a une facture

    name = models.CharField(max_length=32)

    quantity = models.IntegerField()

    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)

    total = models.DecimalField(max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
    # Elle le prix total d'un article
    @property
    def get_total(self):
        total = self.quantity * self.unit_price   
        return total 
        