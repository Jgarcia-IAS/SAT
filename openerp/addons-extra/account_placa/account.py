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
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }


class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"

    _columns = {
            'placa': fields.many2one('fleet.vehicle', string='placa',
                  store=True,related = 'picking_id.placa',
                  help="Número de la placa"
             ),
        }

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }




class account_move_line(osv.osv):
    _name = "account.move.line"
    _inherit = "account.move.line"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }



class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        invoice_vals = super(purchase_order,self)._prepare_inv_line(cr, uid, account_id, order_line, context=context)
        invoice_vals.update({'placa': order_line.placa.id})
        print "-----------order_line.placa------------"
        print order_line.placa
        return invoice_vals






class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }



class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

#    def action_move_create(self, cr, uid, ids, context=None):
#        ret = super(account_invoice, self).action_move_create(cr, uid, ids, context=None)
#        if ret:
#            for inv in self.browse(cr, uid, ids):
#                move_line_ids = []
#
#                for move_line in inv.move_id.line_id:
#                    move_line_ids.append(move_line.id)
#                    aml_obj = self.pool.get("account.move.line")
#                    print "------ction_move_create---------"
#
#                    if inv.type in ('out_invoice', 'out_refund'):
#                        aml_obj.write(cr, uid, move_line_ids, {'placa': inv.placa.id})
#                    else: 
#
#                        for line in inv.invoice_line:
#                           if line.product_id.id == move_line.product_id.id:
#                                aml_obj.write(cr, uid, move_line.id, {'placa': line.placa.id})
 
#        return ret

class account_invoice_line(osv.osv):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

 
class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }
    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(sale_order,self)._prepare_invoice(cr, uid, order, line_ids, context=context)

        invoice_vals.update({'placa': order.placa.id})
        print "-----------sale order------------"
        print order.placa.id


        return invoice_vals




class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = "sale.order.line"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', 
             store=True,related = 'order_id.placa',
             help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }


    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
 
        invoice_vals = super(sale_order_line,self)._prepare_order_line_invoice_line(cr, uid,  line,account_id, context=context)
        invoice_vals.update({'placa': line.placa.id})
        print "-----------sale order line ------------"
        print line.placa.id

        return invoice_vals


class hr_expense_expense(osv.osv):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

    def line_get_convert(self, cr, uid, x, part, date, context=None):
        invoice_vals = super(hr_expense_expense,self).line_get_convert(cr, uid, x, part, date, context=context)
        invoice_vals.update({'placa': x.get('placa', False)})
        return invoice_vals

    def move_line_get_item(self, cr, uid, line, context=None):
        invoice_vals = super(hr_expense_expense,self).move_line_get_item(cr, uid, line, context=context)
        invoice_vals.update({'placa':line.placa.id,})
        return invoice_vals


class hr_expense_line(osv.osv):
    _name = "hr.expense.line"
    _description = "Expense Line"

    _inherit = "hr.expense.line"
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

class account_bank_statement(osv.osv):
    _inherit = 'account.bank.statement'
    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }
    def _prepare_move_line_vals(self, cr, uid, st_line, move_id, debit, credit, currency_id=False,
                amount_currency=False, account_id=False, partner_id=False, context=None):

        invoice_vals = super(account_bank_statement,self)._prepare_move_line_vals( cr, uid, st_line, move_id, debit, credit, currency_id,
                amount_currency, account_id, partner_id, context=context)

        invoice_vals.update({'placa': st_line.placa.id})

        return invoice_vals


class account_bank_statement_line(osv.osv):
    _inherit = 'account.bank.statement.line'

    _columns = {
            'placa': fields.many2one('fleet.vehicle','Placa', help="Placa del vehiculo relacionada con esta Factura de proveedor o Factura de cliente"),

        }

#===================================================================================



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
