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

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"
        
    _columns = {
       'unit_price' : fields.float('Precio Unit.', help="Precio unitario de la operacion", required=True),       
       'cost' : fields.float('Costo', help="Costo promedio", required=True),       
       'account_move_ids': fields.many2many('account.move', 'stock_move_account_rel', 'stock_id', 'move_id', 'Movimientos contables', help='Movimientos contables generados', copy=False),
    }
    _defaults = {
       'unit_price' : 0.00,
       'cost' : 0.00,
    }

class account_move_line(osv.osv):
    _name = "account.move.line"
    _inherit = "account.move.line"
        
    _columns = {
       'stock_id': fields.many2one('stock.move', 'Mov. almacen', help="Relaciona el movimiento de almacen con el movimiento contable"),
       'quant_id': fields.many2one('stock.quant', 'Mov. almacen', help="Relaciona el movimiento de almacen con el movimiento contable"),
    }

class stock_quant(osv.osv):
    _inherit = "stock.quant"

    def _prepare_account_move_line(self, cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=None):
        res = super(stock_quant, self)._prepare_account_move_line(cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=context)
        
        debit_line_vals = {'stock_id' : move.id,
                          }
        credit_line_vals = {'stock_id' : move.id,
                           }
        res[0][2].update(debit_line_vals)
        res[1][2].update(credit_line_vals)
        
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
