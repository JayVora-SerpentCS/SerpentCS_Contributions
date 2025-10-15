# See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResUsers(models.Model):
    """
    Custom model to manage user-specific menu visibility.
    """

    _inherit = "res.users"

    def write(self, vals):
        """
        Overridden write method for the ResUsers model.
        Ensures that hidden menus remain hidden after modification.
        """
        res = super(ResUsers, self).write(vals)
        for user in self:
            # Link hidden menus to the user
            for menu in user.hide_menu_ids:
                menu.write({"restrict_user_ids": [fields.Command.link(user.id)]})
            # Handle menus that have been unlinked (removed from the hidden list)
            previous_menus = self.env["ir.ui.menu"].search(
                [("restrict_user_ids", "in", [user.id])]
            )
            removed_menus = previous_menus - user.hide_menu_ids
            for menu in removed_menus:
                menu.write({"restrict_user_ids": [fields.Command.unlink(user.id)]})
        return res

    def _compute_get_is_admin(self):
        """
        Compute method to determine if the user is an admin.
        The admin user will have the Hide specific menu tab hidden on their form.
        """
        for user in self:
            user.is_admin = False
            if user.id == self.env.ref("base.user_admin").id:
                user.is_admin = True

    hide_menu_ids = fields.Many2many(
        "ir.ui.menu",
        string="Hidden Menus",
        store=True,
        help="Select menu items to be hidden for this user.",
    )
    is_admin = fields.Boolean(
        compute="_compute_get_is_admin", help="Indicates whether the user is an admin.",
    )


class IrUiMenu(models.Model):
    """
    Custom model to manage menu access restrictions for specific users.
    """

    _inherit = "ir.ui.menu"

    restrict_user_ids = fields.Many2many(
        "res.users",
        string="Restricted Users",
        help="Users who are restricted from accessing this menu.",
    )
