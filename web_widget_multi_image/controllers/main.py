# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#    Copyright (C) 2011-2015 Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>).
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

import openerp.http as http
from openerp.addons.web.controllers.main import Binary
import simplejson
import time
import os
import StringIO
import functools
import logging
from openerp.http import request, serialize_exception as _serialize_exception
import werkzeug.utils
import werkzeug.wrappers

_logger = logging.getLogger(__name__)


def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError
        (simplejson.dumps(error))
        (simplejson.dumps(error))
    return wrap


class Binary_multi(Binary):

    @http.route('/web/binary/removeimage', type='json', auth="user")
    def load(self, path):
        """ Remove Image from the server path.

        :param str path: path of image stored in server.
        """
        if path:
            addons_path = http.addons_manifest['web']['addons_path']
            file_path = addons_path + path
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                return
        return

    @http.route('/web/binary/upload_image_multi', type='http', auth="user")
    @serialize_exception
    def upload_image_multi(self, callback, ufile):
        # TODO: might be useful to have a configuration flag for
        # max-length file uploads
        # TODO: might be useful to have a configuration flag
        # for max-length file uploads
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        try:
            data = ufile.read()
            if data:
                current_date_time = time.strftime("%d%m%y%H%M%S")
                file_name = current_date_time + "_" + ufile.filename
                ap = http.addons_manifest['web']['addons_path']
                ap += "/web/static/src/img/image_multi/"
                if not os.path.isdir(ap):
                    os.mkdir(ap)
                ap += file_name
                buff = StringIO.StringIO()
                buff.write(data)
                buff.seek(0)
                file_name = "/web/static/src/img/image_multi/" + file_name
                file = open(ap, 'wb')
                file.write(buff.read())
                file.close()
                args = [len(data), file_name, ufile.content_type,
                        ufile.filename, time.strftime("%m/%d/%Y %H:%M:%S")]
            else:
                args = []
        except Exception, e:
            args = [False, e.message]
        return out % (simplejson.dumps(callback), simplejson.dumps(args))
