# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class LabelTestCase(common.TransactionCase):

    def setUp(self):
        super().setUp()

    def test_label_print_action(self):
        self.model_field = self.env["ir.model.fields"]
        self.model = self.env["ir.model"].sudo().search([("model", "=", "res.users")])
        self.fields = self.model_field.sudo().search([("model_id", "=", self.model.id)])

        self.image_field = self.fields.with_context(
            model_list=str(["res.users", "res.partner"])
        ).name_search(
            name="image",
            args=[
                [
                    "ttype",
                    "not in",
                    ["one2many", "refenrence", "function"],
                ]
            ],
            limit=1,
        )

        self.barcode_field = self.fields.with_context(
            model_list=str(["res.users", "res.partner"])
        ).name_search(
            name="barcode",
            args=[
                [
                    "ttype",
                    "not in",
                    ["one2many", "refenrence", "function"],
                ]
            ],
            limit=1,
        )

        self.name_field = self.fields.with_context(
            model_list=str(["res.users", "res.partner"])
        ).name_search(
            name="name",
            args=[
                [
                    "ttype",
                    "not in",
                    ["one2many", "refenrence", "function"],
                ]
            ],
            limit=1,
        )

        self.label_print = self.env["label.print"]
        self.label_print_id = self.label_print.sudo().create(
            {
                "name": "Lable Print Test",
                "model_id": self.model.id,
                "field_ids": [
                    (
                        0,
                        0,
                        {
                            "sequence": 1,
                            "type": "normal",
                            "field_id": self.name_field[0][0],
                            "fontsize": 8.0,
                            "position": "top",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "sequence": 2,
                            "type": "barcode",
                            "field_id": self.barcode_field[0][0],
                            "fontsize": 10.0,
                            "position": "right",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "sequence": 3,
                            "type": "image",
                            "field_id": self.image_field[0][0],
                            "fontsize": 12.0,
                            "position": "left",
                        },
                    ),
                ],
            }
        )

        self.label_print_id.onchange_model()
        self.label_print_id.create_action()
        self.label_print_id.unlink_action()