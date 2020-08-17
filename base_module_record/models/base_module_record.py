# See LICENSE file for full copyright and licensing details.

import string
from xml.dom import minidom
from odoo import api, models
from odoo.tools import ustr

DEFAULT_FIELDS = [
    "create_date",
    "create_uid",
    "display_name",
    "id",
    "__last_update",
    "write_date",
    "write_uid",
]


class XElement(minidom.Element):
    """dom.Element with compact print
    The Element in minidom has a problem: if printed, adds whitespace
    around the text nodes. The standard will not ignore that whitespace.
    This class simply prints the contained nodes in their compact form, w/o
    added spaces.
    """

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write(indent)
        minidom.Element.writexml(self, writer, indent="", addindent="",
                                 newl="")
        writer.write(newl)


def doc_createXElement(xdoc, tagName):
    e = XElement(tagName)
    e.ownerDocument = xdoc
    return e


class BaseModuleRecord(models.Model):
    _name = "ir.module.record"
    _description = "Module Record"

    def __init__(self, *args, **kwargs):
        self.recording = 0
        super(BaseModuleRecord, self).__init__(*args, **kwargs)

    # To Be Improved
    @api.model
    def _create_id(self, model, data):
        id_indx = 0
        while True:
            try:
                name = list(
                    filter(
                        lambda x: x in string.ascii_letters,
                        (data.get("name", "") or "").lower(),
                    )
                )
                name = "".join(name)
            except:
                name = ""
            val = model.replace(".", "_") + "_" + name + str(id_indx)
            if val not in self.blank_dict.values():
                break
            id_indx += 1
        return val

    @api.model
    def _get_id(self, model, id):
        if isinstance(id, tuple):
            id = id[0]
        if (model, id) in self.blank_dict:
            res_id = self.blank_dict[(model, id)]
            return res_id, False
        dt = self.env["ir.model.data"]
        obj = dt.search([("model", "=", model), ("res_id", "=", id)])
        if not obj:
            return False, None
        obj = obj[0]
        depends = self._context.get("depends", {})
        depends[obj.module] = True
        return obj.module + "." + obj.name, obj.noupdate

    @api.model
    def _create_record(self, doc, model, data, record_id, noupdate=False):
        data_pool = self.env["ir.model.data"]
        model_pool = self.env[model]
        record = doc.createElement("record")
        record.setAttribute("id", record_id)
        record.setAttribute("model", model)
        record_list = [record]
        lids = data_pool.search([("model", "=", model)])
        lids = lids[:1]
        res = lids.read(["module"])
        blank_dict = self.blank_dict
        depends = {}
        self = self.with_context({"depends": {}})
        # Add blank_dict to new self object
        self.blank_dict = blank_dict
        if res:
            depends[res[0]["module"]] = True
        fields = model_pool.fields_get()
        for key, val in data.items():
            # functional fields check
            if key in model_pool._fields.keys() and not model_pool._fields[key].store:
                continue
            if not (val or (fields[key]["type"] == "boolean")):
                continue
            if (
                fields[key]["type"] in ("integer", "float")
                or fields[key]["type"] == "selection"
                and isinstance(val, int)
            ):
                field = doc.createElement("field")
                field.setAttribute("name", key)
                field.setAttribute("eval", val and str(val) or "False")
                record.appendChild(field)
            elif fields[key]["type"] in ("boolean",):
                field = doc.createElement("field")
                field.setAttribute("name", key)
                field.setAttribute("eval", val and "1" or "0")
                record.appendChild(field)
            elif fields[key]["type"] in ("many2one",):
                field = doc.createElement("field")
                field.setAttribute("name", key)
                if type(val) in (type(""), type(u"")):
                    id = val
                else:
                    id, update = self._get_id(fields[key]["relation"], val)
                    noupdate = noupdate or update
                if not id:
                    relation_pool = self.env[fields[key]["relation"]]
                    field.setAttribute("model", fields[key]["relation"])
                    fld_nm = relation_pool._rec_name
                    val = relation_pool.browse(val)
                    name = val.read([fld_nm])[0][fld_nm] or False
                    field.setAttribute("search", str([(str(fld_nm), "=", name)]))
                else:
                    field.setAttribute("ref", id)
                record.appendChild(field)
            elif fields[key]["type"] in ("one2many",):
                for valitem in val or []:
                    if (
                        valitem[0] in (0, 1)
                        and valitem[2].get("name") not in DEFAULT_FIELDS
                    ):
                        if valitem[0] == 0:
                            newid = self._create_id(fields[key]["relation"], valitem[2])
                            valitem[1] = newid
                        else:
                            newid, update = self._get_id(
                                fields[key]["relation"], valitem[1]
                            )
                            if not newid:
                                newid = self._create_id(
                                    fields[key]["relation"], valitem[2]
                                )
                                valitem[1] = newid
                        self.blank_dict[(fields[key]["relation"], valitem[1])] = newid
                        childrecord, update = self._create_record(
                            doc, fields[key]["relation"], valitem[2], newid
                        )
                        noupdate = noupdate or update
                        record_list += childrecord
                    else:
                        pass
            elif fields[key]["type"] in ("many2many",):
                res = []
                for valitem in val or []:
                    if valitem[0] == 6:
                        for id2 in valitem[2]:
                            id, update = self._get_id(fields[key]["relation"], id2)
                            self.blank_dict[(fields[key]["relation"], id2)] = id
                            res.append(id)
                            noupdate = noupdate or update
                        field = doc.createElement("field")
                        field.setAttribute("name", key)
                        field.setAttribute(
                            "eval",
                            "[(6,0,["
                            + ",".join(map(lambda x: "ref('%s')" % (x,), res))
                            + "])]",
                        )
                        record.appendChild(field)
            else:
                field = doc_createXElement(doc, "field")
                field.setAttribute("name", key)
                field.appendChild(doc.createTextNode(ustr(val)))
                record.appendChild(field)
        return record_list, noupdate

    @api.model
    def get_copy_data(self, model, id, result):
        res = []
        obj = self.env[model]
        data = obj.browse([id][0]).read([])
        if isinstance(data, list):
            del data[0]["id"]
            data = data[0]
        else:
            del data["id"]
        mod_fields = obj.fields_get()
        for key in data.keys():
            if key in result:
                continue
            if mod_fields[key]["type"] == "many2one":
                if isinstance(data[key], bool):
                    result[key] = data[key]
                elif not data[key]:
                    result[key] = False
                else:
                    result[key] = data[key][0]

            elif mod_fields[key]["type"] in ("one2many",):
                rel = mod_fields[key]["relation"]
                if len(data[key]):
                    res1 = []
                    for rel_id in data[key]:
                        res = [0, 0]
                        if rel == model:
                            continue
                        res.append(self.get_copy_data(rel, rel_id, {}))
                        res1.append(res)
                    result[key] = res1
                else:
                    result[key] = data[key]

            elif mod_fields[key]["type"] == "many2many":
                result[key] = [(6, 0, data[key])]

            else:
                result[key] = data[key]
        for v in obj._inherits.values():
            del result[v]
        return result

    @api.model
    def _create_function(self, doc, model, name, record_id):
        record = doc.createElement("function")
        record.setAttribute("name", name)
        record.setAttribute("model", model)
        record_list = [record]
        value = doc.createElement("value")
        value.setAttribute("eval", "[ref('%s')]" % (record_id,))
        value.setAttribute("model", model)
        record.appendChild(value)
        return record_list, False

    @api.model
    def _generate_object_xml(self, rec, recv, doc, result=None):
        record_list = []
        noupdate = False
        recording_data = self._context.get("recording_data", [])
        if rec[3] == "write":
            for id in rec[4]:
                id, update = self._get_id(rec[2], id)
                noupdate = noupdate or update
                if not id:
                    continue
                record, update = self._create_record(doc, rec[2], rec[5], id)
                noupdate = noupdate or update
                record_list += record

        elif rec[4] in ("menu_create",):
            for id in rec[5]:
                id, update = self._get_id(rec[3], id)
                noupdate = noupdate or update
                if not id:
                    continue
                record, update = self._create_function(doc, rec[3], rec[4], id)
                noupdate = noupdate or update
                record_list += record

        elif rec[3] == "create":
            id = self._create_id(rec[2], rec[4])
            record, noupdate = self._create_record(doc, rec[2], rec[4], id)

            self.blank_dict[(rec[2], result)] = id
            record_list += record

        elif rec[3] == "copy":
            data = self.get_copy_data(rec[2], rec[4], rec[5])
            copy_rec = (rec[0], rec[1], rec[2], rec[3], rec[4], data, rec[5])
            rec = copy_rec
            rec_data = [
                (recording_data[0][0], rec, recording_data[0][2], recording_data[0][3])
            ]
            recording_data = rec_data
            id = self._create_id(rec[2], rec[5])
            record, noupdate = self._create_record(doc, rec[2], rec[5], id)
            self.blank_dict[(rec[2], result)] = id
            record_list += record
        return record_list, noupdate

    @api.model
    def _generate_assert_xml(self, rec, doc):
        pass

    @api.model
    def generate_xml(self):
        recording_data = self._context.get("recording_data", [])
        if recording_data:
            self.blank_dict = {}
            doc = minidom.Document()
            terp = doc.createElement("odoo")
            doc.appendChild(terp)
            for rec in recording_data:
                if rec[0] == "workflow":
                    rec_id, noupdate = self._get_id(rec[1][2], rec[1][4])
                    if not rec_id:
                        continue
                    data = doc.createElement("data")
                    terp.appendChild(data)
                    wkf = doc.createElement("workflow")
                    data.appendChild(wkf)
                    wkf.setAttribute("model", rec[1][2])
                    wkf.setAttribute("action", rec[1][3])
                    if noupdate:
                        data.setAttribute("noupdate", "1")
                    wkf.setAttribute("ref", rec_id)
                if rec[0] == "query":
                    res_list, noupdate = self._generate_object_xml(
                        rec[1], rec[2], doc, rec[3]
                    )
                    data = doc.createElement("data")
                    if noupdate:
                        data.setAttribute("noupdate", "1")
                    if res_list:
                        terp.appendChild(data)
                    for res in res_list:
                        data.appendChild(res)
                elif rec[0] == "assert":
                    pass
            return doc.toprettyxml(indent="\t").encode("utf-8")

