# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class ProjectKanbanTest(common.TransactionCase):
    def setup(self):
        super(ProjectKanbanTest, self).setup()

    def test_project_kanban(self):
        self.project_obj = self.env["project.project"]
        self.project_obj.create(
            {
                "name": "Project Kanban",
                "recent_date": self.project_obj._compute_get_recent_date(),
            }
        )
