from odoo import api, fields, models


class SaleOrderContainerWizard(models.TransientModel):
    _name = "sale.order.container.wizard"
    _description = "Renseigner le conteneur du devis"

    sale_order_id = fields.Many2one(
        "sale.order", string="Devis", required=True, readonly=True,
    )
    container = fields.Char(string="Conteneur")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order_id = self.env.context.get("active_id")
        if order_id:
            order = self.env["sale.order"].browse(order_id)
            res["sale_order_id"] = order.id
            res["container"] = order.container
        return res

    def action_validate(self):
        self.ensure_one()
        self.sale_order_id.write({"container": self.container})
        return {"type": "ir.actions.act_window_close"}

    def action_cancel(self):
        return {"type": "ir.actions.act_window_close"}