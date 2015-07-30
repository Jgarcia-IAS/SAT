# -*- coding: utf-8 -*-
from openerp import models, fields

class product_template(models.Model):
    _inherit = 'product.template'

    store_ids = fields.Many2many(
        'res.store', 'res_store_partner_rel', 'partner_id', 'store_id',
        'Sucursal', help="""Users that are not of this store, can see this\
        product records but can not post or modify any entry on them.""")

