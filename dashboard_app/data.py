# calling data from DB
from .models import Groupe, Pole, Cost, PrevisionCost

class data():
   
   #les paramètres sont de base en False, et mis en True si actifs
   #colonnes : 
        #input : modifiable
        #list : liste déroulante
        #checkbox : case à cocher
        #total : affiche le total de la colonne
   
   #total : fait le total en pied de page si "total" du tableau est en True

    membres_du_collectif = {
        "slug": "membres_du_collectif",
        "titre": "",
        "colonnes": [
            {'nom':'', 'list': True, }, # liste qui vient de l'organigramme
            {'nom':'A valider', 'total':True}, #total des colonnes A valider (bienveillance et presta interne) du suivi détaillé
            {'nom':'A facturer', 'total':True},  #total des colonnes A Facturer (bienveillance et presta interne) du suivi détaillé
            {'nom':'A Payer', 'total':True }, #total des colonnes A Payé (bienveillance et presta interne) du suivi détaillé
        ],
        "lignes": [
            ['Jacques', 30, 20, 20],
            ['Camille', 10, 20, 40],
            ['Jacqueline', 10, 20, 10],
        ],
        "total": True,
    }
    

    recap_depenses = {
        "slug": "recap_depenses",
        "titre": "Dépenses",
        "colonnes": [
            {'nom':''}, 
            {'nom':'prév'}, #somme du dépenses prévisionnel 
            {'nom':'dépensé'}, #somme des dépenses réel
            {'nom':'reste à dépenser'}, #somme des reste à dépenser
        ],
        "lignes": [
            ['bienveillance', 10, 20, 30],
            ['presta int.', 10, 20, 30],
            ['presta.ext / achats', 10, 20, 30],
            ['dépenses int.', 10, 20, 30],
        ],
        "total": True,
    }

    recap_recettes = {
        "slug": "recap_recettes",
        "titre": "Recettes",
        "colonnes": [
            {'nom':''}, 
            {'nom':'prév'},  #somme des recettes prévisionnel 
            {'nom':'encaissé'}, #somme des recettes encaissées
            {'nom':'reste à encaisser'}, #somme des recettes qui reste à encaisser
        ],
        "lignes": [
            ['animation ateliers', 10, 20, 30],
            ['entretien matérie', 10, 20, 30],
            ['ventes', 10, 20, 30],
            ['recette int', 10, 20, 30],
        ],
        "total": True,
    }
    
################## suivi budgétaire détaillé ################
    ####  dépenses ###
   # creating a list with Caring prevision cost data

    #import ipdb; ipdb.set_trace()
    bienveillance_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants
        ],

        "lignes": [

                    ['Garant du cadre', 100],
                    ['ref budget', 100],
                    ['ref communication', 100],
            ],

        "total": True,
    }

    bienveillance_reel = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':''}, #les bienveillants peuvent selectionné un nom si il créé une nouvelle ligne
            {'nom':'date', 'input': True, 'total': True}, #les bienveillants peuvent remplir une date
            {'nom':'propo.' , 'input': True, 'total': False}, #les bienveillants peuvent remplir un un montant
            {'nom':'validé', 'input': True}, #les bienveillants peuvent valider
            {'nom':'factu.', 'input': True}, #les bienveillants peuvent valider
            {'nom':'payé'}, #si la facture est "payé" dans odoo, la checkbox est True, il y aura un peu de réflexion à avoir pour voir comment associé une proposition à une facture odoo
        ],
        "lignes": [
            ['Rémy','02/03/23', 100, True, False, True],
            ['Georgette','02/03/23', 200, True, True, False],
            ['hugues','02/03/23', 300, False, False, False],
            ['yvette','02/03/23', 500, True, True, False],
        ],
        #"ajouter_ligne":True,
        "total": True,
    }

    presta_int_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants
        ],
        "lignes": [
            ['animation ateliers', 530],
            ['entretien matérie', 200],
        ],
        "total": True,
    }

    presta_int_reel = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'liste': True}, #liste déroulante des presta interne de l'organigramme
            {'nom':'date', 'input': True, 'total': False}, #les presta int concerné peuvent remplir un une date
            {'nom':'propo.', 'input': True}, #les presta int concerné peuvent remplir un un montant
            {'nom':'validé'}, #les bienveillants peuvent valider
            {'nom':'factu.'}, #les presta int concerné peuvent valider
            {'nom':'payé'}, #si la facture est "payé" dans odoo, la checkbox est True 
        ],
        "lignes": [
            ['Rémy', '02/04/2023', 100, False, False,True],
            ['Georgette', '02/04/2023', 100, True, False,False],
        ],
        "total": True,
    }

    presta_ext_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['matériel', 500],
            ['consomable', 400],
        ],
        "total": True,
    }

    presta_ext_reel = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':''},  #le nom des facture de tout les articles sauf co-rem et presta int
            {'nom':'intitulé'}, #l'intitulé des facture
            {'nom':'date', 'total': False}, #date des factures
            {'nom':'validé',},#si la facture est "validé" dans odoo, la checkbox est True, c'est une checkbox non modifiable par l'utilisateur
            {'nom':'payé',}, #si la facture est "payé" dans odoo, la checkbox est True, c'est une checkbox non modifiable par l'utilisateur
        ],
        "lignes": [
            ['Ravate','course', '03/05/23', True, False],
            ['decathlon','matériel ', '09/08/23', True, True],
        ],
        "total": True,
    }

    depenses_int_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
    }

    #le principe est que ce tableau est relié avec le tableau recette int des projets selectionné dans "nom"
    depenses_int_reel = { 
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'list': True}, #liste déroulante des projets
            {'nom':'date', 'date': True, 'total': False}, #date à rentrer par un bienveillant
            {'nom':'montant', 'input': True}, #montant à rentrer par un bienveillant
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
    }

    ####  recettes ###

    subvention_donne_de_base= {
        "slug": "donnees_de_base",
        "titre": "Données de base",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['Région - investissement', 10,20,3,30],
            ['mairie - fonctionnement', 22,33,44,55],
        ],
        "total": True,
    }

#ce tableau est relié à la page subventions
    subvention_historique = {
        "slug": "historique",
        "titre": "Historique",
        "colonnes": [
                    {'nom':''},
                    {'nom':'Demandée le'},
                    {'nom':'Acceptée le'},
                    {'nom':'Notifié le'},
                    {'nom':'référence'},
        ],
        "lignes": [
            ['Région - investissement', 9,8,7,6],
            ['mairie - fonctionnement', 11,12,13,14],
        ],
        "total": True,
    }

    presta_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True},  #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
             
        ],
        "lignes": [
            ['micro-recylerie','9800€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
    }

    presta_reel = { 
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': False}, #factures client avec l'article presta ext via odoo
            {'nom':'date', 'total': False}, # date des factures 
            {'nom':'montant'},# montant des factures
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
    }

    vente_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '2000€'],
            ['commun', '2000€'],
        ],
        "total": True,
    }

    vente_reel = { 
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'',}, #factures client avec l'article vente via odoo
            {'nom':'date', 'total': False},  #date des factures 
            {'nom':'montant',},  #montant des factures 
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
    }

    recettes_int_prev = {
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom':'', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des intulés 
            {'nom':'montant', 'input': True}, #les membres du collectif ayant le caractére bienveillant dans l'organigramme, peuvent ajouter des montants 
        ],
        "lignes": [
            ['micro-recylerie','1000€'],
            ['Culture', '666€'],
            ['commun', '2000€'],
        ],
        "total": True,
    }

#le principe est que ce tableau est relié avec le tableau dépense int des projets selectionné dans "nom"
    recettes_int_reel = { 
        "slug": "recap_recettes",
        "titre": "",
        "colonnes": [
            {'nom': '', 'list': False}, 
            {'nom': 'date', 'input': True, 'total': False},
            {'nom': 'montant', 'input': True},
        ],
        "lignes": [
            ['micro-recylerie', '03/05/23','1000€'],
            ['Culture', '03/05/23', '2000€'],
        ],
        "total": True,
    }

############ Organigramme #################


    organigramme = { 
        "slug": "organigramme",
        "titre": "",
        "colonnes": [
                    {'nom':'', 'list': True}, #liste déroulante des membres de odoo qui ont l'étiquette "Raffineur.euse"
                    {'nom':'presta interne', 'input': True}, #peut être coché par les admins 
                    {'nom':'garant du cadre', 'input': True}, #peut être coché par les admins
                    {'nom':'référent budgtet / subvention', 'input': True}, #peut être coché par les admins
                    {'nom':'référent tâche planning', 'input': True}, #peut être coché par les admins
        ],
        "lignes": [
            ['jessica', True, True, False, False ],
            ['Bob', True, False, True, False ],
            ['John', True, False, False, True ],
            ['Suzy', True, False, False, False ],
            ['John', True, False, False, False ],
        ],
        "total": False,
        "ajouter_ligne" : True,
    }


############ Subventions #################

    subventions = { 
        "slug": "subventions",
        "titre": "subventions",
        "colonnes": [
                    {'nom':'projet concerné', 'input': True}, #projet concerné par la subvention
                    {'nom':'intitulé', 'input': True}, #nom de la subvention, rempli par le référent
                    {'nom':'référent', 'input': True}, #corespond au référent inscrit dans l'organigramme
                    {'nom':'partenaire', 'input': True}, #rempli par l'admin
                    {'nom':'service', 'input': True}, #rempli par l'admin
                    {'nom':'montant', 'input': True}, #rempli par l'admin
        ],
        "lignes": [
            ['micro-forêt', 'economik', 'Marc', 'OFB', '', '22 500€'],
            ['édition', 'machine estampe', 'Julien', 'Dac réunion', 'Culture', '8000€'],
            ['Travailler autrement', 'contrat de revitalisation', 'Claire', 'Air France', '', '8000€'],
        ],
        "total": False,
        "ajouter_ligne" : False,
    }

    subvention_historique = {
        "slug": "historique",
        "titre": "Historique",
        "colonnes": [
                    {'nom':''},
                    {'nom':'Demandée le'},
                    {'nom':'Acceptée le'},
                    {'nom':'Notifié le'},
                    {'nom':'référence'},
        ],
        "lignes": [
            ['Région - investissement', 9,8,7,6],
            ['mairie - fonctionnement', 11,12,13,14],
        ],
        "total": False,
    }


membres_du_collectifcccccc = {
        "slug": "membres_du_collectif",
        "titre": "",
        "colonnes": [
            {'nom':'', 'list': True, }, # liste qui vient de l'organigramme
            {'nom':'A valider', 'total':True}, #total des colones A valider (bienveillance et presta interne) du suivi détaillé
            {'nom':'A facturer', 'total':True},  #total des colones A Facturer (bienveillance et presta interne) du suivi détaillé
            {'nom':'A Payer', 'total':True }, #total des colones A Payé (bienveillance et presta interne) du suivi détaillé
        ],
        "lignes": [
            ['Jacques', 10, 20, 20],
            ['Camille', 10, 20, 40],
            ['Jacqueline', 10, 20, 10],
        ],
        "total": True,
    }

       


