from odoo import fields, models


class SaleContainer(models.Model):
    _name = "sale.container"
    _description = "Conteneur"

    name = fields.Char(
        string="Référence",
        required=True,
    )