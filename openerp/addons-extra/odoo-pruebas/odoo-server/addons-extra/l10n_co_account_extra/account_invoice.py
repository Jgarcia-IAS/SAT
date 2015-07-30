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

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def convert_co(self): 
        return self.pool.get('ir.translation').amount_to_text(amount, 'co','pesos')

    _columns = {
        #'amount_in_word': fields.char('Son:', size=128, select=True, readonly=True, states={'draft':[('readonly',False)]}),
        'amount_in_word': fields.function(convert_co, string='Son:', type='char'),
        'discount' : fields.float('Descuento', required=True, readonly=True),
        'amount_iva' : fields.float('IVA', required=True, readonly=True),
        'amount_rte' : fields.float('Retención ', required=True, readonly=True),
        'amount_cree' : fields.float('CREE', required=True, readonly=True),
        'amount_reteiva' : fields.float('ReteIVA', required=True, readonly=True),        
    }

    _defaults = {
        'discount': 0,
        'amount_iva': 0,
        'amount_rte': 0,
        'amount_cree': 0,
        'amount_reteiva': 0,
    }
    
        
