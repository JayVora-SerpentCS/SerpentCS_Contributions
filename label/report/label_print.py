# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import pooler
from report.interface import report_rml
import tools


class label_form(report_rml):
    def create(self, cr, uid, ids, datas, context):
        rml = """<document filename="Label Print.pdf">
            <template pageSize="(210mm, 297mm)"  title="Label Print"
        author="Serpent Consulting Services (contact@serpentcs.com)" >
        <pageTemplate id="first">
        <frame id="first" x1="0" y1="0" width="210mm" height="297mm"/>
        </pageTemplate>
        </template>
        <stylesheet>
        <blockTableStyle id="Standard_Outline">
        <blockAlignment value="LEFT"/>
        <blockValign value="TOP"/>
        </blockTableStyle>
        <blockTableStyle id="Table1">
        <blockAlignment value="LEFT"/>
        <blockValign value="TOP"/>
        """

        height = datas.get('height')-1
        width = datas.get('width')
        cols = int(210/width)
        fontsize = datas.get('font_size')
        for i in range(cols):
            rml += '<lineStyle kind="LINEBEFORE" colorName="#000000" start="' + \
                   str(i)+',0" stop="'+str(i)+',-1"/>'
            rml += '<lineStyle kind="LINEAFTER" colorName="#000000" start="' + \
                   str(i)+',0" stop="'+str(i)+',-1"/>'
            rml += '<lineStyle kind="LINEABOVE" colorName="#000000" start="' + \
                   str(i)+',0" stop="'+str(i)+',0"/>'
            rml += '<lineStyle kind="LINEBELOW" colorName="#000000" start="' + \
                   str(i)+',-1" stop="'+str(i)+',-1"/>'
        rml += """</blockTableStyle>
                    <initialize>
                        <paraStyle name="needed" alignment="justify"/>
                    </initialize>"""
        rml + ='<paraStyle name="P1" fontName="Helvetica" fontSize="' + \
            str(fontsize)+'"/><images/>'
        rml += '</stylesheet><story>'
        tbl = ''


        tbl += '<blockTable colWidths="'
        tbl += str(width)+'mm'
        for i in range(cols-1):
            tbl += ','+str(width)+'mm'
        tbl += '" rowHeights="'+str(height)+'mm" style="Table1" >'
        rec_cnt = len(context.get('active_ids'))
        row = 0
        row = rec_cnt/cols
        if(rec_cnt % cols != 0):
            row += 1
        rec_id = 0
        model = context.get('active_model')
        f_names = datas.get('field_cols')
        f_cnt = len(f_names)
        for j in range(row):
            rml += tbl+'<tr>'
            for k in range(cols):
                rml += '<td>'
                if(rec_id < rec_cnt):
                    obj = pooler.get_pool(cr.dbname).get(model)
                    rec = obj.read(cr, uid, context.get('active_ids')[rec_id])
                    obj = pooler.get_pool(cr.dbname).get('ir.model.fields')
                    for l in range(f_cnt):
                        rml += '<para style="P1">'
                        f_info = obj.browse(cr, uid, f_names[l])
                        rml += f_info.field_description+' : '
                        temp = rec.get(f_info.name)
                        if f_info.ttype == 'many2one':
                            if temp is not False:
                                rml += tools.ustr(temp[1])
                        else:
                            rml += tools.ustr(temp)
                        rml += '</para>'
                rec_id += 1
                rml += '</td>'
            rml += '</tr></blockTable>'
        rml += '</story></document>'

        report_type = datas.get('report_type', 'pdf')
        create_doc = self.generators[report_type]
        pdf = create_doc(rml, title=self.title)
        return (pdf, report_type)

label_form('report.label.print', 'label.print', '', '')
