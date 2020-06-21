# See LICENSE file for full copyright and licensing details.

import xlwt
from io import BytesIO
import base64
from xlrd import open_workbook
import tempfile

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import misc
from datetime import datetime


class WizDownloadTemplate(models.TransientModel):
    _name = 'wiz.download.template'
    _rec_name = 'ir_model'
    _description = 'Wiz Download Template'

    @api.depends('ir_model', 'ir_model.field_id', 'ir_model.field_id.model_id')
    def _compute_get_names(self):
        self.field_names_computed = self.ir_model.field_id.filtered(
            lambda l: l.model_id.id == self.ir_model.id)

    type = fields.Selection(
        [('export', 'Export'), ('import', 'Import')], string="Type")
    ir_model = fields.Many2one(
        'ir.model', string="Select Type Of Document To Download")
    upload_file = fields.Binary(string="Upload File")
    fname = fields.Char('File Name')
    create_m2o = fields.Boolean(string="Create Many2one")
    create_m2m = fields.Boolean(string="Create Many2many")
    update_only = fields.Boolean(string="Update records", default=True)
    create_only = fields.Boolean(string="Create records", default=True)
    field_names_computed = fields.Many2many(
        'ir.model.fields', compute='_compute_get_names')
    fields_list_ids = fields.Many2many(
        'ir.model.fields', domain="[('model_id', '=', ir_model)]")

    @api.onchange('type')
    def _get_active_model(self):
        if self._context and self._context.get('active_model'):
            model = self._context.get('active_model')
            ir_model = self.env['ir.model'].search([('model', '=', model)])
            self.ir_model = ir_model.id
            return {'domain': {'ir_model': [('id', '=', ir_model.id)]}}

    @api.onchange('ir_model')
    def _onchange_blank(self):
        self.button_uncheck()

    @api.multi
    def button_required(self):
        manual_selected = []
        if self.fields_list_ids:
            manual_selected.extend(self.fields_list_ids.ids)

        required = []
        required.extend(self.field_names_computed.filtered(
            lambda l: l.required).ids)

        self.fields_list_ids = manual_selected + required
        ctx = dict(self._context)
        ctx.update(({'nodestroy': False}))
        return {
            'context': ctx,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wiz.download.template',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def button_select_all(self):
        self.fields_list_ids = [(6, 0, self.field_names_computed.filtered(
            lambda l: l.name != 'id').ids)]
        ctx = dict(self._context)
        ctx.update(({'nodestroy': False}))
        return {
            'context': ctx,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wiz.download.template',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def button_uncheck(self):
        self.fields_list_ids = [(5, self.field_names_computed.ids)]
        ctx = dict(self._context)
        ctx.update(({'nodestroy': False}))
        return {
            'context': ctx,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wiz.download.template',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def download_template(self, row_values=None, error_reason=None,
                          error_value=None):
        """This method is used for export template."""
        fl = BytesIO()
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(self.ir_model.name)
        bold = xlwt.easyxf('font: bold 1;')
        main_header = xlwt.easyxf(
            'font: bold 1, height 270;'
            ' align: horiz center,vert center ,wrap 1;'
            'borders :top hair, bottom hair,left hair, right hair,'
            ' bottom_color black,top_color black')
        label_header = xlwt.easyxf(
            'font: bold 1, height 230;'
            ' align: horiz center,vert center ,wrap 1;'
            'borders :top hair, bottom hair,left hair, right hair,'
            ' bottom_color black,top_color black')

        if self.ir_model:
            col = 1
            count = -1
            row_12 = 12
            row_13 = 13
            row_14 = 14
            row_15 = 15
            row_16 = 16
            row_17 = 17

            worksheet.row(0).height = 500
            worksheet.col(0).width = 6200
            worksheet.col(1).width = 9500
            worksheet.col(2).width = 9500
            worksheet.col(3).width = 9500
            worksheet.col(4).width = 9500
            worksheet.write_merge(
                0, 0, 0, 4, 'Data Import Template', main_header)
            worksheet.write_merge(1, 1, 0, 4, '')
            worksheet.write_merge(2, 2, 0, 4, '')
            worksheet.write_merge(3, 3, 0, 2, 'Notes:', bold)
            worksheet.write_merge(
                4, 4, 0, 2, 'Please do not change the template headings.')
            worksheet.write_merge(
                5, 5, 0, 2, 'First data column must be blank.')
            worksheet.write_merge(
                6, 6, 0, 2, 'If you are uploading new records, "Naming Series"'
                ' becomes mandatory, if present.')
            worksheet.write_merge(
                7, 7, 0, 2, 'Only mandatory fields are necessary for new'
                ' records. You can keep non-mandatory columns blank if you'
                ' wish.')
            worksheet.write_merge(
                8, 8, 0, 2, 'For updating, you can update only selective'
                ' columns.')
            worksheet.write_merge(
                9, 9, 0, 2, 'You can only upload upto 5000 records in one go.'
                ' (may be less in some cases)')

            worksheet.write_merge(3, 3, 3, 4, 'Data Import Notes:', bold)
            worksheet.write_merge(4, 4, 3, 4, '')
            worksheet.write_merge(
                5, 5, 3, 4, 'Many2one: You can enter "NAME" of the relational'
                ' model!')
            worksheet.write_merge(
                6, 6, 3, 4, 'Many2many: You can enter "NAME" of the relational'
                ' model Seprate by ";"')
            worksheet.write_merge(
                7, 7, 3, 4, 'One2many: Let this blank! & Download Blank'
                ' Template for displayed comodel to Import!')
            worksheet.write_merge(8, 8, 3, 4, '')
            worksheet.write_merge(9, 9, 3, 4, '')
            worksheet.write_merge(10, 10, 3, 4, '')

            worksheet.write(row_12, 0, 'DocType:', bold)
            worksheet.write(row_12, 1, self.ir_model.name)
            worksheet.write(row_13, 0, 'Column Name:', bold)
            worksheet.write(row_14, 0, 'Type:', bold)
            worksheet.write(row_15, 0, 'Mandatory:', bold)
            worksheet.write(row_16, 0, 'Column Labels:', bold)
            worksheet.write(row_17, 0, 'Start entering data this line', bold)

            if not self.fields_list_ids and not error_value:
                raise UserError(
                    _("Fields should not be blank!"))

            if self.fields_list_ids:
                for line in self.fields_list_ids:
                    count += 1
                    worksheet.col(count + 1).width = 9900
                    worksheet.write(row_13, col, line.name)
                    worksheet.write(row_14, col, line.ttype + ' ' +
                                    'Relation: ' + str(line.relation) + '')
                    # Check for delegated field!
                    delegated = False
                    data = 'No'
                    if line.ttype == 'many2one' and line.relation in [
                        x.model for x in self.ir_model.inherited_model_ids
                    ] and not line.related or line.ttype == 'one2many':
                        delegated = True
                    # Check for all fields and its required attribute!
                    if line.required and not delegated:
                        data = 'Yes'
                    worksheet.write(row_15, col, str(data))
                    worksheet.write(
                        row_16, col, line.field_description, label_header)
                    col += 1

            elif row_values and error_value:
                for line in row_values:
                    count += 1
                    worksheet.col(count + 1).width = 9900
                    if count == 13:
                        i = line.index("Column Name:")
                        del line[i]
                        for data in line:
                            worksheet.write(row_13, col, data)
                            col += 1
                        col = 1
                    elif count == 14:
                        i = line.index("Type:")
                        del line[i]
                        for data in line:
                            worksheet.write(row_14, col, data)
                            col += 1
                        col = 1

                    elif count == 15:
                        i = line.index("Mandatory:")
                        del line[i]
                        for data in line:
                            worksheet.write(row_15, col, str(data))
                            col += 1
                        col = 1

                    elif count == 16:
                        i = line.index("Column Labels:")
                        del line[i]
                        for data in line:
                            worksheet.write(row_16, col, data, label_header)
                            col += 1
                        worksheet.write(
                            row_16, col, "REASONS: (NOT CREATED RECORD)",
                            label_header)
                        col += 1
                        col = 1

                    elif count == 17:
                        for each_error in error_value:
                            del each_error[0]
                            reason = set(each_error) & set(error_reason)
                            for value in each_error:
                                worksheet.write(row_17, col, str(value))
                                col += 1
                            worksheet.write(row_17, col, (str(
                                reason) + ': Value not found in Database!'
                                ' Please create it'
                                ' first. once create'
                                ' value in database.'
                                ' remove (REASON)'
                                ' column for IMPORT!'
                            ))
                            col += 1
                            row_17 += 1
                            col = 1

        workbook.save(fl)
        fl.seek(0)
        buf = base64.encodestring(fl.read())
        ctx = dict(self._context)
        vals = {'file': buf}
        ctx.update(vals)
        self.env.args = self._cr, self._uid, misc.frozendict(ctx)
        file_id = self.env['wiz.template.file'].create({
            'file': buf,
            'name': self.ir_model.name + '.xls'
        })

        return {
            'res_id': file_id.id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wiz.template.file',
            'context': ctx,
            'target': 'new'
        }

    @api.multi
    def import_data(self):
        """This method is used for import data."""
        for rec in self:
            datafile = rec.upload_file
            file_name = str(rec.fname)

            # Checking for Suitable File
            if not datafile or not file_name.lower().endswith(('.xls')):
                raise UserError(
                    _("""Please select an (Downloded Blank Template)
                     .xls compatible file to Import"""))
            xls_data = base64.decodestring(datafile)
            temp_path = tempfile.gettempdir()

            # writing a file to temp. location
            fp = open(temp_path + '/xsl_file.xls', 'wb+')
            fp.write(xls_data)
            fp.close()

            # opening a file form temp. location
            wb = open_workbook(temp_path + '/xsl_file.xls')

            header_list = []
            data_list = []

            field_type_dict = {}
            headers_dict = {}
            flag_dict = {}

            row_values = []
            for sheet in wb.sheets():
                for rownum in range(sheet.nrows):
                    row_values.append(sheet.row_values(rownum))
                    # headers
                    if rownum == 13:
                        # converting unicode chars into string
                        header_key = [x.strip().encode().decode('utf-8')
                                      for x in sheet.row_values(rownum)]

                    elif rownum == 14:
                        # converting unicode chars into string
                        field_type_list = [x.strip().encode().decode(
                            'utf-8').split(" Relation: "
                                           ) for x in sheet.row_values(rownum)]
                        list1 = []
                        list2 = []
                        for x in field_type_list:
                            list1.append(x[0])
                            if len(x) == 1:
                                list2.append(field_type_list.index(x))
                            else:
                                list2.append(x[1])
                        field_type_dict = dict(
                            zip(header_key, zip(list1, list2)))

                    elif rownum == 15:
                        # converting unicode chars into string
                        flag_list = [x.strip().encode().decode('utf-8')
                                     for x in sheet.row_values(rownum)]
                        list1 = []
                        for x in flag_list:
                            list1.append(x)
                        if header_key and list1:
                            flag_dict = dict(zip(header_key, list1))

                    elif rownum == 16:
                        # converting unicode chars into string
                        header_list = [x.strip().encode().decode('utf-8')
                                       for x in sheet.row_values(rownum)]
                        model_name = self.ir_model.name
                        name_file = ''.join(map(str, file_name.split('.xls')))
                        if model_name != name_file:
                            raise UserError(
                                _("""Selected document type not matched
                                    with browsed file name!"""))

                        index = []
                        for x in header_list:
                            index.append(header_list.index(x))
                        if header_key and index:
                            headers_dict = dict(zip(header_key, index))

                    # rows data
                    elif rownum >= 17:
                        data_list.append(sheet.row_values(rownum))

            # Data List
            if data_list and headers_dict:
                error_reason = []
                error_value = []
                for row in data_list:
                    vals = {}
                    for key in header_key:
                        if row[headers_dict[str(key)]]:
                            vals.update(
                                {str(key): row[headers_dict[str(key)]]})
                            if field_type_dict.get(str(key))[0] == 'date':
                                try:
                                    date = datetime.strptime(
                                        row[headers_dict[str(key)]],
                                        '%Y/%m/%d')
                                    vals.update({str(key): date})
                                except:
                                    raise UserError(
                                        _("""The Date format should
                                            be: YY/mm/dd << %s >>""") % (
                                            row[headers_dict[str(key)]]))

                            elif field_type_dict.get(str(key)
                                                     )[0] == 'datetime':
                                try:
                                    date = datetime.strptime(
                                        row[headers_dict[str(key)]],
                                        '%Y/%m/%d %H:%M:%S')
                                    vals.update({str(key): date})
                                except:
                                    raise UserError(
                                        _("""The DateTime format should
                                            be: YY/mm/dd HH:MM:SS  << %s >> """
                                          ) % (
                                            row[headers_dict[str(key)]]))

                            elif field_type_dict.get(str(key)
                                                     )[0] == 'many2one':
                                search_id = self.env["" + str(
                                    field_type_dict.get(str(key))[1]
                                ) + ""].search(
                                    [('name', '=',
                                        row[headers_dict[str(key)]])],
                                    limit=1).id

                                self.create_m2o = True
                                if not search_id and self.create_m2o:
                                    ir_model_search = self.env['ir.model'].\
                                        search([('model', '=', str(
                                            field_type_dict.get(str(key))[1])
                                        )])
                                    required_field = [
                                        x.id for x in
                                        ir_model_search.field_id.filtered(
                                            lambda l: l.required)]
                                    count = self.env['ir.model.fields'].\
                                        search_count([('id', 'in',
                                                       required_field)])
                                    if (count > 1):
                                        error_reason.append(
                                            row[headers_dict[str(key)]])
                                        error_value.append(row)
                                        vals.clear()
                                        break

                                    create_id = self.env["" + str(
                                        field_type_dict.get(str(key))[1]) + ""
                                    ].create({'name': row[headers_dict[str(key
                                                                           )]]}
                                             )
                                    vals.update(
                                        {str(key): create_id and create_id.id})
                                    search_id = create_id.id
                                vals.update({str(key): search_id})

                            elif field_type_dict.get(str(key)
                                                     )[0] == 'many2many':
                                ids = []
                                for line in row[
                                        headers_dict[str(key)]].split(';'):
                                    search_id = self.env[
                                        "" + str(field_type_dict.get(
                                            str(key))[1]) + ""].search(
                                        [('name', '=', line)])
                                    self.create_m2m = True
                                    if not search_id and self.create_m2m:
                                        ir_model_search\
                                            = self.env['ir.model'].search(
                                                [('model', '=',
                                                    str(field_type_dict.get(
                                                        str(key))[1]))])
                                        required_field = [
                                            x.id for x in ir_model_search.
                                            field_id.filtered(
                                                lambda l: l.required)]
                                        count = self.env['ir.model.fields'].\
                                            search_count([('id', 'in',
                                                           required_field)])
                                        if (count > 1):
                                            error_reason.append(
                                                row[headers_dict[str(key)]])
                                            error_value.append(row)
                                            vals.clear()
                                            break

                                        create_id = self.env[
                                            "" + str(field_type_dict.get(
                                                str(key))[1]) + ""].create(
                                            {'name': line})
                                        ids.append(create_id and create_id.id)
                                        vals.update({str(key): [(6, 0, ids)]})
                                        search_id = create_id.id
                                    ids.append(search_id and search_id.id)
                                    vals.update({str(key): [(6, 0, ids)]})

                            elif field_type_dict.get(str(key)
                                                     )[0] == 'one2many':
                                vals.update({str(key): False})
                        else:
                            if flag_dict.get(str(key)) == 'Yes' and \
                                    field_type_dict.get(str(key)
                                                        )[0] != 'one2many':
                                raise UserError(
                                    _('This field is required! << %s >>'
                                      ) % (str(key)))
                            vals.update({str(key): False})
                        vals.pop('Column Name:', None)

                    model_env = self.env["" + str(self.ir_model.model) + ""]
                    if vals != {}:
                        record_search_id = model_env.search(
                            [('name', '=', str(vals.get('name')))])
                        if record_search_id and self.update_only:
                            record_search_id.write(vals)
                        elif not record_search_id and self.create_only:
                            model_env.create(vals)

                if error_reason and error_value and row_values:
                    return self.download_template(row_values, error_reason,
                                                  error_value)
        return {'context': {'close_previous_dialog': True}}


class WizTemplateFile(models.TransientModel):
    _name = 'wiz.template.file'
    _description = 'Wiz Template File'

    @api.model
    def default_get(self, fields):
        if self._context is None:
            self._context = {}
        ctx = self._context
        res = super(WizTemplateFile, self).default_get(fields)
        if self._context.get('file'):
            res.update({'file': ctx['file']})
        return res

    file = fields.Binary('File')
    name = fields.Char(string='File Name', size=32)
