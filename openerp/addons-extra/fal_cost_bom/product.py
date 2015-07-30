# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    def get_cost(self, cr, uid, product_id, context=None):
        cost_of_bom = 0.00
        if not product_id:
            return cost_of_bom
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        if product_id.bom_ids :
            bom_id = bom_obj.browse(cr, uid, product_id.bom_ids[0].id, context=context)
            for bom_line in bom_id.bom_line_ids:
                pro_qty = bom_line.product_qty
                if bom_line.product_uom.id != bom_line.product_uom.id:
                    pro_qty = uom_obj._compute_qty(cr, uid, bom_line.product_uom.id, bom_line.product_qty, bom_line.product_uom.id)
                if bom_line.product_id.bom_ids:
                    cost_of_bom += pro_qty * self.get_cost(cr, uid, bom_line.product_id,  context=context) 
                else:
                    cost_of_bom += pro_qty * bom_line.product_id.standard_price
        else:
            cost_of_bom = product_id.standard_price
        return cost_of_bom
       
    def _get_cost_bom(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for product_id in self.browse(cr, uid, ids, context=context):
            cost_of_bom = self.get_cost(cr, uid, product_id,  context=context) 
            res[product_id.id] = cost_of_bom
        return res
    
    def _get_bom(self, cr, uid, ids, context=None):
        result = {}
        for bom in self.pool.get('mrp.bom').browse(cr, uid, ids, context=context):
            result[bom.product_id.id] = True
        return result.keys()
        
    _columns = {
        'fal_bom_costs' : fields.function(_get_cost_bom, type='float', string='Cost of BoM',
            help="Cost of Raw Material",
            digits_compute=dp.get_precision('BoM Cost'),
            store=False
            ),
    }

#end of product_product()