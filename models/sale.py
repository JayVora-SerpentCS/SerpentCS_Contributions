# -*- coding: utf-8 -*-
#
#
#    Author: Lorenzo Battistini
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (c) 2016 Serpent Consulting Services Pvt. Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import api, fields, models, _


class SaleOrderLineGroup(models.Model):
    _name = 'sale.order.line.group'

    name = fields.Char('Group', size=64, required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 index=True,
         default=lambda self:\
         self.env['res.company']._company_default_get('sale.order.line.group'))


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    picking_group_id = fields.Many2one(
            'sale.order.line.group', 'Picking Group')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    picking_group_id = fields.Many2one(
            'sale.order.line.group', 'Group',
            help="This is used by 'multi-picking' to group order lines in one "
                 "picking")


class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_group_id = fields.Many2one('sale.order.line.group',
                                       'Picking Group',
                        related='procurement_id.sale_line_id.picking_group_id')

    @api.cr_uid_ids_context
    def _picking_assign(self, cr, uid, move_ids, context=None):
        """Try to assign the moves to an existing picking
        that has not been reserved yet and has the same
        procurement group, locations and picking type
        (moves should already have them identical)
         Otherwise, create a new picking to assign them to.
        """

        move = self.browse(cr, uid, move_ids, context=context)[0]
        pick_obj = self.pool.get("stock.picking")
        picks = pick_obj.search(cr, uid, [
                ('group_id', '=', move.group_id.id),
                ('location_id', '=', move.location_id.id),
                ('location_dest_id', '=', move.location_dest_id.id),
                ('picking_type_id', '=', move.picking_type_id.id),
                ('printed', '=', False),
                ('state', 'in', ['draft', 'confirmed', 'waiting',
                                 'partially_available', 'assigned'])],
                                limit=1, context=context)
        if picks:
            pick = picks[0]
            picking_id = pick_obj.browse(cr, uid, pick, context=context)
            if move.picking_group_id.id == picking_id.picking_group_id.id:
                return self.write(cr, uid, move_ids, {'picking_id': pick},
                                  context=context)
            else:
                values = self._prepare_picking_assign(cr, uid, move,
                                                      context=context)
                values.update({'picking_group_id': move.picking_group_id.id})
                pick = pick_obj.create(cr, uid, values, context=context)
                return self.write(cr, uid, move_ids, {'picking_id': pick},
                                  context=context)
        else:
            values = self._prepare_picking_assign(cr, uid, move,
                                                  context=context)
            values.update({'picking_group_id': move.picking_group_id.id})
            pick = pick_obj.create(cr, uid, values, context=context)
            return self.write(cr, uid, move_ids, {'picking_id': pick},
                              context=context)
