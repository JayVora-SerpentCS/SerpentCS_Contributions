# See LICENSE file for full copyright and licensing details.

import werkzeug
from odoo import http
from odoo.http import request
import odoo.addons.website_sale.controllers.main
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

PPG = 20
PPR = 4


class WebsiteSale(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/
        <int:page>''',
        '''/shop/brands'''],
        type='http', auth="public", website=True,
        sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False,
             brand=None, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")]
                         for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category),
                        search=search, attrib=attrib_list,
                        order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context,
                               pricelist=pricelist.id,
                               partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)
        values = {}

        # Brand's product search
        if brand:
            values.update({'brand': brand})
            product_designer_obj = request.env['product.brand']
            brand_ids = product_designer_obj.search([('id', '=', int(brand))])
            domain += [('product_brand_id', 'in', brand_ids.ids)]

        search_product = Product.search(domain)
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search(
                [('product_tmpl_ids', 'in',
                  search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(
            url=url, total=product_count, page=page,
            step=ppg, scope=7, url_args=post)
        products = Product.search(
            domain, limit=ppg, offset=pager['offset'],
            order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search(
                [('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref(
                    'website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = self.currency_compute(from_currency, to_currency)

        values.update({
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        })
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    def currency_compute(self, from_currency, to_currency):
        return lambda price: from_currency.compute(price,
                                                   to_currency)

    # Method to get the brands.
    @http.route(['/page/product_brands'], type='http', auth='public',
                website=True)
    def product_brands(self, **post):
        brand_values = []
        brand_obj = request.env['product.brand']
        domain = []
        if post.get('search'):
            domain += [('name', 'ilike', post.get('search'))]
        brand_ids = brand_obj.search(domain)
        for brand_rec in brand_ids:
            brand_values.append(brand_rec)

        keep = QueryURL('/page/product_brands', brand_id=[])
        values = {'brand_rec': brand_values, 'keep': keep}
        if post.get('search'):
            values.update({'search': post.get('search')})
        return request.render('website_product_brand.product_brands', values)
