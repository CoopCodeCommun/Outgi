import time

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.html import format_html
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard_app.data import data

from dashboard_app.models import Contact, AccountAccount, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount, \
    Badge, DepensesBienveillance
from dashboard_app.odoo_api import OdooApi
from dashboard_app.serializers import UserSerializer
from .serializers import AccountAnalyticGroupSerializer
from dashboard_app.models import AccountAccount


def index(request):
    """
    Livre un template HTML
    Ne passe pas par l'api Django-Rest-Framework mais par le moteur de template de Django
    Template base.html dans le dossier templates
    avec un contexte qui contient le nom de l'utilisateur
    """
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'dashboard/example.html', context=context)


def julienjs_suivi_budgetaire(request):
    context = {}
    return render(request, 'pages_html/suivi_budgetaire.html', context=context)
    pass


def edit_tableau_generique(request, table, index):
    table = getattr(data, table)
    ligne = table['lignes'][index]
    if request.GET.get('edit'):
        return render(request, 'dashboard/tableau_generique_ligne_edit.html', context={'ligne':ligne, 'table':table, 'index':index})
    else :
        return render(request, 'dashboard/tableau_generique_ligne_read.html', context={'ligne':ligne, 'table':table, 'index':index})

def suivi_budgetaire(request):
    #### DEBUT DU CONTROLEUR
    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data,
    }

    return render(request, 'dashboard/pages_html/suivi_budgetaire.html', context=context)


def tableau_de_bord_perso(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'tableau_de_bord_perso.html', context=context)


def subventions(request):
    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data
        #'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'dashboard/pages_html/subventions.html', context=context)



def organigramme(request):
    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data
    }

    # import ipdb; ipdb.set_trace()
    return render(request, 'dashboard/pages_html/organigramme.html', context=context)


def repertoire(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'repertoire.html', context=context)


def objectifs_indicateurs(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'objectifs_indicateurs.html', context=context)


### CONTROLEUR API ###

class AccountAnalyticGroupAPI(viewsets.ViewSet):
    # Un ViewSet est un outil qui permet te tout faire en un seul coup :
    # https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
    # On se sert d'un serializer pour formater la réponse et filtrer les données

    def list(self, request):
        # Pour récupérer tous les éléments
        serializer = AccountAnalyticGroupSerializer(AccountAnalyticGroup.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Pour récupérer un seul élément avec le pk (primary key, ici, c'est un uuid4)
        serializer = AccountAnalyticGroupSerializer(AccountAnalyticGroup.objects.get(pk=pk))
        return Response(serializer.data)

    # Créer un élément. Il est parfois préférable de fabriquer un autre serializer qui va servir de formulaire de validation.
    # def create(self, request):
    #     serializer = CreateCardSerializer(data=json.loads(request.data.get('cards')), context={'request': request}, many=True)
    #     if serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        # On peut choisir les permissions suivant l'action.
        # Par exemple pour créer ou détruire un objet, il faut être authentifié
        # if self.action in ['create', 'destroy']:
        #     permission_classes = [IsAuthenticated]
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class OdooContactsAPI(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # Récupération du contact demandé
        contact = Contact.objects.get(pk=pk)

        # Le retrieve est activé avec un hx-get :
        #     bouton cancel du tableau contact en mode écriture
        #     bouton modal du tableau contact
        #     bouton edit du tableau odoo contact

        if request.query_params.get('cancel'):
            return render(request, 'htmx/odoo_contacts_table_row.html', context={'contact': contact})

        if request.query_params.get('modal'):
            # Je simule un temps de chargement pour que tu puisse voir le spinner :)
            time.sleep(0.5)
            return render(request, 'htmx/odoo_contacts_modal_info.html', context={'contact': contact})

        # ce n'est ni un modal ni un cancel
        # Envoie du formulaire de modification du contact
        return render(request, 'htmx/odoo_contacts_edit_row.html', context={'contact': contact})

    def update(self, request, pk=None):
        # Le update est activé avec le hx-put du bouton save du tableau odoo contact
        contact = Contact.objects.get(pk=pk)

        # On récupère les données des formulaires et on remplace en base de donnée si nécessaire
        # Pas très élégant, on passera par un serializer pour faire ça proprement
        if request.data.get('nom') != contact.nom:
            contact.nom = request.data.get('nom')
        if request.data.get('structure') != contact.structure:
            contact.structure = request.data.get('structure')
        if request.data.get('adresse') != contact.adresse:
            contact.adresse = request.data.get('adresse')
        contact.save()

        return render(request, 'htmx/odoo_contacts_table_row.html', context={'contact': contact})

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


# Page d'exemple d'implémentation de l'API
def api_exemple(request):
    context = {}
    return render(request, 'api/from_api_exemple.html', context=context)


### PAGE D'EXAMPLE HTMX ###


def odoo_account(request):
    context = {
        "AccountAccounts": AccountAccount.objects.all().order_by('code'),
        "AccountJournals": AccountJournal.objects.all().order_by('name'),
        "AccountAnalyticGroup": AccountAnalyticGroup.objects.all().order_by('name'),
        "AccountAnalyticAccount": AccountAnalyticAccount.objects.all().order_by('code'),
    }
    return render(request, 'htmx/odoo_account.html', context=context)


@permission_classes([AllowAny])
class reload_account_from_odoo(APIView):
    def get(self, request, uuid=None):
        odooApi = OdooApi()
        odooApi.get_account_account()
        odooApi.get_account_journal()
        odooApi.get_account_analytic()
        context = {
            "AccountAccounts": AccountAccount.objects.all().order_by('code'),
            "AccountJournals": AccountJournal.objects.all().order_by('name'),
            "AccountAnalyticGroup": AccountAnalyticGroup.objects.all().order_by('name'),
            "AccountAnalyticAccount": AccountAnalyticAccount.objects.all().order_by('code'),
        }
        return render(request, 'htmx/odoo_account_button_dropdown.html', context=context)


def contacts(request):
    # On va chercher tout les objets de la table Contact
    # de la base de donnée (models.puy)
    # Pour l'exemple, on ne prend que ceux qui sont "Membership"
    contacts = Contact.objects.all()
    context = {
        'contacts': contacts[:5]
    }
    return render(request, 'htmx/odoo_contacts.html', context=context)


@permission_classes([AllowAny])
class reload_contact_from_odoo(APIView):
    def get(self, request, uuid=None):
        # Mise à jour la base de donnée depuis Odoo
        # requete appellé par le bouton "Mise à jour depuis Odoo"

        # pour simuler le spinner :
        # time.sleep(1)

        # Mise à jour la base de donnée depuis Odoo
        odooApi = OdooApi()
        contacts = odooApi.get_all_contacts()

        # On va chercher tous les objects Contact
        # dans la base de donnée mise à jour
        context = {
            'contacts': contacts[:10],
        }
        return render(request, 'htmx/odoo_contacts_table.html', context=context)


# HTMX USE CASES

@permission_classes([AllowAny])
class lazy_loading_profil_image(APIView):
    def get(self, request, uuid=None):
        context = {
            'contact': Contact.objects.get(pk=uuid)
        }
        return render(request, 'htmx/lazy_loading.html', context=context)
    
