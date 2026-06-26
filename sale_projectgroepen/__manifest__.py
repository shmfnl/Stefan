{
    "name": "Verkoop Projectgroepen",
    "version": "18.0.1.4.0",
    "summary": "Beperk verkoopproducten per prijslijst, projectgroep en expliciete uitzonderingen",
    "description": """
Verkoop Projectgroepen
======================

Beheer welke producten gekozen mogen worden op offertes en verkooporders op basis van de gekozen prijslijst.

Functies
--------
* Projectgroepen op producten
* Toegestane projectgroepen op prijslijsten
* Verboden producten op prijslijsten
* Uitgesloten prijslijsten op producten
* Automatisch verwijderen of blokkeren van niet-toegestane orderregels
* Ondersteuning voor optionele producten
* Opschonen van lege secties en notities
    """,
    "category": "Sales/Sales",
    "author": "Stefan Heinen | Isolatie.com",
    "support": "stefanovich85@outlook.com",
    "license": "OPL-1",
    "price": 99.00,
    "currency": "EUR",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_group_views.xml",
        "views/product_template_views.xml",
        "views/product_pricelist_views.xml",
        "views/sale_order_views.xml"
    ],
    "images": ["static/description/banner.png"],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
    "auto_install": False
}
