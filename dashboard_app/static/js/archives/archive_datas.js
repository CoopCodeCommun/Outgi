let groupe_analytique = [];

// Fonction pour récupérer les données
function fetchAnalyticGroup() {
    return fetch('/api/account_analytic_group/')
        .then(response => response.json())
        .then(data => {groupe_analytique = data;           
        });
};


const appData = {
    //les différent pôles dans le menu supérieur
    menuOptions: ['vélo', 'Groupe Culture', 'Micro recyclerie', 'champignonnière'],
    annees: ['2022', '2023', '2024', '2025'],
    
    
    // les différents menu dans la barre latéral

    sidebarOptions: [
        {icon: 'bi bi-bar-chart-line', text: 'Tableau de bord'
        },       
        { icon: 'bi bi-currency-euro', text: 'Suivi budgétaire1', submenu: [
            { icon: 'bi bi-currency-euro', text: 'Tableaux budgétaires', link: '/suivi_budgetaire/'},
            { icon: 'bi bi-person-video2', text: 'Organigramme', link: '/organigramme/'},
            { icon: 'bi bi-cash-coin', text: 'Suivi subventions', link: '/subventions/' },
            { icon: 'bi bi-piggy-bank', text: 'Plan de trésorerie' },]
        },
        { icon: 'bi bi-file-music', text: 'Suivi de projet', submenu: [
            { icon: 'bi bi-person-video2', text: 'Objectifs indicateurs', link: '/objectifs_indicateurs/'  },
            { icon: 'bi bi-file-music', text: 'Postulations'},
            { icon: 'bi bi-file-music', text: 'Tâches'},
            { icon: 'bi bi-file-music', text: 'Suivi évenements'},
            { icon: 'bi bi-piggy-bank', text: 'Plan de trésorerie' },
            { icon: 'bi bi-file-music', text: 'Cadre de vie'},]
        },
        { icon: 'bi bi-people', text: 'Raffineur.euses', submenu: [
            { icon: 'bi bi-people', text: 'Répertoire', link: '/repertoire/'},
            { icon: 'bi bi-list-ol', text: 'Suivi volontariat'},            
            { icon: 'bi bi-list-ol', text: 'Badges' },
            { icon: 'bi bi-list-ol', text: 'Le calculateur de bien-être' },
            { icon: 'bi bi-currency-euro', text: 'tableau de bord perso', link: '/tableau_de_bord_perso/' },]
        },        
        { icon: 'bi bi-book', text: 'Boîte à outils', submenu: [
            { icon: 'bi bi-book', text: 'Documentation' },
            { icon: 'bi bi-file-music', text: 'outils numériques'},]
        }
        
    ]

};

////////////////////// données des tableaux //////////////////////////

// total = true : ajoute "Total" en pied de tableau
// newline = true : ajouter un "ajouter" ligne en bas de tableau

// pour les colonnes
// pas de critères particulier, les cellules sont grisées et non modifiables
//input: true, les cellules sont modifiable
//shouldTotal: false si Total=True, le total ne se fait pas sur cette colonne
//dropdown: true,  options: ['Option 1', 'Option 2', 'Option 3'], les cellule sont à choix multiple

let tableaux = {

    suivi_budgetaire: {
    
    //suivi budgétaire

        // recap membres du collectif
        tableau_membre_collectif: {
            titre: "",
            total: true,
            newline: true,
            rows: [{ name: 'Paul' },{ name: 'Jessica' }, { name: 'Bob' },{ name: 'Marcel' }],
            columns: [
                { name: 'à valider' },
                { name: 'à facturer' },
                { name: 'à payer' }
            ]
        },
    
        //données recap depenses
            tableau_recap_depenses : {
            titre : "Dépenses",
            total : true,
            newline : false,
            rows : [{ name:'bienveillance' },{ name: 'presta int.' },{ name: 'presta.ext / achats' },{ name: 'dépenses int.'}],
            columns : [
                { name: 'prév', },
                { name: 'dépensé', },
                { name: 'reste à dépensé',},
            ],
        },

        //données recap recettes
        tableau_recap_recettes : {
            titre : "Recettes",
            total: true,
            newline: false,
            rows: ['subventions / app', 'prestations', 'ventes', 'recette int'].map(name => ({ name })),
            columns: [
                { name: 'prév.',},
                { name: 'encaissé',},
                { name: 'reste à encaisser',},
            ],
        },

        //données prévisionnel bienveillance
        tableau_prev_bienveillance : {
            titre : "",
            total: true,
            newline: true,
            rows: [
                {name:'bienvei- llance', comment: 'bienveillance du pôle sur mars' },

            ],
            columns: [
            { name: 'Montant', input: true,},
            ],
        },

        // données réel bienveillance
        tableau_reel_bienveillance :{
            titre : "",
            total: true,
            newline: true,
            rows: [
                { name: 'kevin', },
                { name: 'kevin', },
                { name: 'Paul',commentaire: 'bienveillance du pôle sur mars' },
                { name: 'Paul',commentaire: 'bienveillance du pôle sur avril' },
                { name: 'Paul',commentaire: 'bienveillance du pôle sur avril' },
                { name: 'kevin',commentaire: 'bienveillance du pôle sur mars' },

                ],
            columns: [
                { name: 'date', input: true, shouldTotal: false  },
                { name: 'propo.', input: true, },
                { name: 'validé', input: true, },
                { name: 'factu.', input: true, },
                { name: 'payé', },
            ],
        },

        //données prévisionnel prestations internes
        tableau_prev_prestations_internes:{
            titre : "",
            total: true,
            newline: true,
            rows: ['bienveillance', 'animation ateliers', 'entretien matériel'].map(name => ({ name })),
            columns: [
            { name: 'Montant', input: true, },
            ], 
        },

        //données réel prestation interne
        tableau_reel_prestations_internes:{
            titre : "",
            total: true,
            newline: true,
            rows: ['Jessica', 'kevin'].map(name => ({ name })),
            columns: [
                { name: 'date', input: true, shouldTotal: false}, 
                { name: 'propo.', input: true, },
                { name: 'validé', input: true, },
                { name: 'factu.', input: true, },
                { name: 'payé', input: false, },
            ],
        },

        //données prévisionnel prestations externes
        tableau_prev_prestations_externes:{    
            titre : "",
            total: true,
            newline: true,
            rows: ['achat matériel','presta. externes'].map(name => ({ name })),
            columns: [
                { name: 'Montant', input: true, }, 
            ],
        },

        //données réel prestation externes
        tableau_reel_prestations_externes:{    
            titre : "",
            total: true,
            newline: false,
            rows: [ 'Ravate', 'run market', 'SARL Payet'].map(name => ({ name })),
            columns: [
                { name: 'intitulé', shouldTotal: false },
                { name: 'date', shouldTotal: false,},
                { name: 'validé',},
                { name: 'payé',},
            ],
        },

        //données prévisionnel dépenses interne
        tableau_prev_depenses_internes:{    
            titre: "",
            total: true,
            newline: true,
            rows: ['pôle culture','inter-formation', 'micro-recylerie'].map(name => ({ name })),
            columns: [
                { name: 'Montant', input: true, }, 
            ],
        },

        //données réel dépenses interne
        tableau_reel_depenses_internes:{    
            titre: "",
            total: true,
            newline: true,
            rows: [ 'Dépenses interne'].map(name => ({ name })),
            columns: [
                { name: 'pôle', dropdown: true,  options: ['Option 1', 'Option 2', 'Option 3'], shouldTotal: false, },
                { name: 'date', input: true, shouldTotal: false,},
                { name: 'montant', input: true,  },          
            ],
        },

        //données suivi recap dépenses
        tableau_suivi_recap_depenses:{    
            titre: "Recap",
            total: false,
            newline: false,
            rows: [ 'Recap'].map(name => ({ name })),
            columns: [
                { name: 'prévisionnel', },
                { name: 'réel', },
                { name: 'rest à dépenser', },          
            ],
        },

        //données prévisionnel subvention
        tableau_prev_subvention:{    
            titre: "",
            total: true,
            newline: true,
            rows: ['subventions'].map(name => ({ name })),
            columns: [
                { name: 'Montant', input: true, }, // La colonne par défaut est sans input
            ],
        },

        //données réel subvention
        tableau_reel_subvention:{    
            titre: "",
            total: true,
            newline: false,
            rows: [ 'Région', 'Mairie'].map(name => ({ name })),
            columns: [
                { name: 'Date',  shouldTotal: false},
                { name: 'Montant', },          
            ],
        },

        //données prévisionnel prestations
        tableau_prev_prestations:{    
            titre : "",
            total: true,
            newline: true,
            rows: ['divers prestations'].map(name => ({ name })),
            columns: [
                { name: 'Montant', input: true,  }, 
            ],
        },

        //données réel prestations
        tableau_reel_prestations:{
            titre : "",
            total: true,
            newline: false,
            rows: [ 'asso rvp', 'SARL dudu'].map(name => ({ name })),
            columns: [
                { name: 'Date', shouldTotal: false},
                { name: 'Montant', },          
            ],
        },


        //données prévisionnel ventes
        tableau_prev_ventes:{    
            titre: "",
            total: true,
            newline: true,
            rows: ['Ventes en direct'].map(name => ({ name })),
            columns: [
                    { name: 'Montant', input: true,}, 
            ],
        },

        //données réel ventes
        tableau_reel_ventes:{   
            titre: "",
            total: true,
            newline: false,
            rows: [ 'vente en direct', 'asso hoareau'].map(name => ({ name })),
            columns: [
                { name: 'Date', shouldTotal: false},
                { name: 'Montant', },          
            ],
        },


        //données prévisionnel recettes internes
        tableau_prev_recettes_internes:{    
            titre: "",
            total: true,
            newline: true,
            rows: ['divers pôles'].map(name => ({ name })),
            columns: [
                { name: 'Montant', input: true, }, // La colonne par défaut est sans input
            ],
        },

        //données réel dépenses internes
        tableau_reel_recettes_internes:{ 
            titre: "",
            total: true,
            newline: true,
            rows: ['micro'].map(name => ({ name })),
            columns: [
                { name: 'Montant', input: true, },
                { name: 'Montant', input: true, },
                { name: 'Montant', input: true, },
            ],
        },

    },

   
//////////////////////////// data subventions /////////////////////
 

    subventions: {
     
        //données de base subventions
        tableau_donnees_base_subventions : {
            titre: "",
            total: false,
            newline: true,
            rows: [{ name: 'Région - investissement' },{ name: 'mairie - fonctionnement' }],
            columns: [
                { name: 'Référent',input: true, shouldTotal: false},
                { name: 'Partenaire',input: true, shouldTotal: false},
                { name: 'service',input: true,},
                { name: 'référence',input: true,},
            
            ],
        },

        //données de base subventions
        tableau_historique_subventions : {
            titre: "",
            total: false,
            newline: false,
            rows: [{ name: 'Région - investissement' },{ name: 'mairie - fonctionnement' }],
            columns: [
                { name: 'Demandée le',input: true,   },
                { name: 'Acceptée le',input: true,   },
                { name: 'Notifiée le',input: true,   },
                { name: 'référence',input: true,   },
            ],
        },
    },


    //////////////////////////// data repertoire /////////////////////
 

    repertoire: {
     
        //repertoire
        tableau_repertoire : {
            titre: "",
            total: false,
            newline: false,
            rows: [{ name: 'Jessica'},{ name: 'Hugo'},{ name: 'Patricia'},{ name: 'George'},{ name: 'Paula'}],
            columns: [
                { name: 'telephone'},
                { name: 'mail'},
            ],
        },
    },

//////////////////////////// data organigramme /////////////////////
 

    organigramme: {
     
        //repertoire
        tableau_organigramme : {
            titre: "",
            total: false,
            newline: false,
            rows: [{ name: 'Jessica'},{ name: 'Hugo'},{ name: 'Patricia'},{ name: 'George'},{ name: 'Paula'}],
            columns: [
                { name: 'Code analytique'},
                { name: 'garant du cadre',input: true,},
                { name: 'référent budget / subventions',input: true,},
                { name: 'référent tâche / planning',input: true,},
            ],
        },
    },    

    objectifs_indicateurs: {
     
        //objectifs_indicateurs
        tableau_objectifs_indicateurs : {
            titre: "",
            total: false,
            newline: false,
            rows: [{ name: ''}],
            columns: [
                { name: 'Objectifs',input: true,},
                { name: 'Indicateurs',input: true,},
                { name: 'comment on mesure?',input: true,},
            ],
        },

        //indicateurs_valeurs
        tableau_indicateurs_valeurs : {
            titre: "",
            total: false,
            newline: false,
            rows: [{ name: ''}],
            columns: [
                { name: 'valeur initiale',input: true,},
                { name: 'valeur minimal',input: true,},
                { name: 'valeur satisfaisante',input: true,},
                { name: 'valeur max',input: true,},
            ],
        },




    }, 


    //////////////////////////// data tableau de bord perso /////////////////////


    tableau_de_bord_perso: {
    
        //recap membres du collectif
        tableau_membre_collectif1: {
            titre: "", 
            total: true, 
            newline: true, 
            rows: [{ name: 'Paul' },{ name: 'Jessica' }, { name: 'Bob' },{ name: 'Marcel' }],
            columns: [
                { name: 'à valider' },
                { name: 'à facturer' },
                { name: 'à payer' }
            ]
        },
    },

};