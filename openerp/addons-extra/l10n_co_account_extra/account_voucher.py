# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv,fields
from openerp.tools.translate import _

class account_voucher(osv.osv):
    _inherit = 'account.voucher'
    def _get_partner_bank(self, cr, uid, context=None):
        if self.partner_id:
            p = self.pool.get('res.partner').browse(cr, uid, self.partner_id)
            if p.bank_ids:
                bank_id = p.bank_ids[0].id
                if partner_bank_id != bank_id:
                    to_update = self.onchange_partner_bank(cr, uid, ids, bank_id)
                    result['value'].update(to_update['value'])
                    return result

    _columns = {
        'partner_bank_id': fields.many2one('res.partner.bank', 'Bank Account',
            help='Bank Account Number to which the invoice will be paid. A Company bank account if this is a Customer Invoice or Supplier Refund, otherwise a Partner bank account number.', readonly=True, states={'draft':[('readonly',False)]}),        
    }

    _defaults = {
        'partner_bank_id': _get_partner_bank,
    }
    
    
