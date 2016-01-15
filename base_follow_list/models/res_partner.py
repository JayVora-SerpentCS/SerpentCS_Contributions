# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Till Today Serpent Consulting Services PVT LTD (<http://www.serpentcs.com>)
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
############################################################################

from openerp import models, fields, api


class res_partner(models.Model):

    _inherit = 'res.partner'

    @api.one
    def _count_following(self):
        self.following_counts = len(self.env['mail.followers'].search([('partner_id', '=', self.id)]))

    following_counts = fields.Integer(string='Follows',
        compute='_count_following', 
        help="List of Following Models.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
