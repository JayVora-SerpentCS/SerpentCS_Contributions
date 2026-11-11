# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    digital_signature = fields.Binary(string="Signature")

    # Override of SELF_READABLE_FIELDS / SELF_WRITEABLE_FIELDS (properties since
    # 17.0) so the user can see and edit their own digital signature from the
    # preferences form, as with the standard 'signature' field.
    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["digital_signature"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["digital_signature"]
