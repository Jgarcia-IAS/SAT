# -*- coding: utf-8 -*-
from openerp import models, fields


class stok_warehouse(models.Model):
    _inherit = 'stock.warehouse'

    store_id = fields.Many2one(
        'res.store', 'Sucursal', required = True ,
         help="""  Sucursal. """)

    _defaults = {
        'store_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).store_id.id,
    }

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    store_id = fields.Many2one(
        'res.store', 'Sucursal', required = True ,
         help="""  Sucursal. """)

    _defaults = {
        'store_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).store_id.id,
    }
