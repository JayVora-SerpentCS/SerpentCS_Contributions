# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class ProjectProjectTestCase(common.TransactionCase):
    def setup(self):
        super(ProjectProjectTestCase, self).setup()

    def test_project_action(self):
        user_1 = self.env.ref('base.user_root')
        user_2 = self.env.ref('base.user_demo')

        team = self.env['crm.team'].sudo().create({
            'name': 'Test Project Team',
            'user_id': user_1.id,
            'type_team': 'sale',
            'team_members_ids': [(6, 0, [user_1.id, user_2.id])]})
        project = self.env['project.project'].sudo().create({
            'name': 'Test Project',
            'team_id': team.id
        })
        project._get_team_members()
        self.assertEqual(team.name, project.team_id.name)
