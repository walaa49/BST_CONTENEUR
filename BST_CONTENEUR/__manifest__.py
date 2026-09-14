{
    'name': 'Sale Order Container',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add container information to sales quotations and orders',
    'description': """
        Sale Order Container
        ====================
        Adds a container reference to sales quotations and orders.

        Features:
        - Container field on sale orders
        - Container changes tracked in the chatter
        - Container will be managed through a dedicated wizard
    """,
    'author': 'ATLAS SERVICES',
    'license': 'LGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_container_wizard_views.xml', 
        'views/sale_order_views.xml',
        'report/sale_order_report_inherit.xml',
    ],
    'installable': True,
    'application': False,
}