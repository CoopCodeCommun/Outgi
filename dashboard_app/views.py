import time

from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.utils.html import format_html
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard_app.data import data
from dashboard_user.models import CustomUser, ContactProvisional
from dashboard_app.models import PrevisionCost, Recette, Groupe
from dashboard_app.models import (Contact, AccountAccount, AccountJournal, AccountAnalyticGroup, AccountAnalyticAccount, \
    RealCostInternSpending, RealCost, RealCostExternService, PrestationsVentsRecettesInt, Grant, Cost,
    OrganizationalChart, Badge, DepensesBienveillance, Pole)
from dashboard_app.odoo_api import OdooApi
from dashboard_app.serializers import UserSerializer
from dashboard_app.serializers import (AccountAnalyticGroupSerializer, OrganizationalChartValidator, RealcostSerializer,
        PrestationsVentsRecettesIntValidator, PrevisionCostSerializer, RealCostExternServiceSerializer,
        RealCostIntSpendSerializer, PrestationsVentsRecettesIntSerializer)
from dashboard_app.models import AccountAccount
from rest_framework.viewsets import ViewSet

# We'll create a fonction that will return a dictionary in the form adapted to
# the generale tables
def create_dict_with_data(slug_name, colonnes,lignes, total,new_ligne,new_line_name="", url_viewset="",titre_colonne=""):

    return {
        "slug": slug_name,
        "titre": titre_colonne,
        "colonnes": colonnes,
        "lignes": lignes,
        "total": total,
        "ajouter_ligne" : new_ligne,
        'new_line_name': new_line_name,
        'url_viewset': url_viewset
    }


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
    else:
        return render(request, 'dashboard/tableau_generique_ligne_read.html', context={'ligne':ligne, 'table':table, 'index':index})


# in this method we will factorize the method of filtering the data for PrevisionCost,
# serializing and thant creating the data dictionary taht will send to the template
def refactor_cost_prev(model,data_type,type,name_table,serializer, total):
    # passing datas through the serializer by selecting the type of Cost Prevision
    queryset = model.filter(type__type=type)
    cost_serializer = serializer(queryset, many=True)
    # creating the dictionary that will send thee datas through context
    data_type['lines'] = cost_serializer.data
    data_type['total'] = total
    data_type['name_table'] = name_table+type
    data_type['columns'] = [{'nom':''}, {'nom':'amount'},{'nom':'editer'},{'nom':'effacer'}]
    data_type['list_include'] = ['titled', 'amount']
    data_type['new_line_name'] = 'prevision'+type


# Refacotr for retrive method in viewsets:
def refactor_retrive(model,given_pk, model_serializer):
    model_obj = model.objects.get(pk=given_pk)
    serialized_obj = model_serializer(model_obj, many=False)
    return serialized_obj.data



# creating a refacor for destroyn selected object from all viewsets of Cost prevision
def destroy_refactor(given_pk, model):
    all_objects = model.objects.all()
    obj = get_object_or_404(all_objects, pk=given_pk)
    obj.delete()


# creating a viewset class for Caring (bienveillance) prevision cost table
class PrevisionBudgetCaringViewset(viewsets.ModelViewSet): #PrevisionBudgetCaringViewset
    def list(self, request):
        prevision_cost, prevision_intern_service = {}, {}
        prevision_extern_service, intern_spends = {},{}
        model = PrevisionCost.objects.all()
        refactor_cost_prev(model,prevision_cost, 'CAR','prev_cost_tab', PrevisionCostSerializer, True)
        refactor_cost_prev(model, prevision_intern_service, 'IN_S', 'prev_cost_tab',PrevisionCostSerializer, True)
        refactor_cost_prev(model,prevision_extern_service, 'EX_S', 'prev_cost_tab', PrevisionCostSerializer, True)
        refactor_cost_prev(model, intern_spends, 'SP_I', 'prev_cost_tab',PrevisionCostSerializer, True)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template,
                    'prevision_cost': prevision_cost,
                    'prevision_intern_service': prevision_intern_service,
                    'prevision_extern_service': prevision_extern_service,
                    'intern_spends': intern_spends
                    }

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html',
                      context=context)


    def retrieve(self, request, pk=None):
        # prev_cost = PrevisionCost.objects.get(pk=pk)
        # prev_cost_serializer = PrevisionCostSerializer(prev_cost, many=False)
        prev_cost_ser_data = refactor_retrive(PrevisionCost,pk, PrevisionCostSerializer)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if 'cancel' in request.GET:

            line = prev_cost_ser_data
            # Return the original table row HTML
            context = {
                'base_template': base_template, 'line': line,
                'list': ['titled', 'amount']
            }

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'htmx/cost_prev_row_edit.html',
                      {'prev_cost_ser_data': prev_cost_ser_data})

    def create(self, request):
        serializer = PrevisionCostSerializer(data=request.data)
        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if serializer.is_valid():
            serializer.save()
            line = serializer.data

            context = {'base_template': base_template, 'line': line,
                       'list': ['titled', 'amount']}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
                'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):

        queryset = PrevisionCost.objects.all()
        car = get_object_or_404(queryset, pk=pk)
        serializer = PrevisionCostSerializer(car, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            line = serializer.data

            base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
            context = { 'base_template': base_template, 'line': line,
                        'list':['titled','amount']}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk=None):
        # calling the refactor destroy to delete selected obj
        destroy_refactor(pk, PrevisionCost)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# create viewset class for Real cost of caring and intern service
class RealCostCaringInternServiceViewSet(viewsets.ModelViewSet):
    def list(self, request):
        caring_real, int_service_real = {}, {}
        model = RealCost.objects.all()

        refactor_cost_prev(model,caring_real, 'CAR', 'real_cost_tab',RealcostSerializer, True)
        refactor_cost_prev(model,int_service_real, 'IN_S', 'real_cost_tab', RealcostSerializer, True)

        caring_real['columns'] = [{'nom': ''},
                                  {'nom': 'date'},
                                  {'nom': 'proposition'},
                                  {'nom': 'validé'},
                                  {'nom': 'facturé'},
                                  {'nom': 'payé'},
                                  {'nom': 'editer'},
                                  {'nom':'effacer'}]
        caring_real['list_include'] = ['username','date','proposition','validated', 'invoiced','payed']
        caring_real['new_line_name'] = 'real_cost'+'CAR'

        int_service_real['columns'] = [{'nom':''},
                                       {'nom':'date'},
                                       {'nom':'proposition'},
                                       {'nom':'validé'},
                                       {'nom':'facturé'},
                                       {'nom':'payé'},
                                       {'nom': 'editer'},
                                       {'nom':'effacer'}]
        int_service_real['list_include'] = ['username','date','proposition','validated', 'invoiced','payed']
        int_service_real['new_line_name'] = 'real_cost'+'IN_S'

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template,
                    'caring_real': caring_real,
                    'int_service_real':int_service_real
                    }

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html',
                      context=context)


    def retrieve(self, request, pk=None):
        # real_cost_car = RealCost.objects.get(pk=pk)
        # real_cost_car_serializer = RealcostSerializer(real_cost_car, many=False)
        real_cost_serialized_data = refactor_retrive(RealCost,pk, RealcostSerializer)

        list = ['username','date','proposition','validated', 'invoiced','payed']

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if 'cancel' in request.GET:

            line = real_cost_serialized_data
            # Return the original table row HTML
            context = {
                'base_template': base_template, 'line': line,
                'list': list
            }

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'htmx/cost_real_row_edit.html',
                      {'real_cost_serialized_data': real_cost_serialized_data})


    def create(self, request):
        # Verify why we can't pass imediatly request.data in Serializer...
        given_data = request.POST.copy()
        real_cost_serializer = RealcostSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        # import ipdb; ipdb.set_trace()
        if real_cost_serializer.is_valid():
            real_cost_serializer.save()
            line = real_cost_serializer.data
            list = ['username','date','proposition','validated', 'invoiced','payed']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
                'dashboard/tableau_generique_ligne_read.html',context=context)



    def update(self, request, pk=None):
        queryset = RealCost.objects.all()
        cost_reel = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = RealcostSerializer(cost_reel, data=given_data, partial=True)

        list = ['username','date','proposition','validated', 'invoiced','payed']


        if serializer.is_valid():
            serializer.save()

            line = serializer.data

            base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
            context = { 'base_template': base_template, 'line': line,
                        'list':list}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)



    def destroy(self, request, pk=None):
        # calling the refactor destroy to delete selected obj
        destroy_refactor(pk, RealCost)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# create viewset class for Real cost of caring and intern service
class RealCostPurchaseViewSet(viewsets.ModelViewSet):

    def list(self, request):
        purchase_real_cost = {}

        model = RealCostExternService.objects.all()
        refactor_cost_prev(model, purchase_real_cost,
                           'EX_S',
                           'real_cost_tab',
                           RealCostExternServiceSerializer, True)

        purchase_real_cost['columns'] = [{'nom': ''},
                                         {'nom': 'intitulé'},
                                         {'nom': 'date'},
                                         {'nom': 'validé'},
                                         {'nom': 'payé'},
                                         {'nom': 'editer'},
                                         {'nom':'effacer'}
                                         ]
        purchase_real_cost['list_include'] = ['contact_name',
                                              'titled', 'date',
                                              'validated',
                                              'invoiced',
                                              'payed']
        purchase_real_cost['new_line_name'] = 'real_cost' + 'EX_S'

        base_template = "dashboard/partial.html" if request.htmx else \
            "dashboard/base.html"

        context = {'base_template': base_template,
                   'purchase_real_cost':purchase_real_cost}

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html',
                   context=context)


    def retrieve(self, request, pk=None):

        purchase_serialized_data = refactor_retrive(RealCostExternService,pk, RealCostExternServiceSerializer)
        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        list = ['contact_name', 'titled', 'date', 'validated', 'payed']

        if 'cancel' in request.GET:

            line = purchase_serialized_data
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'line': line,
                'list': list
            }

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'edit_line/purchase_row_edit.html',
                      {'purchase_serialized_data': purchase_serialized_data})

    def create(self, request):
        given_data = request.POST.copy()
        purchase_serializer = RealCostExternServiceSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if purchase_serializer.is_valid():
            purchase_serializer.save()
            line = purchase_serializer.data
            list = ['contact_name', 'titled', 'date', 'validated', 'invoiced', 'payed']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
                'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):
        queryset = RealCostExternService.objects.all()
        purchase_cost = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = RealCostExternServiceSerializer(purchase_cost, data=given_data, partial=True)

        list = ['contact_name', 'titled', 'date', 'validated', 'invoiced', 'payed']


        if serializer.is_valid():
            serializer.save()

            line = serializer.data

            base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
            context = { 'base_template': base_template, 'line': line,
                        'list':list}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk=None):
        #calling the destroy refactor method to delete selected object
        destroy_refactor(pk, RealCostExternService)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# creating viewset class for intern real depenses
class RealInternSpendViewSet(viewsets.ModelViewSet):
    def list(self,request):
        intern_spend = {}
        model = RealCostInternSpending.objects.all()
        refactor_cost_prev(model,intern_spend,
                           'SP_I',
                           'real_cost_tab',
                           RealCostIntSpendSerializer,
                           True)

        intern_spend['columns'] = [{'nom': ''},
                                   {'nom': 'date'},
                                   {'nom': 'montant'},
                                   {'nom': 'editer'},
                                   {'nom': 'effacer'}]
        intern_spend['list_include'] = ['pole_name', 'date_cost', 'amount']
        intern_spend['new_line_name'] = 'real_cost' + 'SP_I'

        base_template = "dashboard/partial.html" if request.htmx else \
            "dashboard/base.html"

        context = {'base_template': base_template,
                   'intern_spend':intern_spend}

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html',
                   context=context)


    def retrieve(self, request, pk=None):
        intern_spending_data = refactor_retrive(RealCostInternSpending,pk, RealCostIntSpendSerializer)
        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        list = ['pole_name', 'date_cost', 'amount']

        if 'cancel' in request.GET:

            line = intern_spending_data
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'line': line,
                'list': list
            }

            return render(request,
                    'dashboard/tableau_generique_ligne_read.html',
                          context=context)

        return render(request, 'edit_line/intern_spend_row_edit.html',
                      {'intern_spending_data': intern_spending_data})

    def create(self,request):
        given_data = request.POST.copy()
        intern_spending_serializer = RealCostIntSpendSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if intern_spending_serializer.is_valid():
            intern_spending_serializer.save()
            line = intern_spending_serializer.data
            list = ['pole_name', 'date_cost', 'amount']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request, 'dashboard/tableau_generique_ligne_read.html',context=context)


    def update(self, request, pk=None):
        queryset = RealCostInternSpending.objects.all()
        intern_spending = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = RealCostIntSpendSerializer(intern_spending, data=given_data, partial=True)

        list = ['pole_name', 'date_cost', 'amount']

        if serializer.is_valid():
            serializer.save()

            line = serializer.data

            base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
            context = { 'base_template': base_template, 'line': line,
                        'list':list}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk=None):
        #calling the destroy refactor method to delete selected object
        destroy_refactor(pk, RealCostInternSpending)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


# in this method we will factorize the method of filtering the data for Recettes,
# serializing and thant creating the data dictionary taht will send to the template
def refactor_recette(model,p_or_r,data_type,type,name_table,serializer, total):
    # passing datas through the serializer by selecting the type of Cost Prevision
    queryset = model.filter(prev_ou_reel=p_or_r,recette__type=type)
    cost_serializer = serializer(queryset, many=True)
    # creating the dictionary that will send thee datas through context
    data_type['lines'] = cost_serializer.data
    data_type['total'] = total
    data_type['name_table'] = name_table+p_or_r+type
    data_type['columns'] = [{'nom':''}, {'nom':'amount'},{'nom':'editer'},{'nom':'effacer'}]
    data_type['list_include'] = ['groupe_name', 'amount']
    data_type['new_line_name'] = 'recette'+p_or_r+type


# creating viewset class for recettes
class PrestationsVentsRecettesIntViewset(viewsets.ModelViewSet):
    def list(self, request):
        recettest_presta_prev, recettest_presta_real = {}, {}
        recette_sells_prev, recette_sells_real = {}, {}
        recette_intern_prev, recette_intern_real = {}, {}

        model = PrestationsVentsRecettesInt.objects.all()
        refactor_recette(model,'P',recettest_presta_prev,'P','recette_prev_tab',PrestationsVentsRecettesIntSerializer,True)
        refactor_recette(model,'R',recettest_presta_real,'P','recette_real_tab',PrestationsVentsRecettesIntSerializer,True)
        refactor_recette(model,'P',recette_sells_prev,'V','recette_prev_tab',PrestationsVentsRecettesIntSerializer,True)
        refactor_recette(model,'R',recette_sells_real,'V','recette_real_tab',PrestationsVentsRecettesIntSerializer,True)
        refactor_recette(model,'P',recette_intern_prev,'R_IN','recette_prev_tab',PrestationsVentsRecettesIntSerializer,True)
        refactor_recette(model,'R',recette_intern_real,'R_IN','recette_real_tab',PrestationsVentsRecettesIntSerializer,True)

        base_template = "dashboard/partial.html" if request.htmx else \
            "dashboard/base.html"

        context = {'base_template': base_template,
                   'recettest_presta_prev':recettest_presta_prev,
                   'recettest_presta_real':recettest_presta_real,
                   'recette_sells_prev':recette_sells_prev,
                   'recette_sells_real':recette_sells_real,
                   'recette_intern_prev':recette_intern_prev,
                   'recette_intern_real':recette_intern_real
                   }

        return render(request, 'dashboard/pages_html/suivi_budgetaire.html',
                   context=context)

    def retrieve(self, request, pk=None):
        recette_serialized_data = refactor_retrive(PrestationsVentsRecettesInt,pk, PrestationsVentsRecettesIntSerializer)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        list = ['groupe_name', 'amount']

        # import ipdb; ipdb.set_trace()
        if 'cancel' in request.GET:

            line = recette_serialized_data
            # Return the original table row HTML
            context = {
                'base_template': base_template,
                'line': line,
                'list': list
            }
            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                context=context)

        return render(request, 'edit_line/recette_row_edit.html',
                      {'recette_serialized_data': recette_serialized_data})



    def create(self, request):
        given_data = request.POST.copy()
        recettes_serializer = PrestationsVentsRecettesIntSerializer(data=given_data)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"

        if recettes_serializer.is_valid():
            recettes_serializer.save()
            line = recettes_serializer.data
            list = ['groupe_name', 'amount']

            context = {'base_template': base_template, 'line': line,
                       'list': list}

            return render(request,
                'dashboard/tableau_generique_ligne_read.html',
                      context=context)
        context = {'base_template': base_template,'message': f"Saisie incorrecte"}

        return render(request,
        'dashboard/tableau_generique_ligne_read.html',context=context)



    def update(self, request, pk=None):
        queryset = PrestationsVentsRecettesInt.objects.all()
        recette = get_object_or_404(queryset, pk=pk)
        given_data = request.POST.copy()
        serializer = PrestationsVentsRecettesIntSerializer(recette, data=given_data, partial=True)

        list = ['groupe_name', 'amount']

        if serializer.is_valid():
            serializer.save()

            line = serializer.data

            base_template = "dashboard/partial.html" if request.htmx else\
                "dashboard/base.html"
            context = { 'base_template': base_template, 'line': line,
                        'list':list}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)


    def destroy(self, request, pk):
        destroy_refactor(pk, PrestationsVentsRecettesInt)

        base_template = "dashboard/partial.html" if request.htmx else\
            "dashboard/base.html"
        context = { 'base_template': base_template}

        return render(request,
            'dashboard/tableau_generique_ligne_read.html',
                      context=context)

# Refactory the Viesets method
class CombinedView(APIView):
    pass
    # def get(self, request,*args,**kwargs):
    #     # Instantiate the viewsets
    #     caring_viewset = PrevisionBudgetCaringViewset()
    #     int_serv_viewset = RealCostCaringInternServiceViewSet()
    #
    #     context = {'caring_viewset': caring_viewset,
    #                 'int_serv_viewset':int_serv_viewset}
    #     # Render the template with the combined data
    #     return render(request, 'general.html',context=context)



# class viewset for organigramme
class OrganizationalChartViewSet(viewsets.ViewSet):

    # method for listing organigramme
    def list(self, request):
        data1 = {}
        # creating colones
        col_org = [
            {'nom': '', 'list': True},
            {'nom': 'presta interne', 'input': True},
            {'nom': 'garant du cadre', 'input': True},
            {'nom': 'référent budgt / subvention', 'input': True},
            {'nom': 'référent tâche planning', 'input': True},
            {'nom': '', 'input': False},
            {'nom':'', 'input': False}
        ]
        # Creer la liste avec les données de l'organigrame
        organigramme_list = [[{'pk':x.pk},{'user_name':x.user.name}, {'intern_services': x.intern_services}, {'settlement_agent': x.settlement_agent}, {'budget_referee': x.budget_referee}, {'task_planning_referee': x.task_planning_referee}] for x in OrganizationalChart.objects.all()]

        data1['organigramme'] = create_dict_with_data('organigramme_new', col_org, organigramme_list, False, True,new_line_name='organigramme_new')
        # adding the url that will be used to add, create or edit OragnizationalChart objects
        data1['organigramme']['crud_url'] = '/suivi_budg/organizationalchart/'

        base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
        context = {
            'base_template': base_template,
            'data1': data1,
        }

        return render(request, 'dashboard/pages_html/organigramme.html', context=context)


    # method for creating organigramme
    def create(self, request):
        "Controleur pour POST"
        # Reciving data from new line and creating a new personne on organigramme
        serializer = OrganizationalChartValidator(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return redirect('/suivi_budg/organizationalchart/')


    # Delete organizationalchart object
    def destroy(self, request, pk=None):
        "Controleur pour DELETE"
        if request.method == 'DELETE':# and request.POST.get('_method') == 'DELETE':
            #calling the destroy refactor method to delete selected object
            destroy_refactor(pk, OrganizationalChart)

            return redirect('/suivi_budg/organizationalchart/')

        # return redirect('/suivi_budg/organizationalchart/')


def tableau_de_bord_perso(request):
    context = {
        'name': request.user.email if request.user.is_authenticated else 'Anonymous',
    }
    return render(request, 'tableau_de_bord_perso.html', context=context)



def send_subventions(request):
    data1 = {}
    # Cherchons les données de la table subvention (Grant)
    subventions = Grant.objects.all()
    # Creat list of subventions for données de base
    subvention_donne_de_base_list = [[x.label, x.referee, x.partnaire, x.notification_date, x.reference] for x in subventions]
    # create the columns
    col_sub_base = [{'nom':''}, {'nom':'Référent'}, {'nom':'Partenaire'}, {'nom':'service'}, {'nom':'référence'}]
    # creating the dictionary with the data
    data1['subvention_donne_de_base'] = create_dict_with_data('donnees_de_base',col_sub_base,subvention_donne_de_base_list, True, False)

    # Subvention history part
    # Create history list
    subvention_historique_list = [[x.request_date, x.acceptation_date, x.notification_date, x.reference] for x in subventions]
    # column of history list
    col_history = [{'nom':''}, {'nom':'Demandée le'}, {'nom':'Acceptée le'}, {'nom':'Notifié le'}, {'nom':'référence'}]
    subvention_historique = create_dict_with_data('historique', col_history,subvention_historique_list,True, False)

    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data
    }
    return render(request, 'dashboard/pages_html/subventions.html', context=context)



def organigramme(request):
    dataO = {}
    # creating colones
    col_org = [
        {'nom':'', 'list': True},
                    {'nom':'presta interne', 'input': True},
                    {'nom':'garant du cadre', 'input': True},
                    {'nom':'référent budgt / subvention', 'input': True},
                    {'nom':'référent tâche planning', 'input': True}
    ]
    # Creer la liste avec les données de l'organigrame
    organigramme_list = [[x.user.name, x.intern_services, x.settlement_agent, x.budget_referee, x.task_planning_referee] for x in OrganizationalChart.objects.all()]
    dataO['organigramme'] = create_dict_with_data('organigramme_new', col_org, organigramme_list, False, True,new_line_name='organigramme_new')

    #Reciving data from new line and creating a new personne on organigramme
    if request.method == 'POST':

        # serch the validated data from serializer for the new line
        new_organigramme_validator = OrganizationalChartValidator(data=request.POST)

        if not new_organigramme_validator.is_valid():
            base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
            return render(request, 'dashboard/pages_html/organigramme.html', {'message_org_new': "Le nom choisit il existe déjà dans l'organigramme", 'base_template': base_template})

        validated_data_org = new_organigramme_validator.validated_data

        user_pk = validated_data_org.get('users').pk
        user = CustomUser.objects.get(pk=user_pk)
        # Attention if you do validated_data_org['intern_services'] it will search
        # a key that doesn't exist and will return error in case the checkbox isn't
        # 'on' if you do var_validated.get('name') it will search vor the name and
        # won't return an error.
        def refacto_check_var(var):
            return True if validated_data_org.get(var) == 'check' else False

        intern_services= refacto_check_var('intern_services')
        settlement_agent= refacto_check_var('settlement_agent')
        budget_referee= refacto_check_var('budget_referee')
        task_planning_referee = refacto_check_var('task_planning_referee')

        user_choice = CustomUser.objects.get(username=user)

        OrganizationalChart.objects.create(user=user_choice,
                                           intern_services=intern_services,
                                           settlement_agent=settlement_agent,
                                           budget_referee=budget_referee,
                                           task_planning_referee=task_planning_referee
                                           )
        return redirect('organigramme')


    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,
        'data': data,
        'dataO': dataO,
    }

    return render(request, 'dashboard/pages_html/organigramme.html', context=context)


'''
Sending data to the forms of nwe line in Prevision Cost tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''
# ------------ Start -------------------- #
# send data to Caring (bienveillance) form
def caring_data_form(request):
    cost_type = Cost.objects.get(type='CAR')
    tab_name = "prev_cost_tabCAR"
    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})


# send data to intern prevision cost form
def intern_serv_prev_form(request):
    cost_type = Cost.objects.get(type='IN_S')
    tab_name = "prev_cost_tabIN_S"

    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})


# send data to extern prevision cost form
def ext_serv_prev_form(request):
    cost_type = Cost.objects.get(type='EX_S')
    tab_name = "prev_cost_tabEX_S"

    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})

# send data to intern spendings cost form
def intern_spend_prev_form(request):
    cost_type = Cost.objects.get(type='SP_I')
    tab_name = "prev_cost_tabSP_I"

    return render(request, 'new_lines/new_budget_cost_prev.html',
                  {'cost_type': cost_type,'tab_name': tab_name})


#---------------- FIN FORM NEW LINE PREV COST --------


'''
Sending data to the forms of nwe line in Real Cost tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''
# ------------ Start -------------------- #

# send data to Caring (bienveillance) real form
def real_caring_form(request):
    cost_type = Cost.objects.get(type='CAR')
    users = CustomUser.objects.all()
    us = users.last()
    tab_name = "real_cost_tabCAR"

    return render(request, 'new_lines/new_budget_cost_real.html',
                  {'cost_type': cost_type,
                        'tab_name': tab_name,
                        'users': users, 'us':us})


# send data to intern service real form
def real_in_s_form(request):
    cost_type = Cost.objects.get(type='IN_S')
    tab_name = "real_cost_tabIN_S"
    users = CustomUser.objects.all()

    return render(request, 'new_lines/new_budget_cost_real.html',
                  {'cost_type': cost_type,
                   'tab_name': tab_name,
                   'users': users})

# send data to real purchase form
def real_purchase_form(request):
    cost_type = Cost.objects.get(type='EX_S')
    tab_name = "real_cost_tabEX_S"
    # in the purchase case we send the contact and not the user
    contacts = ContactProvisional.objects.all()

    return render(request, 'new_lines/new_purchcase.html',
    {'cost_type': cost_type, 'tab_name': tab_name, 'contacts': contacts})


# send data to real intern spending form
def intern_spending_form(request):
    cost_type = Cost.objects.get(type='SP_I')
    tab_name = "real_cost_tabSP_I"
    # in the purchase case we send the contact and not the user
    poles = Pole.objects.all()

    return render(request, 'new_lines/new_intern_spend.html',
    {'cost_type': cost_type, 'tab_name': tab_name, 'poles': poles})


#---------------- FIN FORM NEW LINE PREV REAL COST --------

'''
Sending data to the forms of nwe line in Recettes real and prev tables
We'll send all to one template but with different url and the variable
will be called the same with different values depended on the cases
'''

# ------------ Start ----------------- #

# ___ Previstion
# form for Prestation prevision
def recette_prev_presta_form(request):
    recette = Recette.objects.get(type='P') # SUB   v   R_IN
    groupes = Groupe.objects.all()
    prev_ou_reel = 'P'
    tab_name = "recette_tabPP"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_prev_ventes_form(request):
    recette = Recette.objects.get(type='V')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'P'
    tab_name = "recette_tabPV"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
             'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_internes_form(request):
    recette = Recette.objects.get(type='R_IN')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'P'
    tab_name = "recette_tabPR_IN"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })


# ___ Real
# form for Prestation prevision
def recette_real_presta_form(request):
    recette = Recette.objects.get(type='P')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'R'
    tab_name = "recette_tabRP"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_real_ventes_form(request):
    recette = Recette.objects.get(type='V')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'R'
    tab_name = "recette_tabRV"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
             'tab_name': tab_name, 'groupes': groupes })


# form for Vents prevision
def recette_internes_form_real(request):
    recette = Recette.objects.get(type='R_IN')
    groupes = Groupe.objects.all()
    prev_ou_reel = 'R'
    tab_name = "recette_tabRR_IN"

    return render(request, 'new_lines/new_recette.html',
    {'recette': recette, 'prev_ou_reel': prev_ou_reel,
        'tab_name': tab_name, 'groupes': groupes })

#---------------- FIN FORM NEW LINE RECETTES --------





# send user to organigrame creating new line
def send_user_to_organigrame(request):
    all_users = CustomUser.objects.all()

    return render(request, 'htmx/new_organigramme.html', {'user':all_users})


################################

# methode generique qui va envoyer tous les données
def suivi_budgetaire(request):

    base_template = "dashboard/partial.html" if request.htmx else "dashboard/base.html"
    context = {
        'base_template': base_template,

    }
    return render(request, 'dashboard/pages_html/suivi_budgetaire.html', context=context)

#################################


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
