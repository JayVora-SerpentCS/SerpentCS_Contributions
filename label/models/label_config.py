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
    top_margin = fields.Float("Top Margin (in mm)")
    bottom_margin = fields.Float("Bottom Margin  (in mm)")
    left_margin = fields.Float("Left Margin (in mm)")
    right_margin = fields.Float("Right Margin (in mm)")
    cell_spacing = fields.Float("Cell Spacing", default=1.0)
    label_main_id = fields.Many2one("label.brand", "Label")
 

    @api.constrains('height', 'width')
    def _check_positive_label(self):
        """
        Constraint to ensure that the height and width of a label are positive values.
        
        Raises: ValidationError: If the height or width is less than 0.0.
        """
        for label in self:
            if label.height < 0.0 or label.width < 0.0:
                raise ValidationError(_("Height/Width value must be Positive."))
