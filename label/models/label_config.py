# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class LabelMain(models.Model):
    _name = "label.brand"
    _rec_name = "brand_name"

    _description = "Configured Label Brands"

    brand_name = fields.Char("Name", size=64, index=True)
    label_config_ids = fields.One2many(
        "label.config", "label_main_id", "Label Config")
    

class LabelConfig(models.Model):
    _name = "label.config"

    _description = "Configuration for label"

    name = fields.Char("Name", size=64, required=True, index=True)
    height = fields.Float("Height (in mm)", required=True)
    width = fields.Float("Width (in mm)", required=True)
    top_margin = fields.Float("Top Margin (in mm)", default=0.0)
    bottom_margin = fields.Float("Bottom Margin  (in mm)", default=0.0)
    left_margin = fields.Float("Left Margin (in mm)", default=0.0)
    right_margin = fields.Float("Right Margin (in mm)", default=0.0)
    cell_spacing = fields.Float("Cell Spacing", default=1.0)
    label_main_id = fields.Many2one("label.brand", "Label")
 

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('height') == 0.0 or vals.get('width') == 0.0:
                raise ValidationError(_("Height/Width value must be non zero."))
        return super().create(vals_list)

    def write(self,vals):
        if vals.get('height') == 0.0 or vals.get('width') == 0.0:
            raise ValidationError(_("Height/Width value must be non zero."))
        return super().write(vals)
