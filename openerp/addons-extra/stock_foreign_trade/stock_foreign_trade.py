# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Interconsulting S.A e Innovatecsa SAS.
#    (<http://www.interconsulting.com.co).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv


class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _columns = {
        'additional_cost': fields.boolean('Costos adicionales', help="If the active field is set to True, it will not recalculete the average cost when generate the stock move."),
        }

    _defaults = {
        'additional_cost': False,
    }

#    def action_picking_create(self, cr, uid, ids, context=None):
#        for order in self.browse(cr, uid, ids):
#            picking_vals = {
#                'picking_type_id': order.picking_type_id.id,
#                'partner_id': order.dest_address_id.id or order.partner_id.id,
#                'date': max([l.date_planned for l in order.order_line]),
#                'origin': order.name,
#                'additional_cost': order.additional_cost,
#                'move_id': order.id,
#            }
#            picking_id = self.pool.get('stock.picking').create(cr, uid, picking_vals, context=context)
#            self._create_stock_moves(cr, uid, order, order.order_line, picking_id, context=context)
#
#        return super(purchase_order, self).action_picking_create(self, cr, uid, ids,context=None)

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
    _columns = {
        'additional_cost': fields.boolean('Costos adicionales',
         help="If the active field is set to True, it will not recalculete the average cost when generate the stock move."),
        }

    _defaults = {
        'additional_cost': False,
    }

class stock_landed_cost(osv.osv):
    _name = 'stock.landed.cost'
    _description = 'Stock Landed Cost'
    _inherit = 'stock.landed.cost'

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
        'move_id': fields.many2one('stock.move','move_id', help='move_id'),
        'additional_cost': fields.boolean('Costos adicionales',
         help="If the active field is set to True, it will not recalculete the average cost when generate the stock move."),
       }

    _defaults = {
        'additional_cost': False,
    }


