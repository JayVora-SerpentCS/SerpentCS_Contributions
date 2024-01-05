# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class CrmLeadFunnelTestCase(common.TransactionCase):
    def setup(self):
        super(CrmLeadFunnelTestCase, self).setup()

    def tests_crm_lead_funnel(self):
        self.stageA = self.env.ref("crm.stage_lead1")
        self.stageB = self.env.ref("crm.stage_lead2")
        self.stageC = self.env.ref("crm.stage_lead3")
        self.crm_obj = self.env["crm.lead"]
        self.crmA = self.crm_obj.create(
            {"name": "Need to customize the solution", "stage_id": self.stageA.id}
        )
        self.crmB = self.crm_obj.create(
            {
                "name": "“Resource Planning” project develpment",
                "stage_id": self.stageB.id,
            }
        )
        self.crmC = self.crm_obj.create(
            {"name": "Interest in your customizable Pcs", "stage_id": self.stageC.id}
        )
        self.crm_obj.get_lead_stage_data()
