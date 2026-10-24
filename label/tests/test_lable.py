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
            domain=[("ttype", "not in", ["one2many", "reference", "function"])],
            limit=1,
        )

        self.barcode_field = self.fields.with_context(
            model_list=str(["res.users", "res.partner"])
        ).name_search(
            name="barcode",
            domain=[("ttype", "not in", ["one2many", "reference", "function"])],
            limit=1,
        )

        self.name_field = self.fields.with_context(
            model_list=str(["res.users", "res.partner"])
        ).name_search(
            name="name",
            domain=[("ttype", "not in", ["one2many", "reference", "function"])],
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
        self.assertTrue(self.label_print_id.ref_ir_act_report)
        self.label_print_id.unlink_action()
        self.assertFalse(self.label_print_id.ref_ir_act_report)

    def test_binary_image_field_renders_as_image(self):
        model = (
            self.env["ir.model"].sudo().search([("model", "=", "res.partner")], limit=1)
        )
        image_field = (
            self.env["ir.model.fields"]
            .sudo()
            .search(
                [
                    ("model_id", "=", model.id),
                    ("name", "=", "image_1920"),
                ],
                limit=1,
            )
        )
        self.assertTrue(image_field, "res.partner.image_1920 must be available")
        barcode_field = (
            self.env["ir.model.fields"]
            .sudo()
            .search(
                [
                    ("model_id", "=", model.id),
                    ("name", "=", "barcode"),
                ],
                limit=1,
            )
        )
        self.assertTrue(barcode_field, "res.partner.barcode must be available")

        image = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/"
            "x8AAwMCAO+/fjoAAAAASUVORK5CYII="
        )
        partner = self.env["res.partner"].create(
            {
                "name": "Label image test",
                "image_1920": image,
                "barcode": "LABEL-123",
            }
        )
        label_print = self.env["label.print"].create(
            {
                "name": "Image label test",
                "model_id": model.id,
                "field_ids": [
                    (
                        0,
                        0,
                        {
                            "sequence": 1,
                            "field_id": image_field.id,
                            # A binary image must still render even when the
                            # configuration row is left at its Normal default.
                            "type": "normal",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "sequence": 2,
                            "field_id": barcode_field.id,
                            "type": "normal",
                        },
                    ),
                ],
            }
        )

        rendered = (
            self.env["report.label.report_label"]
            .with_context(label_print=label_print.id)
            .get_data(1, 1, [partner.id], "res.partner", 1)
        )

        values = rendered[0][0]
        self.assertEqual([value["type"] for value in values], ["image", "barcode"])
        self.assertTrue(values[0]["value"].startswith("iVBOR"))
        self.assertTrue(values[0]["mimetype"].startswith("image/"))
        self.assertIn("float:right", values[0]["style"])
        self.assertEqual(values[1]["value"], "LABEL-123")
        self.assertTrue(values[1]["barcode_image"].startswith("PD94bWwg"))
        self.assertEqual(values[1]["barcode_mimetype"], "image/svg+xml")
        self.assertIn("float:left", values[1]["style"])

        wizard_defaults = (
            self.env["label.print.wizard"]
            .with_context(label_print=label_print.id)
            .default_get(["is_image", "is_barcode"])
        )
        self.assertTrue(wizard_defaults["is_image"])
        self.assertTrue(wizard_defaults["is_barcode"])

        report_data = {
            "form": {
                "rows": 1,
                "columns": 1,
                "ids": partner.ids,
                "model": "res.partner",
                "number_of_copy": 1,
                "height": "20mm",
                "width": "30mm",
                "top_margin": "0mm",
                "bottom_margin": "0mm",
                "left_margin": "0mm",
                "right_margin": "0mm",
                "cell_spacing": "1px",
                "image_width": "10",
                "image_height": "10",
                "barcode_width": 100,
                "barcode_height": 40,
            }
        }
        html, output_type = (
            self.env["ir.actions.report"]
            .with_context(
                active_model="res.partner",
                active_ids=partner.ids,
                label_print=label_print.id,
            )
            ._render_qweb_html("label.report_label", partner.ids, report_data)
        )
        html = html.decode() if isinstance(html, bytes) else html
        self.assertEqual(output_type, "html")
        self.assertIn("data:image/", html)
        self.assertIn("data:image/svg+xml;base64,", html)
        self.assertIn("LABEL-123", html)
        self.assertNotIn("BinaryValueAttachment", html)
