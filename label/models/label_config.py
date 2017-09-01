# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# 1:  imports of openerp
from openerp import models, fields, api


class label_main(models.Model):

    _name = 'label.brand'
    _rec_name = 'brand_name'

    brand_name = fields.Char("Name", size=64, select=1)
    label_config_ids = fields.One2many('label.config', 'label_main_id',
                                       'Label Config')


class label_config(models.Model):

    _name = 'label.config'

    name = fields.Char("Name", size=64, required=True, select=1)
    height = fields.Float("Height (in mm)", required=True)
    width = fields.Float("Width (in mm)", required=True)
    top_margin = fields.Float("Top Margin (in mm)", default=0.0)
    bottom_margin = fields.Float("Bottom Margin  (in mm)", default=0.0)
    left_margin = fields.Float("Left Margin (in mm)", default=0.0)
    right_margin = fields.Float("Right Margin (in mm)", default=0.0)
    cell_spacing = fields.Float("Cell Spacing", default=1.0)
    label_main_id = fields.Many2one('label.brand', 'Label')
