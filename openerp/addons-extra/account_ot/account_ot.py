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


class account_move(osv.osv):
    _name = "account.move"
    _inherit = "account.move"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con este movimiento"),

        }


class account_move_line(osv.osv):
    _name = "account.move.line"
    _inherit = "account.move.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT',
             store=True,related = 'move_id.ot', 
            help="Orden de trabajo relacionada con esta orden de compras"),

        }



class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con esta orden de compras"),

        }



    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(purchase_order,self)._prepare_invoice(cr, uid, order, line_ids, context=context)

        invoice_vals.update({'ot': order.ot.id})

        return invoice_vals



class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
                  store=True,related = 'order_id.ot',
            help="Orden de trabajo relacionada con esta orden de compras"),

        }



class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"),

        }


    def action_move_create(self, cr, uid, ids, context=None):
        ret = super(account_invoice, self).action_move_create(cr, uid, ids, context=None)
        if ret:
            for inv in self.browse(cr, uid, ids):
                move_line_ids = []
                for move_line in inv.move_id.line_id:
                    move_line_ids.append(move_line.id)
                    aml_obj = self.pool.get("account.move.line")
                    aml_obj.write(cr, uid, move_line_ids, {'ot': inv.ot.id})
        return ret




class account_invoice_line(osv.osv):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
    _columns = {
            'ot': fields.many2one('mrp.repair', string='OT', 
                  store=True,related = 'invoice_id.ot',
                  help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"
             ),
        }

 
   



class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"),

        }
    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(sale_order,self)._prepare_invoice(cr, uid, order, line_ids, context=context)

        invoice_vals.update({'ot': order.ot.id})

        return invoice_vals


class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = "sale.order.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
                  store=True,related = 'order_id.ot',
                  help="Orden de trabajo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

class hr_expense_expense(osv.osv):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
             help="Orden de trabajo relacionada con este gasto"),

        }

          
      


class hr_expense_line(osv.osv):
    _name = "hr.expense.line"
    _description = "Expense Line"

    _inherit = "hr.expense.line"
    _columns = {
            'ot': fields.many2one('mrp.repair','OT', 
                  store=True,related = 'expense_id.ot',
             help="Orden de trabajo relacionada con este gasto"),

        }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
