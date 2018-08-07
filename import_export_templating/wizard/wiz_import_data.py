# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from xlrd import open_workbook
import tempfile
import base64
import pytz

from odoo import api, models, _
from odoo.exceptions import UserError
from datetime import datetime

def _offset_format_timestamp1(src_tstamp_str, src_format, dst_format,
                              ignore_unparsable_time=True, context=None):
    if not src_tstamp_str:
        return False

    res = src_tstamp_str

    if src_format and dst_format:
        try:
            # dt_value needs to be a datetime.datetime object (
            #            so no time.struct_time or mx.DateTime.DateTime here!)
            dt_value = datetime.strptime(src_tstamp_str, src_format)
            if context.get('tz', False):
                try:
                    src_tz = pytz.timezone(context['tz'])
                    dst_tz = pytz.timezone('UTC')
                    src_dt = src_tz.localize(dt_value, is_dst=True)
                    dt_value = src_dt.astimezone(dst_tz)
                except Exception:
                    pass
            res = dt_value.strftime(dst_format)
        except Exception:
            # Normal ways to end up here are if strptime or strftime failed
            if not ignore_unparsable_time:
                return False
            pass
    return res


class WizReadSheetAndImport(models.TransientModel):

    _inherit = 'wiz.download.template'

    @api.multi
    def import_data(self):
        user = self.env.user
        context = dict(self.env.context)
        for rec in self:
            datafile = rec.upload_file
            file_name = str(rec.fname)

            # Checking for Suitable File
            if not datafile or not file_name.lower().endswith(('.xls')):
                raise UserError(
                    _("Please select an (Downloded Blank Template) .xls compatible file to Import"))
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
                            'utf-8').split(" Relation: ") for x in sheet.row_values(rownum)]
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
                                _("Selected document type not matched with browsed file name!"))

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
                            vals.update({str(key): row[headers_dict[str(key)]]})
                            if field_type_dict.get(str(key))[0] == 'date':
                                try:
                                    date = datetime.strptime(row[headers_dict[str(key)]], '%Y/%m/%d')
                                    vals.update({str(key): date})
                                except:
                                    raise UserError(
                                        _('The Date format should be: YY/mm/dd << %s >>') % (
                                            row[headers_dict[str(key)]]))

                            elif field_type_dict.get(str(key))[0] == 'datetime':
                                try:

                                    date = datetime.strptime(row[headers_dict[str(key)]], '%Y/%m/%d %H:%M:%S')
                                    context.update({'tz':user.tz})
                                    local_date = _offset_format_timestamp1(
                                        row[headers_dict[str(key)]],
                                        '%Y/%m/%d %H:%M:%S',
                                        '%Y/%m/%d %H:%M:%S',
                                        context=context,
                                    )
                                    vals.update({str(key): local_date})
                                except:
                                    raise UserError(
                                        _('The DateTime format should be: YY/mm/dd HH:MM:SS  << %s >> ') % (
                                            row[headers_dict[str(key)]]))

                            elif field_type_dict.get(str(key))[0] == 'many2one':
                                search_id = self.env["" + str(field_type_dict.get(str(key))[1]) + ""].search(
                                    [('name', '=', row[headers_dict[str(key)]])], limit=1).id

                                self.create_m2o = True
                                if not search_id and self.create_m2o:
                                    # model = str(field_type_dict.get(str(key))[1])
                                    # value = row[headers_dict[str(key)]]
                                    ir_model_search = self.env['ir.model'].search(
                                        [('model', '=', str(field_type_dict.get(str(key))[1]))])
                                    required_field = [x.id for x in ir_model_search.field_id.filtered(lambda l: l.required)]
                                    count = self.env['ir.model.fields'].search_count([('id', 'in', required_field)])
                                    if (count > 1):
                                        error_reason.append(row[headers_dict[str(key)]])
                                        error_value.append(row)
                                        vals.clear()
                                        break
                                        # return self.return_form_view_ref(model, ir_model_search, value)

                                    create_id = self.env["" + str(field_type_dict.get(str(key))[1]) + ""].create({
                                        'name': row[headers_dict[str(key)]]})
                                    vals.update({str(key): create_id and create_id.id})
                                    search_id = create_id.id
                                vals.update({str(key): search_id})

                            elif field_type_dict.get(str(key))[0] == 'many2many':
                                ids = []
                                for line in row[headers_dict[str(key)]].split(';'):
                                    search_id = self.env["" + str(field_type_dict.get(str(key))[1]) + ""].search([('name', '=', line)])
                                    self.create_m2m = True
                                    if not search_id and self.create_m2m:
                                        # model = str(field_type_dict.get(str(key))[1])
                                        # value = row[headers_dict[str(key)]]
                                        ir_model_search = self.env['ir.model'].search(
                                            [('model', '=', str(field_type_dict.get(str(key))[1]))])
                                        required_field = [x.id for x in ir_model_search.field_id.filtered(lambda l: l.required)]
                                        count = self.env['ir.model.fields'].search_count([('id', 'in', required_field)])
                                        if (count > 1):
                                            error_reason.append(row[headers_dict[str(key)]])
                                            error_value.append(row)
                                            vals.clear()
                                            break
                                            # return self.return_form_view_ref(model, ir_model_search, value)

                                        create_id = self.env["" + str(field_type_dict.get(str(key))[1]) + ""].create({'name': line})
                                        ids.append(create_id and create_id.id)
                                        vals.update({str(key): [(6, 0, ids)]})
                                        search_id = create_id.id
                                    ids.append(search_id and search_id.id)
                                    vals.update({str(key): [(6, 0, ids)]})

                            elif field_type_dict.get(str(key))[0] == 'one2many':
                                vals.update({str(key): False})
                        else:
                            if flag_dict.get(str(key)) == 'Yes' and field_type_dict.get(str(key))[0] != 'one2many':
                                raise UserError(_('This field is required! << %s >>') % (str(key)))
                            vals.update({str(key): False})
                        vals.pop('Column Name:', None)

                    model_env = self.env["" + str(self.ir_model.model) + ""]
                    if vals != {}:
                        record_search_id = model_env.search([('name', '=', str(vals.get('name')))])
                        if record_search_id and self.update_only:
                            record_search_id.write(vals)
                        elif not record_search_id and self.create_only:
                            model_env.create(vals)

                if error_reason and error_value and row_values:
                    return self.download_template(row_values, error_reason, error_value)

        return {'context': {'close_previous_dialog': True}}
