
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from .models import *

def pagination(request, invoices):
    # default_page 
        default_page = 1 

        page = request.GET.get('page', default_page)

        # paginate items

        items_per_page = 5

        paginator = Paginator(invoices, items_per_page)

        try:

            items_page = paginator.page(page)

        except PageNotAnInteger:

            items_page = paginator.page(default_page)

        except EmptyPage:

            items_page = paginator.page(paginator.num_pages) 

        return items_page    


  # Elle permet de mettre *args permet de mettre d'argument à l'infinit par contre **kwargs permet de mettre un dictionnaire d'argument à l'infinit


# on recupere l'id d'invoice donc pk est une clé primaire obj recupere l'objet invoice par la clé primaire pk


        # ON VEUT AVOIR TOUT LES ARTICLES RELIER A L'OBJET INVOICE exemple on veut recupere qui est le client qui à payer tout les article
def get_invoice(pk):
    """ get invoice fonction """

    obj = Invoice.objects.get(pk=pk)

    articles = obj.article_set.all()

    context = {
        'obj': obj,
        'articles': articles
    }

    return context