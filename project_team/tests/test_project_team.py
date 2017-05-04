# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo.tests import common


class ProjectProjectTestCase(common.TransactionCase):
    def setUp(self):
        super(ProjectProjectTestCase, self).setUp()

    def test_project_action(self):
        self.res_user_model = self.env['res.users']
        self.team_member_user = self.res_user_model.\
            with_context({'no_reset_password': True}).\
                create(dict(
                name="Team Member",
                company_id=self.env.user.company_id.id,
                login="test",
                email="team@yourcompany.com",
        ))
        self.team_member_user2 = self.res_user_model.\
            with_context({'no_reset_password': True}).\
                create(dict(
                name="Team Member 2",
                company_id=self.env.user.company_id.id,
                login="acc",
                email="team2@yourcompany.com",
        ))
        self.team = self.env['crm.team'].sudo().create({
            'name': 'Test Project Team',
            'user_id': self.team_member_user.id,
            'type_team': 'sale',
            'team_members': [(6, 0, [self.team_member_user2.id,
                                     self.team_member_user.id])],
        })
        self.project = self.env['project.project'].\
            create({'name': 'Test Project',
                    'team_id': self.team.id})
        self.project.get_team_members()
