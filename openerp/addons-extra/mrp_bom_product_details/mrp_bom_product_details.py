# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Solutions Libergia inc. (<http://www.libergia.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm , osv
from openerp.addons.decimal_precision import decimal_precision as dp

class mrp_bom_line(orm.Model):
    _inherit = 'mrp.bom.line'

    def _get_unit_cost(self, cr, uid, ids, field_name, arg, context):
        result = {}

        for bom_line_obj in self.browse(cr, uid, ids, context=context):
            result[bom_line_obj.id] = bom_line_obj.product_id.product_tmpl_id.standard_price or 0.00
        return result 

    def _get_product_total_cost(self, cr, uid, ids, field_name, arg, context):
        result = {}

        for bom_line_obj in self.browse(cr, uid, ids, context=context):
            result[bom_line_obj.id] = (bom_line_obj.product_id.product_tmpl_id.standard_price or 0.00) * (bom_line_obj.product_qty or 0.00)
        return result 



    _columns = {
        'product_standard_price': fields.related(
            'product_id',
            'standard_price',
            type='float',
            string='Cost Price',
            readonly=True,
        ),
        'product_qty_available': fields.related(
            'product_id',
            'qty_available',
            type='float',
            string='Quantity on Hand',
            readonly=True,
        ),
        'product_unit_cost' : fields.function(_get_unit_cost, string="Product Cost", digits_compute=dp.get_precision('Product Price')),
        'product_total_cost' : fields.function(_get_product_total_cost, string="Total Cost", digits_compute=dp.get_precision('Product Price')),

    }

class mrp_bom(orm.Model):
    _inherit = 'mrp.bom'

    def get_total_cost(self, cr, uid, ids, name, args, context=None):
        res = {}
        for rec in self.browse(cr, uid, ids, context=context):
            total_cost = 0.0
            for line_rec in rec.bom_line_ids:
                total_cost += line_rec.product_total_cost or 0.0
            res.update({rec.id : total_cost})
        return res

    _columns = {
        'total_cost' : fields.function(get_total_cost, string="Total Cost"),


    }
