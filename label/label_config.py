# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Serpent Consulting Services (<http://www.serpentcs.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp import models, fields, _


class label_main(models.Model):
    _name = 'label.brand'
    _rec_name = 'brand_name'

    brand_name = fields.Char(_("Name"), size=64, select=1)
    label_config_ids = fields.One2many(
        'label.config', 'label_main_id', _('Label Config'))


class label_config(models.Model):

    _name = 'label.config'

    name = fields.Char(_("Name"), size=64, required=True, select=1)
    height = fields.Float(_("Height (in mm)"), required=True)
    width = fields.Float(_("Width (in mm)"), required=True)
    top_margin = fields.Float(_("Top Margin (in mm)"), default=0.0)
    bottom_margin = fields.Float(_("Bottom Margin  (in mm)"), default=0.0)
    left_margin = fields.Float(_("Left Margin (in mm)"), default=0.0)
    right_margin = fields.Float(_("Right Margin (in mm)"), default=0.0)
    cell_spacing = fields.Float(_("Cell Spacing"), default=1.0)
    label_main_id = fields.Many2one('label.brand', _('Label'))
    padding_top = fields.Float(_("Padding Top (in mm)"), default=0.0)
    padding_bottom = fields.Float(_("Padding Bottom  (in mm)"), default=0.0)
    padding_left = fields.Float(_("Padding Left (in mm)"), default=0.0)
    padding_right = fields.Float(_("Padding Right (in mm)"), default=0.0)
