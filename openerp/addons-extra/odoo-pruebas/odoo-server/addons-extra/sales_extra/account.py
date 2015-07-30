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

class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _columns = {
        'x_partner_name': fields.char('Name', track_visibility='always', readonly=True, copy=False),
        'x_vat': fields.char('Name', track_visibility='always', readonly=True, copy=False),
        'x_street': fields.char('Name', track_visibility='always', readonly=True, copy=False),
        'x_partner': fields.char('Name', track_visibility='always', readonly=True, copy=False),

        }

    def action_move_create(self, cr, uid, ids, context=None):
        ret = super(account_invoice, self).action_move_create(cr, uid, ids, context=None)
        if ret:
            for inv in self.browse(cr, uid, ids):
                move_line_ids = []
                for move_line in inv.move_id.line_id:
                    move_line_ids.append(move_line.id)
                    aml_obj = self.pool.get("account.move.line")
                    aml_obj.write(cr, uid, move_line_ids, {'x_partner_name': inv.ot.id})
                    aml_obj.write(cr, uid, move_line_ids, {'x_vat': inv.ot.id})
                    aml_obj.write(cr, uid, move_line_ids, {'x_street': inv.ot.id})
                    aml_obj.write(cr, uid, move_line_ids, {'x_partner': inv.ot.id})
 
        return ret

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _columns = {
        'x_partner_name': fields.char('Name', track_visibility='always', readonly=True, copy=False),
        'x_vat': fields.char('Name', track_visibility='always', readonly=True, copy=False),
        'x_street': fields.char('Name', track_visibility='always', readonly=True, copy=False),
        'x_partner': fields.char('Name', track_visibility='always', readonly=True, copy=False),

        }
    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(sale_order,self)._prepare_invoice(cr, uid, order, line_ids, context=context)

        invoice_vals.update({'x_partner_name': order.x_partner_name})
        invoice_vals.update({'x_vat': order.x_vat})
        invoice_vals.update({'x_street': order.x_street})
        invoice_vals.update({'x_partner': order.x_partner})

        return invoice_vals





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
