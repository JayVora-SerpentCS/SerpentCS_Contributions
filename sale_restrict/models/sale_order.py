from openerp import models,fields,api,_
from openerp.exceptions import Warning

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def action_button_confirm(self):
        zero_price = [x.product_id.name for x in self.order_line if not x.price_unit]
        if zero_price:
            message= _("Please specify unit price for the following products:") + '\n'
            message += '\n'.join(map(str,zero_price))
            raise Warning(message.rstrip())
        return super(sale_order,self).action_button_confirm()
    
