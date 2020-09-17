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

from osv import osv,fields

class label_main(osv.osv):
    _name = 'label.brand'
    _rec_name = 'brand_name'
    _columns = {
        'brand_name' : fields.char("Name", size=64, select=1),
        'label_config_ids' : fields.one2many('label.config', 'label_main_id', 'Label Config'),
    }
label_main()

class label_config(osv.osv):
    
    _name = 'label.config'
    
    _columns = {
        'name' : fields.char("Name", size=64, required=True, select=1),
        'height' : fields.float("Height (in mm)", required=True),
        'width' : fields.float("Width (in mm)", required=True),
        'top_margin' : fields.float("Top Margin (in mm)"),
        'bottom_margin' : fields.float("Bottom Margin  (in mm)"),
        'left_margin' : fields.float("Left Margin (in mm)"),
        'right_margin' : fields.float("Right Margin (in mm)"),
        'cell_spacing' : fields.float("Cell Spacing"),
        'label_main_id' : fields.many2one('label.brand', 'Label'),
    }
    
    _defaults = {
        'top_margin' : 0.0,
        'bottom_margin' : 0.0,
        'left_margin' : 0.0,
        'right_margin' : 0.0,
        'cell_spacing' : 1.0
    }

label_config()
