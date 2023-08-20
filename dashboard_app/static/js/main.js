// les différentes data
const appData = {
    //les différent pôles dans le menu supérieur
    menuOptions: ['vélo', 'Groupe Culture', 'Micro recyclerie', 'champignonnière'],
    // les différents menu dans la barre latéral
    sidebarOptions: [
        {icon: 'bi bi-bar-chart-line', text: 'Tableau de bord'},
        {icon: 'bi bi-currency-euro', text: 'Suivi budgétaire'},
        {icon: 'bi bi-piggy-bank', text: 'Plan de trésorerie'},
        {icon: 'bi bi-cash-coin', text: 'Suivi subventions'},
        {icon: 'bi bi-file-music', text: 'Suivi évenements'},
        {icon: 'bi bi-list-ol', text: 'Suivi volontariat'},
        {icon: 'bi bi-people', text: 'Répertoire Raffineur.euses'},
        {icon: 'bi bi-clipboard-data', text: 'Tableau de bord perso'},
        {icon: 'bi bi-book', text: 'Documentation'},
    ],

    //suivi budgétaire
    //données membre du collectif
    titre_membres: "",
    total_membres: false,
    rows_membres: [{name: 'Paul'}, {name: 'Jessica'}, {name: 'Bob'}, {name: 'Marcel'}],
    columns_membres: [
        {name: 'à valider', input: false, dropdown: false},
        {name: 'à facturer', input: false, dropdown: false},
        {name: 'à payer', input: false, dropdown: false},
    ],
    //données recap depenses
    titre_recap_depenses: "Dépenses",
    total_recap_depenses: true,
    rows_recap_depenses: [{name: 'bienveillance'}, {name: 'presta int.'}, {name: 'presta.ext / achats'}, {name: 'dépenses int.'}],
    columns_recap_depenses: [
        {name: 'prév', input: false, dropdown: false,},
        {name: 'dépensé', input: false, dropdown: false,},
        {name: 'reste à dépensé', input: false, dropdown: false,},
    ],

    //données recap recettes
    titre_recap_recettes: "Recettes",
    total_recap_recettes: true,
    rows_recap_recettes: ['suventions / app', 'prestations', 'ventes', 'recette int'].map(name => ({name})),
    columns_recap_recettes: [
        {name: 'prév.', input: false, dropdown: false,},
        {name: 'encaissé', input: false, dropdown: false,},
        {name: 'reste à encaisser', input: false, dropdown: false,},
    ],

    //données prévisionnel bienveillance
    titre_prev_bienveillance: "Prévisionnel",
    total_prev_bienveillance: true,
    rows_prev_bienveillance: ['bienvei- llance'].map(name => ({name})),
    columns_prev_bienveillance: [
        {name: 'Montant', input: true, dropdown: false,},
    ],

    //données réel bienveillance
    titre_reel_bienveillance: "Réel",
    total_reel_bienveillance: true,
    rows_reel_bienveillance: ['Paul', 'Jessica', 'kevin'].map(name => ({name})),
    columns_reel_bienveillance: [
        {name: 'date', input: true, dropdown: false,}, // La colonne par défaut est sans input
        {name: 'propo.', input: true, dropdown: false,},
        {name: 'validé', input: true, dropdown: false,},
        {name: 'factu.', input: true, dropdown: false,},
        {name: 'payé', input: false, dropdown: false,},
    ],

    //données prévisionnel prestations internes
    titre_prev_prestations_internes: "Prévisionnel",
    total_prev_prestations_internes: true,
    rows_prev_prestations_internes: ['bienveillance', 'animation ateliers', 'entretien matériel'].map(name => ({name})),
    columns_prev_prestations_internes: [
        {name: 'Montant', input: true, dropdown: false,}, // La colonne par défaut est sans input
    ],

    //données réel prestation interne
    titre_reel_prestations_internes: "Réel",
    total_reel_prestations_internes: true,
    rows_reel_prestations_internes: ['Jessica', 'kevin'].map(name => ({name})),
    columns_reel_prestations_internes: [
        {name: 'date', input: true, dropdown: false,},
        {name: 'propo.', input: true, dropdown: false,},
        {name: 'validé', input: true, dropdown: false,},
        {name: 'factu.', input: true, dropdown: false,},
        {name: 'payé', input: false, dropdown: false,},
    ],

    //données prévisionnel prestations externes
    titre_prev_prestations_externes: "Prévisionnel",
    total_prev_prestations_externes: true,
    rows_prev_prestations_externes: ['achat matériel', 'prestataires externes'].map(name => ({name})),
    columns_prev_prestations_externes: [
        {name: 'Montant', input: true, dropdown: false,},
    ],

    //données réel prestation externes
    titre_reel_prestations_externes: "Réel",
    total_reel_prestations_externes: true,
    rows_reel_prestations_externes: ['Ravate', 'run market', 'SARL Payet'].map(name => ({name})),
    columns_reel_prestations_externes: [
        {name: 'intitulé', input: false, dropdown: false,},
        {name: 'date', input: false, dropdown: false,},
        {name: 'validé', input: false, dropdown: false,},
        {name: 'payé', input: false, dropdown: false,},
    ],

    //données prévisionnel dépenses interne
    titre_prev_depenses_internes: "Prévisionnel",
    total_prev_depenses_internes: true,
    rows_prev_depenses_internes: ['pôle culture', 'inter-formation', 'micro-recylerie'].map(name => ({name})),
    columns_prev_depenses_internes: [
        {name: 'Montant', input: true, dropdown: false,},
    ],

    //données réel dépenses interne
    titre_reel_depenses_internes: "Réel",
    total_reel_depenses_internes: true,
    rows_reel_depenses_internes: ['Dépenses interne'].map(name => ({name})),
    columns_reel_depenses_internes: [
        {name: 'pôle', input: false, dropdown: true, options: ['Option 1', 'Option 2', 'Option 3']},
        {name: 'date', input: true, dropdown: false,},
        {name: 'montant', input: true, dropdown: false,},
    ],

    //données suivi recap dépenses
    titre_suivi_recap_depenses: "Recap",
    total_suivi_recap_depenses: false,
    rows_suivi_recap_depenses: ['Recap'].map(name => ({name})),
    columns_suivi_recap_depenses: [
        {name: 'prévisionnel', input: false, dropdown: false,},
        {name: 'réel', input: false, dropdown: false,},
        {name: 'rest à dépenser', input: false, dropdown: false,},
    ],

    //données prévisionnel subvention
    titre_prev_subvention: "Prévisionnel",
    total_prev_subvention: true,
    rows_prev_subvention: ['subventions'].map(name => ({name})),
    columns_prev_subvention: [
        {name: 'Montant', input: true, dropdown: false,}, // La colonne par défaut est sans input
    ],

    //données réel subvention
    titre_reel_subvention: "Réel",
    total_reel_subvention: true,
    rows_reel_subvention: ['Région', 'Mairie'].map(name => ({name})),
    columns_reel_subvention: [
        {name: 'Date', input: false, dropdown: false,},
        {name: 'Montant', input: false, dropdown: false,},
    ],

    //données prévisionnel prestations
    titre_prev_prestations: "Prévisionnel",
    total_prev_prestations: true,
    rows_prev_prestations: ['divers prestations'].map(name => ({name})),
    columns_prev_prestations: [
        {name: 'Montant', input: true, dropdown: false,}, // La colonne par défaut est sans input
    ],

    //données réel prestations
    titre_reel_prestations: "Réel",
    total_reel_prestations: true,
    rows_reel_prestations: ['asso rvp', 'SARL dudu'].map(name => ({name})),
    columns_reel_prestations: [
        {name: 'Date', input: false, dropdown: false,},
        {name: 'Montant', input: false, dropdown: false,},
    ],


    //données prévisionnel ventes
    titre_prev_ventes: "Prévisionnel",
    total_prev_ventes: true,
    rows_prev_ventes: ['Ventes en direct'].map(name => ({name})),
    columns_prev_ventes: [
        {name: 'Montant', input: true, dropdown: false,},
    ],

    //données réel ventes
    titre_reel_ventes: "Réel",
    total_reel_ventes: true,
    rows_reel_ventes: ['vente en direct', 'asso hoareau'].map(name => ({name})),
    columns_reel_ventes: [
        {name: 'Date', input: false, dropdown: false,},
        {name: 'Montant', input: false, dropdown: false,},
    ],


    //données prévisionnel recettes internes
    titre_prev_recettes_internes: "Prévisionnel",
    total_prev_recettes_internes: true,
    rows_prev_recettes_internes: ['divers pôles'].map(name => ({name})),
    columns_prev_recettes_internes: [
        {name: 'Montant', input: true, dropdown: false,}, // La colonne par défaut est sans input
    ],

    //données réel subvention
    titre_reel_recettes_internes: "Réel",
    total_reel_recettes_internes: true,
    rows_reel_recettes_internes: ['pôle jardin', 'bar'].map(name => ({name})),
    columns_reel_recettes_internes: [
        {name: 'Date', input: false, dropdown: false,},
        {name: 'Montant', input: false, dropdown: false,},
    ],

};

// menu
function showLoginForm() {
    document.getElementById('loginForm').style.display = 'block';
}

function hideLoginForm() {
    document.getElementById('loginForm').style.display = 'none';
}

function updateButtonText(element) {
    const buttonText = element.textContent || element.innerText;
    document.getElementById('dropdownMenuButton').textContent = buttonText;
}

// Générer les options du menu déroulant
const dropdownMenu = document.getElementById('dropdownMenuOptions');
appData.menuOptions.forEach(option => {
    const optionElement = document.createElement('a');
    optionElement.className = 'dropdown-item';
    optionElement.href = '#';
    optionElement.textContent = option;
    optionElement.onclick = function () {
        updateButtonText(option);
    };
    dropdownMenu.appendChild(optionElement);
});

function updateButtonText(text) {
    document.getElementById('dropdownMenuButton').textContent = text;
}

// Générer les éléments du menu latéral
const sidebarMenu = document.getElementById('sidebarMenu');

appData.sidebarOptions.forEach(menuItem => {
    const li = document.createElement('li');
    li.className = 'nav-item';

    const button = document.createElement('button');
    button.className = 'btn m-2 b-0';

    // Gestionnaire d'événement pour ajouter le style 'case_clair' lors du clic
    button.addEventListener('click', function () {
        // Retirer le style 'case_clair' de tous les autres boutons
        sidebarMenu.querySelectorAll('.btn').forEach(btn => {
            btn.classList.remove('case_clair');
        });

        // Ajouter le style 'case_clair' au bouton actuellement cliqué
        button.classList.add('case_clair');
    });

    const icon = document.createElement('i');
    icon.className = menuItem.icon;
    button.appendChild(icon);

    const textNode = document.createTextNode(` ${menuItem.text}`);
    button.appendChild(textNode);

    li.appendChild(button);
    sidebarMenu.appendChild(li);
});

//ouvrir/fermer une section
function toggleContent(element) {
    const contentDiv = element.nextElementSibling;
    const toggleSign = element.querySelector("#toggleSign");

    if (contentDiv.style.display === "none" || !contentDiv.style.display) {
        contentDiv.style.display = "block";
        toggleSign.textContent = "-";
    } else {
        contentDiv.style.display = "none";
        toggleSign.textContent = "+";
    }
}

//créer une section avec titre toggle
class CreateToggle extends HTMLElement {
    connectedCallback() {
        this.style.cursor = "pointer";
        this.addEventListener('click', this.toggleContent);

        let content = this.nextElementSibling;
        content.style.display = "block";  // Assurez-vous que le contenu est affiché par défaut

        const span = document.createElement("span");
        span.textContent = "-";  // Initialisez avec - puisque le contenu est visible
        this.appendChild(span);
        this.appendChild(document.createTextNode(` ${this.getAttribute('title')}`));
    }

    toggleContent = () => {
        let content = this.nextElementSibling;
        const span = this.querySelector("span"); // Assurez-vous de sélectionner le bon span

        if (content.style.display === "none") {
            content.style.display = "block";
            span.textContent = "-";
        } else {
            content.style.display = "none";
            span.textContent = "+";
        }
    }
}

customElements.define('create-toggle', CreateToggle);


// Creation tableau
function createTableComplete(titre, rows, columns, containerId, total) {
    const container = document.getElementById(containerId);


    const tableDiv = document.createElement('div');
    tableDiv.id = 'tableau_content';
    tableDiv.classList.add('case_clair', 'h-100');
    tableDiv.style.margin = '0px';


    // Créez un élément pour le titre à l'intérieur du conteneur du tableau
    const titleElement = document.createElement('div');
    titleElement.style.fontWeight = 'bold';
    titleElement.style.marginTop = '0px';         // Supprimez la marge du haut
    titleElement.style.padding = '5px 0px 0px 10px'; // Marge intérieure seulement sur les côtés et le bas
    titleElement.textContent = titre;
    tableDiv.appendChild(titleElement);

    const table = document.createElement('table');
    table.className = "table no-border table-spacing";


    // Ajout des en-têtes de colonnes
    const headerRow = document.createElement('tr');
    const firstHeader = document.createElement('th');  // Première cellule vide pour le nom des lignes
    headerRow.appendChild(firstHeader);

    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column.name;
        headerRow.appendChild(th);
    });

    table.appendChild(headerRow);

    // Ajout des noms des lignes et des cases
    rows.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = "case_petite";
        const th = document.createElement('th');
        th.className = "case_petite";
        th.textContent = row.name;
        tr.appendChild(th);

        columns.forEach(column => {
            const td = document.createElement('td');
            td.className = "case_petite";

            if (column.dropdown) {
                const select = document.createElement('select');
                select.className = "form-control case_clair case_petite";
                td.appendChild(select);
            } else if (column.input) {
                const input = document.createElement('input');
                input.type = 'text';
                input.className = "form-control case_clair case_petite";
                td.appendChild(input);
            } else {
                td.className += " case_fonce";
            }

            tr.appendChild(td);
        });

        table.appendChild(tr);
    });

    if (total) {
        const totalRow = document.createElement('tr');
        totalRow.className = "case_petite";
        const totalHeader = document.createElement('th');
        totalHeader.style.textAlign = 'right';
        totalHeader.textContent = 'Total';
        totalRow.appendChild(totalHeader);

        columns.forEach((column, colIndex) => {
            const td = document.createElement('td');
            td.className = "case_petite case_fonce";
            td.style.textAlign = 'center';
            td.style.verticalAlign = 'middle';

            let sum = 0;
            for (let i = 0; i < rows.length; i++) {
                const cell = table.rows[i + 1].cells[colIndex + 1];
                const inputElement = cell.querySelector('input');
                let cellValue;
                if (inputElement) {
                    cellValue = parseFloat(inputElement.value || 0);
                } else {
                    cellValue = parseFloat(cell.textContent || cell.innerText || 0);
                }

                if (!isNaN(cellValue)) {
                    sum += cellValue;
                }
            }
            td.textContent = sum.toFixed(0);
            totalRow.appendChild(td);
        });

        table.appendChild(totalRow);
    }

    tableDiv.appendChild(table);
    container.appendChild(tableDiv);
}


// Appel des focntions de tableaux
createTableComplete(appData.titre_membres, appData.rows_membres, appData.columns_membres, 'tableau_membre_collectif', appData.total_membres);
createTableComplete(appData.titre_recap_depenses, appData.rows_recap_depenses, appData.columns_recap_depenses, 'tableau_recap_depenses', appData.total_recap_depenses);
createTableComplete(appData.titre_recap_recettes, appData.rows_recap_recettes, appData.columns_recap_recettes, 'tableau_recap_recettes', appData.total_recap_recettes);

// suivi détaillé
createTableComplete(appData.titre_prev_bienveillance, appData.rows_prev_bienveillance, appData.columns_prev_bienveillance, 'tableau_prev_bienveillance', appData.total_prev_bienveillance);
createTableComplete(appData.titre_reel_bienveillance, appData.rows_reel_bienveillance, appData.columns_reel_bienveillance, 'tableau_reel_bienveillance', appData.total_reel_bienveillance);
createTableComplete(appData.titre_prev_prestations_internes, appData.rows_prev_prestations_internes, appData.columns_prev_prestations_internes, 'tableau_prev_prestations_internes', appData.total_prev_prestations_internes);
createTableComplete(appData.titre_reel_prestations_internes, appData.rows_reel_prestations_internes, appData.columns_reel_prestations_internes, 'tableau_reel_prestations_internes', appData.total_reel_prestations_internes);
createTableComplete(appData.titre_prev_prestations_externes, appData.rows_prev_prestations_externes, appData.columns_prev_prestations_externes, 'tableau_prev_prestations_externes', appData.total_prev_prestations_externes);
createTableComplete(appData.titre_reel_prestations_externes, appData.rows_reel_prestations_externes, appData.columns_reel_prestations_externes, 'tableau_reel_prestations_externes', appData.total_reel_prestations_externes);
createTableComplete(appData.titre_prev_depenses_internes, appData.rows_prev_depenses_internes, appData.columns_prev_depenses_internes, 'tableau_prev_depenses_internes', appData.total_prev_depenses_internes);
createTableComplete(appData.titre_reel_depenses_internes, appData.rows_reel_depenses_internes, appData.columns_reel_depenses_internes, 'tableau_reel_depenses_internes', appData.total_reel_depenses_internes);
createTableComplete(appData.titre_prev_subvention, appData.rows_prev_subvention, appData.columns_prev_subvention, 'tableau_prev_subvention', appData.total_prev_subvention);
createTableComplete(appData.titre_reel_subvention, appData.rows_reel_subvention, appData.columns_reel_subvention, 'tableau_reel_subvention', appData.total_reel_subvention);
createTableComplete(appData.titre_prev_prestations, appData.rows_prev_prestations, appData.columns_prev_prestations, 'tableau_prev_prestations', appData.total_prev_prestations);
createTableComplete(appData.titre_reel_prestations, appData.rows_reel_prestations, appData.columns_reel_prestations, 'tableau_reel_prestations', appData.total_reel_prestations);
createTableComplete(appData.titre_prev_ventes, appData.rows_prev_ventes, appData.columns_prev_ventes, 'tableau_prev_ventes', appData.total_prev_ventes);
createTableComplete(appData.titre_reel_ventes, appData.rows_reel_ventes, appData.columns_reel_ventes, 'tableau_reel_ventes', appData.total_reel_ventes);
createTableComplete(appData.titre_prev_recettes_internes, appData.rows_prev_recettes_internes, appData.columns_prev_recettes_internes, 'tableau_prev_recettes_internes', appData.total_prev_recettes_internes);
createTableComplete(appData.titre_reel_recettes_internes, appData.rows_reel_recettes_internes, appData.columns_reel_recettes_internes, 'tableau_reel_recettes_internes', appData.total_reel_recettes_internes);


//fonction ouvrir/fermer un tableau
function toggleSection(element) {
    const content = element.nextElementSibling;
    if (content.style.display === "none" || !content.style.display) {
        content.style.display = "block";
        element.querySelector(".toggleSign").textContent = "-";
    } else {
        content.style.display = "none";
        element.querySelector(".toggleSign").textContent = "+";
    }
}

// Exemple d'utilisation
const rows = [
    {
        name: 'Ligne 1',
        data: [
            {content: 'Data 1.1'},
            {dropdown: true, options: ['Option 1', 'Option 2']},
            {userInput: 'Data 1.3'}
        ]
    },
    // ... d'autres lignes
];

const columns = [
    {name: 'Colonne 1'},
    {name: 'Colonne 2'},
    {name: 'Colonne 3'}
];

createTable(rows, columns);


document.addEventListener("DOMContentLoaded", function () {
    // Vos appels à createTableComplete vont ici
});
