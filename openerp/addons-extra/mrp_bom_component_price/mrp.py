# -*- coding: utf-8 -*-

from osv import osv, fields

class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'
    _name = 'mrp.bom'

    _columns = {
        'product_standard_price': fields.related("product_id", "standard_price", type="float", string="Cost price"),
    }

mrp_bom()
