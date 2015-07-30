# -*- coding: utf-8 -*-
from openerp import models, fields


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    store_id = fields.Many2one(
        'res.store', 'Sucursal', required = True ,
         help="""  Sucursal. """)

    _defaults = {
        'store_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).store_id.id,
    }
