#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _


class sale_order(osv.osv):
    _inherit = "sale.order"

    def check_limit(self, cr, uid, ids, context=None):
        for order_id in ids:
            processed_order = self.browse(cr, uid, order_id, context=context)
            if processed_order.order_policy == 'prepaid':
                continue
            partner = processed_order.partner_id
            if partner.credit_limit > 0:
                credit = partner.credit
                available_credit = partner.credit_limit - credit
                if processed_order.amount_total > available_credit:
                    title = 'Cupo de credito excedido!'
                    msg = u'Can not confirm the order since the credit balance is %s\n \
    You can still process the Sales Order by change the Invoice Policy to "Before Delivery."'
                    raise osv.except_osv(_(title), _(msg) % (available_credit,))
                    return False
                    
            #busca la factura más antigua
            cr.execute("select min(l.date_maturity) fecha from account_move_line l\
                             inner join account_account a on (a.id = l.account_id) \
                             where l.reconcile_id is null \
							   and a.type = 'receivable' \
							   and l.debit > 0 \
                               and l.partner_id = %s",(partner.id,))
                               
            res = cr.fetchone()[0] or False
            if res:
                    dd = datetime.strptime(res, "%Y-%m-%d")
	            delta = datetime.today() - dd
                    if delta.days > partner.date_due_limite:
                       title = 'Fecha limite excedida!'
                       msg = u'Can not confirm the order since the date due is more than %s days. Days due %s\n \
    You can still process the Sales Order by change the Invoice Policy to "Before Delivery."'
	               raise osv.except_osv(_(title), _(msg) % (partner.date_due_limite, delta.days))
	               return False
            
        return True

sale_order()

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {                 
        'date_due_limite': fields.integer('Días concedidos'),
        'base_date_due': fields.integer('Base días concedidos'),
        'base_credit'  : fields.float('Base crédito concedido'),
    }
    
    _defaults = {
      'date_due_limite' : 0,
      'base_date_due': 0,
      'base_credit'  : 0,
    }
    
    def refresh_credit_limit(self, cr, uid, context=None):
        
        cr.execute("update res_partner set date_due_limite = base_date_due, credit_limit = base_credit where customer = True")
            
        return True
    
    
