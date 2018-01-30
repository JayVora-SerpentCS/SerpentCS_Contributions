# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class ProjectProjectTestCase(common.TransactionCase):
    def setup(self):
        super(ProjectProjectTestCase, self).setup()

    def test_project_action(self):
        self.team = self.env.ref('base.user_root')
        self.team1 = self.env.ref('base.user_demo')

        self.team = self.env['crm.team'].sudo().create({
            'name': 'Test Project Team',
            'user_id': self.team.id,
            'type_team': 'sale',
            'team_members': [(6, 0, [self.team.id,
                                     self.team1.id])]})
        self.project = self.env['project.project'].create({
            'name': 'Test Project',
            'team_id': self.team.id})
        self.project.get_team_members()
