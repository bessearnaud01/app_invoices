

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

"""

Décorateurs de vue¶
Django fournit plusieurs décorateurs afin de permettre aux vues de prendre en charge différentes fonctionnalités HTTP.

Voir Décoration de la classe pour savoir comment utiliser ces décorateurs avec les vues fondées sur des classes.

Méthodes HTTP autorisées¶
Les décorateurs présents dans django.views.decorators.http peuvent être utilisés pour restreindre l’accès à une vue en se basant sur la méthode utilisée lors de la requête. 
Ces décorateurs renvoient une instance de django.http.HttpResponseNotAllowed si les conditions ne sont pas remplies.

"""

# definition de la fonction superuser_require

def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in and if the user is a superuser,
    redirecting to the log-in page if necessary.

    Décorateur de vues qui vérifie que l'utilisateur est connecté et si l'utilisateur est un superutilisateur,
    redirection vers la page de connexion si nécessaire.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,# La fonction lamdba verifie si l'utilisaateur est authentifie
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    """
    Un decorateur est une fonction qui reçoit en paramètre une autre fonction et function = none est egal à if function:
    def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    if function:
        return actual_decorator(function)
    return actual_decorator


"""
    Si une vue utilise cette classe mixin, toutes les requêtes par des utilisateurs 
    non authentifiés seront redirigées vers la page de connexion ou traitées comme des erreurs HTTP 403
"""
class LoginRequiredSuperuserMixim(UserPassesTestMixin):

    """ Mixin for superuser """

    def test_func(self):
        return self.request.user.is_superuser