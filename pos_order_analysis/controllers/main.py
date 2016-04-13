# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#    Copyright (C) 2011-today Serpent Consulting Services Pvt. Ltd. 
#                                               (<http://www.serpentcs.com>).
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
##############################################################################
import openerp
from openerp.tools.translate import _
from openerp import http, tools
from openerp.http import request
from openerp import SUPERUSER_ID

class Home(http.Controller):
        
    @http.route('/web/pos_order_date', type='json', auth="none")
    def graph_data(self, redirect=None, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        start_date = kw.get('start_date')
        end_date = kw.get('end_date')
        partner_id = kw.get('partner_id')
        product_id = kw.get('product_id')
        column_chart_dict = {}
        pie_chart_dict = {}
        combine_chart = []
        chart_category = []

        #Fetch pos order ids whose date_order between start_date and end_date
        if partner_id :
            cr.execute("""SELECT id from pos_order where date_order >= %s and date_order <= %s and state='paid' and partner_id =%s""",(start_date,end_date,partner_id));
        else :
            cr.execute("""SELECT id from pos_order where date_order >= %s and date_order <= %s and state='paid'""",(start_date,end_date));
        order_ids = cr.fetchall()
        pos_order_ids = [order_id[0] for order_id in order_ids]
        if product_id :
                product_query_op = ' in' if len(product_id) != 1 else  ' ='
                cr.execute("SELECT  DISTINCT(order_id) from pos_order_line where product_id "+ product_query_op + " %s",(tuple(product_id),))
                pos_order_datas = cr.fetchall()
                pos_order_data_ids = [elem[0] for elem in pos_order_datas]
                pos_order_ids = list(set(pos_order_data_ids).intersection(pos_order_ids))

        if pos_order_ids :

            #Pie chart Initialize
            pie_query_op = ' in' if len(pos_order_ids) != 1 else  ' ='
            if product_id :
                product_query_op = ' in' if len(product_id) != 1 else  ' ='
                cr.execute("SELECT  t.name_template,sum(qty) from pos_order_line as p left join product_product t  on (p.product_id = t.id) where product_id " + product_query_op +"%s and order_id" + pie_query_op + "%s  group by t.name_template",(tuple(product_id),tuple(pos_order_ids),))
            else :
                cr.execute("SELECT  t.name_template,sum(qty) from pos_order_line as p left join product_product t  on (p.product_id = t.id) where order_id" + pie_query_op + "%s  group by t.name_template",(tuple(pos_order_ids),))
            chart_categ_data = cr.fetchall()
            for elem in chart_categ_data :
                pie_chart_dict[elem[0]] = {'name': tools.ustr(elem[0]),'y':elem[1]}
                chart_category.append(tools.ustr(elem[0]))
            pie_chart = {'type': 'pie','name': 'Total consumption','data': pie_chart_dict.values(),'center': [100, 40],
                             'size': 200,'showInLegend': False,'dataLabels': {'enabled': False}}

            #Column chart Initialize
            pos_order_obj = pool['pos.order']
            for pos_order in pos_order_obj.browse(cr,SUPERUSER_ID,pos_order_ids,context=context):
                if product_id :
                    product_query_op = ' in' if len(product_id) != 1 else  ' ='
                    cr.execute("SELECT  t.name_template,sum(qty) from pos_order_line as p left join product_product t  on (p.product_id = t.id) where product_id" + product_query_op + "%s and order_id=%s group by t.name_template",(tuple(product_id),pos_order.id,))
                else :
                    cr.execute("""SELECT  t.name_template,sum(qty) from pos_order_line as p left join product_product t  on (p.product_id = t.id) where order_id=%s group by t.name_template""",(pos_order.id,))
                chart_details = cr.fetchall()
                chart_data = [['',0]] * len(chart_category)
                for elem in chart_details :
                    chart_data[chart_category.index(tools.ustr(elem[0]))] = list(elem)
                column_chart_dict[pos_order.id]={'id':pos_order.id,'type': 'column','name':tools.ustr(pos_order.name),'data':chart_data}

            #Combine column and pie chart
            combine_chart = column_chart_dict.values()
            combine_chart.append(pie_chart)
        return [combine_chart,chart_category]

