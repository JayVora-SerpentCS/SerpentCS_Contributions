# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Till Today Serpent Consulting Services PVT LTD 
#    (<http://www.serpentcs.com>)
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


class mail_followers(models.Model):

    _inherit = 'mail.followers'

    @api.one
    @api.depends('res_model','res_id')
    def _related_document_name(self):
        self.related_document_name = self.env[self.res_model].browse(self.res_id).display_name

    related_document_name = fields.Char(string='Related Document Name',
        compute='_related_document_name', 
        help="Related Document Name.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
