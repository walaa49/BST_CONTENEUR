from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderContainer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create({
            "name": "Test Customer",
        })

        cls.product = cls.env["product.product"].create({
            "name": "Test Product",
            "type": "consu",
        })

        cls.container = cls.env["sale.container"].create({
            "name": "CONT-0001",
        })

    def _create_sale_order(self, container=None):
        return self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "container_id": container.id if container else False,
            "order_line": [
                (0, 0, {
                    "product_id": self.product.id,
                    "product_uom_qty": 1,
                }),
            ],
        })

    def test_confirm_without_container_raises(self):
        """Confirming a sale order with no container must raise a UserError."""
        order = self._create_sale_order()

        with self.assertRaises(UserError):
            order.action_confirm()

        self.assertNotEqual(order.state, "sale")

    def test_confirm_with_container_succeeds(self):
        """Confirming a sale order with a container set must succeed."""
        order = self._create_sale_order(container=self.container)

        order.action_confirm()

        self.assertEqual(order.state, "sale")

    def test_confirm_multiple_orders_missing_container(self):
        """Confirming several orders where at least one is missing a
        container must raise, and none of them should be confirmed."""
        order_ok = self._create_sale_order(container=self.container)
        order_missing = self._create_sale_order()

        with self.assertRaises(UserError):
            (order_ok | order_missing).action_confirm()

        self.assertNotEqual(order_ok.state, "sale")
        self.assertNotEqual(order_missing.state, "sale")

    def test_container_field_default(self):
        """A freshly created sale order has no container by default."""
        order = self._create_sale_order()
        self.assertFalse(order.container_id)


@tagged("post_install", "-at_install")
class TestSaleOrderContainerWizard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create({
            "name": "Test Customer",
        })

        cls.product = cls.env["product.product"].create({
            "name": "Test Product",
            "type": "consu",
        })

        cls.container_a = cls.env["sale.container"].create({
            "name": "CONT-A",
        })

        cls.container_b = cls.env["sale.container"].create({
            "name": "CONT-B",
        })

        cls.order = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
            "order_line": [
                (0, 0, {
                    "product_id": cls.product.id,
                    "product_uom_qty": 1,
                }),
            ],
        })

    def test_wizard_default_get_prefills_order_and_container(self):
        """The wizard should prefill the order and its current container
        when opened from the sale order's active_id context."""
        self.order.container_id = self.container_a

        wizard = self.env["sale.order.container.wizard"].with_context(
            active_id=self.order.id
        ).create({})

        self.assertEqual(wizard.sale_order_id, self.order)
        self.assertEqual(wizard.container_id, self.container_a)

    def test_wizard_validate_writes_container_on_order(self):
        """Validating the wizard must write the selected container back
        onto the related sale order."""
        wizard = self.env["sale.order.container.wizard"].create({
            "sale_order_id": self.order.id,
            "container_id": self.container_b.id,
        })

        result = wizard.action_validate()

        self.assertEqual(self.order.container_id, self.container_b)
        self.assertEqual(result.get("type"), "ir.actions.act_window_close")

    def test_wizard_cancel_does_not_change_order(self):
        """Cancelling the wizard must leave the order's container untouched."""
        self.order.container_id = self.container_a

        wizard = self.env["sale.order.container.wizard"].create({
            "sale_order_id": self.order.id,
            "container_id": self.container_b.id,
        })

        result = wizard.action_cancel()

        self.assertEqual(self.order.container_id, self.container_a)
        self.assertEqual(result.get("type"), "ir.actions.act_window_close")