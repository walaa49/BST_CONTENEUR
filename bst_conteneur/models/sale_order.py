from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    container_id = fields.Many2one(
        "sale.container",
        string="Conteneur",
        tracking=True,
        readonly=True,
        copy=False,
    )

    def action_confirm(self):
        missing = self.filtered(lambda order: not order.container_id)

        if missing:
            raise UserError(_(
                "Le conteneur doit être renseigné avant de confirmer ce devis.\n"
                "Utilisez le bouton « Renseigner le conteneur » dans l'en-tête du devis."
            ))

        return super().action_confirm()