# See LICENSE file for full copyright and licensing details.

from odoo import http
import json
from odoo.http import request
from odoo.exceptions import ValidationError


class WebsiteIpushp(http.Controller):
    @http.route(["/iPushp"], type="http", auth="public", website=True)
    def ipushp(self, **kwargs):
        return request.render(
            "ipushp.iPushp",
            {
                "category_data": request.env["business.category"].sudo().search([]),
                "relation_data": request.env["relation.relation"].sudo().search([]),
            },
        )

    @http.route(["/iPushp/search"], type="http", auth="public", website=True)
    def search(self, **kwargs):
        return request.render(
            "ipushp.search",
            {"category_data": request.env["business.category"].sudo().search([])},
        )

    @http.route(["/iPushp/contacts"], type="http", auth="public", website=True)
    def find_contacts(self, **kwargs):
        category_id = kwargs.get("category_id")
        contact_ids = (
            request.env["business.line"]
            .sudo()
            .search([("category_id", "=", int(category_id))])
        )
        return request.render(
            "ipushp.find_contacts",
            {
                "category_data": request.env["business.category"].sudo().search([]),
                "contact_data": contact_ids,
            },
        )

    @http.route(["/contact/ipushp","/contact/ipushp/<string:model_name>"], type="http", auth="public", website=True)
    def contact_ipushp(self, **kwargs):
        hr_emp_obj = request.env["hr.employee"]
        category_id = kwargs.get("business_categ_id")
        if not category_id:
            return request.redirect("/iPushp")
        if not isinstance(category_id, int):
            category_id = int(category_id)
            if category_id == -1:
                if kwargs.get("category_name"):
                    category_name = kwargs.get("category_name").strip()  # Remove leading/trailing spaces
                    existing_category = request.env["business.category"].sudo().search([("name", "=ilike", category_name)])
                    if existing_category:
                        
                        error_msg = "A Business Category with the same name already exists."

                        return request.render("ipushp.iPushp", {'error_msg': error_msg})
                vals = {"name": category_name}
                category_id = request.env["business.category"].sudo().create(vals)
                category_id = category_id.id
        if kwargs.get("user_id"):
            employee = hr_emp_obj.sudo().search(
                [("user_id", "=", int(kwargs.get("user_id")))]
            )
            contact_details = {
                "name": kwargs.get("name"),
                "phone": kwargs.get("phone"),
                "email": kwargs.get("email"),
                "description": kwargs.get("description"),
                "relation": kwargs.get("relation_id"),
                "category_id": category_id,
            }
            employee.sudo().write({"ipushp_ids": [(0, 0, contact_details)]})
        return request.redirect('/thankyoupage')
    

    @http.route(["/thankyoupage"], type="http", auth="public", website=True)
    def thankyoupage(self, **kwargs):

        return request.render("ipushp.ipushp_thanks", {})


    
