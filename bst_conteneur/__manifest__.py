{
    "name": "Sale Order Container",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Add container information to sales quotations and orders",
    "description": """
        Sale Order Container
        ====================

        Adds container information to sales quotations and orders.

        Features:
        - Container field on sale orders
        - Container changes tracked in the chatter
        - Dedicated container model
        - Dedicated wizard to manage the container
        - Container displayed in list and kanban views
        - Container searchable and groupable
        - Container displayed on quotation PDF
    """,
    "author": "ATLAS SERVICES",
    "license": "LGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_order_container_wizard_views.xml",
        "views/container_views.xml",
        "views/sale_order_views.xml",
        "report/sale_order_report_inherit.xml",
    ],
    "installable": True,
    "application": False,
}