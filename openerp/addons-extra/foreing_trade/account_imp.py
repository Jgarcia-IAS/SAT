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

class foreign_trade(osv.osv):
    _name = "foreign.trade"
    _columns = {
            'code': fields.char('Numero de Importación'),
            'name': fields.char('Nombre'),
            'date': fields.date('Fecha De Inicio'),
            'date_end': fields.date('Fecha Prevista De Arribo'),
            'guia': fields.char('Guia'),
        }


class account_move(osv.osv):
    _name = "account.move"
    _inherit = "account.move"
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),
        }

class account_move_line(osv.osv):
    _name = "account.move.line"
    _inherit = "account.move.line"
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),
        }

class purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),
        }

    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(purchase_order,self)._prepare_invoice(cr, uid, order, line_ids, context=context)
        invoice_vals.update({'importacion': order.importacion.id})

        return invoice_vals

class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),

        }

class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),

        }

    def action_move_create(self, cr, uid, ids, context=None):
        ret = super(account_invoice, self).action_move_create(cr, uid, ids, context=None)
        if ret:
            for inv in self.browse(cr, uid, ids):
                move_line_ids = []

                for move_line in inv.move_id.line_id:
                    move_line_ids.append(move_line.id)
                    aml_obj = self.pool.get("account.move.line")
                    print "------ction_move_create---------"

                    if inv.type in ('in_invoice', 'in_refund'):
                       for line in inv.invoice_line:
                           if line.product_id.id == move_line.product_id.id:
                              aml_obj.write(cr, uid, move_line.id, {'importacion': line.importacion.id})
 
        return ret

class account_invoice_line(osv.osv):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),

        }


class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
            'importacion': fields.many2one('foreign.trade','Importación', help="Número de la importtació"),

        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
